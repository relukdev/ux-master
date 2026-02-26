# Spec 04: Add Test Suite

## Problem

No automated tests exist for the core pipeline. Changes frequently break output quality with no way to detect regressions.

## Test Structure

```
tests/
├── conftest.py                    # Shared fixtures (sample harvest data)
├── test_token_mapper.py           # Unit tests for token mapping
├── test_component_generator.py    # Tests generated code compiles
├── test_color_utils.py            # Color utility functions
├── test_neutral_scale.py          # Neutral scale generation
├── test_design_system_indexer.py  # Design system indexing
├── test_doc_generator.py          # Doc HTML generation
├── test_integration.py            # End-to-end pipeline
└── fixtures/
    ├── harvest_fila.json          # Real harvest from Fila template
    ├── harvest_dark_theme.json    # Dark theme sample
    ├── harvest_minimal.json       # Minimal valid harvest
    └── expected_tokens.json       # Expected token output
```

## Key Tests

### test_color_utils.py
```python
def test_normalizeColor_hex():
    assert normalizeColor("#ff0000") == "#FF0000"
    
def test_normalizeColor_rgb():
    assert normalizeColor("rgb(255, 0, 0)") == "#FF0000"

def test_isNeutral_gray():
    assert isNeutral("#808080") == True
    
def test_isNeutral_red():
    assert isNeutral("#FF0000") == False

def test_luminance_white():
    assert luminance("#FFFFFF") == pytest.approx(255, abs=1)

def test_contrastRatio_bw():
    ratio = contrastRatio("#FFFFFF", "#000000")
    assert ratio == pytest.approx(21.0, abs=0.5)
```

### test_token_mapper.py
```python
def test_primary_color_mapped(sample_harvest):
    tokens = map_to_semi_tokens(sample_harvest)
    assert "--semi-color-primary" in tokens
    assert tokens["--semi-color-primary"] == "#0F79F3"

def test_neutral_scale_has_gradient(sample_harvest):
    tokens = map_to_semi_tokens(sample_harvest)
    n50 = luminance(tokens.get("--semi-color-neutral-50", "#FFF"))
    n900 = luminance(tokens.get("--semi-color-neutral-900", "#000"))
    assert n50 - n900 > 100  # Must have visible gradient

def test_text_hierarchy(sample_harvest):
    tokens = map_to_semi_tokens(sample_harvest)
    text0_lum = luminance(tokens["--semi-color-text-0"])
    text1_lum = luminance(tokens["--semi-color-text-1"])
    assert text0_lum < text1_lum  # text-0 is darkest
```

### test_component_generator.py
```python
import subprocess

def test_generated_button_compiles(design_system):
    gen = ComponentGenerator(design_system, "react-tailwind")
    code = gen.generate("button")
    
    # Write to temp file
    Path("/tmp/test_button.tsx").write_text(code)
    
    # Check TypeScript compilation
    result = subprocess.run(
        ["npx", "tsc", "--noEmit", "--jsx", "react-jsx", "/tmp/test_button.tsx"],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"TSC errors: {result.stderr}"

def test_generated_code_has_no_uppercase_tags(design_system):
    gen = ComponentGenerator(design_system, "react-tailwind")
    for component_type in ["button", "card", "input", "badge"]:
        code = gen.generate(component_type)
        # No uppercase HTML tags like <BUTTON>, <DIV>
        assert "<BUTTON" not in code
        assert "<DIV" not in code
        assert "<INPUT" not in code
```

### test_integration.py
```python
def test_full_pipeline_from_harvest():
    """End-to-end: harvest JSON → tokens → components → doc page"""
    harvest = json.load(open("tests/fixtures/harvest_fila.json"))
    
    # Step 1: Token mapping
    tokens = map_to_semi_tokens(harvest)
    assert len(tokens) > 50
    
    # Step 2: Design system indexing
    ds = DesignSystem(name="TestApp")
    ds.colors = tokens  # simplified
    css = ds.generate_css()
    assert ":root" in css
    assert "--semi-color-primary" in css
    
    # Step 3: Component generation
    gen = ComponentGenerator({"tokens": tokens}, "react-tailwind")
    button = gen.generate("button")
    assert "forwardRef" in button
    assert "HTMLButtonElement" in button
    
    # Step 4: Doc generation
    html = generate_doc_html(tokens, harvest)
    assert "<html" in html
    assert "Color Palette" in html
```

## Running Tests

```bash
# All tests
python3 -m pytest tests/ -v

# Specific file
python3 -m pytest tests/test_token_mapper.py -v

# With coverage
python3 -m pytest tests/ --cov=scripts --cov-report=html
```

## Acceptance Criteria

- [ ] `pytest tests/` runs and all pass
- [ ] Coverage > 60% for core modules
- [ ] Test fixtures include at least 3 different harvest samples
- [ ] Integration test covers full pipeline
- [ ] Tests run in < 30 seconds (no network calls)
