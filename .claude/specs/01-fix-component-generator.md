# Spec 01: Fix Component Generator

## Problem

`scripts/component_generator.py` generates React/Semi/Vue component code with critical syntax errors that prevent compilation.

## Current Bugs

### Bug 1: Wrong HTML Tag Casing
```tsx
// ❌ Current
<BUTTON ref={ref} ...>
// ✅ Expected
<button ref={ref} ...>
```

### Bug 2: Broken forwardRef Destructuring
```tsx
// ❌ Current — missing opening brace
>((variant, size, disabled, loading, children, className, ...props}, ref) => {
// ✅ Expected
>(({ variant, size, disabled, loading, children, className, ...props }, ref) => {
```

### Bug 3: Broken className Template
```tsx
// ❌ Current — unclosed strings, invalid object syntax inside cn()
className={cn(
    "inline-flex items-center justify-center
    font-medium transition-colors
    "  // Size: sm
      "h-8 px-3 text-sm": size === "sm",

// ✅ Expected — proper cn() with object syntax
className={cn(
    "inline-flex items-center justify-center font-medium transition-colors",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
    "disabled:pointer-events-none disabled:opacity-50",
    {
      "h-8 px-3 text-sm": size === "sm",
      "h-10 px-4 text-base": !size || size === "md",
      "h-12 px-6 text-lg": size === "lg",
    },
    {
      "bg-primary text-white hover:bg-primary/90": variant === "primary",
      "bg-secondary text-secondary-foreground hover:bg-secondary/90": variant === "secondary",
      "border border-input bg-background hover:bg-accent": variant === "outline",
      "hover:bg-accent hover:text-accent-foreground": variant === "ghost",
    },
    className
)}
```

### Bug 4: Wrong TypeScript Interface for HTMLElement
```tsx
// ❌ Current
React.forwardRef<HTMLBUTTONElement, ButtonProps>
// ✅ Expected
React.forwardRef<HTMLButtonElement, ButtonProps>
```

## Files to Modify

- `scripts/component_generator.py` — main fix target
  - Function: `generate_react_component()` (line 32-73)
  - Function: `generate_semi_component()` (line 76-115)
  - Function: `generate_vue_component()` (line 118-149)
  - Function: `ComponentGenerator._generate_react()` (line 362-400)

## Fix Strategy

### Step 1: Fix Template Strings

In `generate_react_component()`, replace the template literal that builds the component code. The JSX must have:
- Lowercase HTML elements (`<button>`, `<div>`, `<input>`)
- Proper `forwardRef` destructuring with outer braces
- Valid `cn()` usage with object syntax for conditional classes
- Proper string escaping in template literals

### Step 2: Fix Element Type Mapping

Create a mapping:
```python
ELEMENT_TYPE_MAP = {
    "button": {"tag": "button", "ref": "HTMLButtonElement"},
    "input": {"tag": "input", "ref": "HTMLInputElement"},
    "card": {"tag": "div", "ref": "HTMLDivElement"},
    "badge": {"tag": "span", "ref": "HTMLSpanElement"},
    "avatar": {"tag": "div", "ref": "HTMLDivElement"},
    "alert": {"tag": "div", "ref": "HTMLDivElement"},
    # ... for all component types
}
```

### Step 3: Fix cn() Generation

Generate proper `clsx`/`cn` calls:
```python
def generate_cn_call(base_classes, size_variants, style_variants):
    """Generate a valid cn() call with conditional classes."""
    parts = [f'"{base_classes}"']
    
    if size_variants:
        size_obj = ", ".join([f'"{cls}": size === "{name}"' for name, cls in size_variants.items()])
        parts.append(f"{{{size_obj}}}")
    
    if style_variants:
        style_obj = ", ".join([f'"{cls}": variant === "{name}"' for name, cls in style_variants.items()])
        parts.append(f"{{{style_obj}}}")
    
    parts.append("className")
    return f"cn(\n        {',\n        '.join(parts)}\n      )"
```

## Verification

```bash
# 1. Generate components
python3 scripts/component_generator.py \
  --input output/fila/design-system.json \
  --all --output /tmp/test-components

# 2. Create temp tsconfig for validation
cat > /tmp/test-components/tsconfig.json << 'EOF'
{
  "compilerOptions": {
    "jsx": "react-jsx",
    "target": "ES2020",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "noEmit": true,
    "paths": { "@/*": ["./*"] }
  },
  "include": ["**/*.tsx"]
}
EOF

# 3. Add cn utility stub
cat > /tmp/test-components/lib/utils.ts << 'EOF'
export function cn(...args: any[]): string { return args.filter(Boolean).join(" "); }
EOF

# 4. Verify compilation
cd /tmp/test-components && npx tsc --noEmit
# Expected: No errors

# 5. Visual check — render in a simple React app
```

## Acceptance Criteria

- [ ] All generated `.tsx` files pass `tsc --noEmit`
- [ ] Generated Button component renders with correct styles
- [ ] Generated Card component renders with box-shadow and border-radius from tokens
- [ ] Generated Input component renders with correct focus and disabled states
- [ ] Semi Design variant uses `@douyinfe/semi-ui` imports correctly
- [ ] Vue variant uses Composition API with `defineProps` correctly
