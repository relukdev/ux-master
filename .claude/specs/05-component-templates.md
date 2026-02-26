# Spec 05: Component Template System

## Approach: Smart Templates + Token Injection

Replace current "generate code from scratch" (buggy) with a robust template system:

1. **Pre-built, tested templates** for 22 components
2. **Token injection points** filled at generation time
3. **Each template is valid TSX** before injection

## Template Format

Each component template in `templates/components/{name}/`:

```
templates/components/
├── button/
│   ├── react.tsx.tmpl      # React + Tailwind template
│   ├── semi.tsx.tmpl        # Semi Design wrapper template
│   ├── vue.vue.tmpl         # Vue 3 template
│   ├── props.ts             # TypeScript interface (shared)
│   ├── stories.tsx.tmpl     # Storybook story
│   └── spec.json            # Component spec metadata
├── card/
├── input/
├── ...
└── _shared/
    ├── utils.ts             # cn() utility
    └── types.ts             # Shared types
```

### Template Syntax

Use simple `{{TOKEN_NAME}}` placeholders:

```tsx
// templates/components/button/react.tsx.tmpl
"use client";

import React from "react";
import { cn } from "../_shared/utils";

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "primary", size = "md", loading, className, children, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={cn(
          "inline-flex items-center justify-center font-medium transition-colors",
          "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2",
          "disabled:pointer-events-none disabled:opacity-50",
          {
            "h-8 px-3 text-sm": size === "sm",
            "h-10 px-4 text-base": size === "md",
            "h-12 px-6 text-lg": size === "lg",
          },
          {
            "text-white hover:opacity-90": variant === "primary",
            "text-white hover:opacity-90": variant === "secondary",
            "border bg-transparent hover:opacity-80": variant === "outline",
            "bg-transparent hover:bg-gray-100": variant === "ghost",
            "bg-red-500 text-white hover:bg-red-600": variant === "danger",
          },
          className
        )}
        style={{
          ...(variant === "primary" && { backgroundColor: "var(--semi-color-primary)" }),
          ...(variant === "secondary" && { backgroundColor: "var(--semi-color-tertiary)" }),
          ...(variant === "outline" && {
            borderColor: "var(--semi-color-primary)",
            color: "var(--semi-color-primary)",
          }),
          borderRadius: "var(--semi-border-radius-medium, 6px)",
          fontFamily: "var(--semi-font-family-regular)",
        }}
        {...props}
      >
        {loading && <span className="mr-2 animate-spin">⏳</span>}
        {children}
      </button>
    );
  }
);

Button.displayName = "Button";
```

### spec.json

```json
{
  "name": "Button",
  "description": "Primary action component with multiple variants and sizes",
  "semi_equivalent": "@douyinfe/semi-ui/button",
  "tokens_used": [
    "--semi-color-primary",
    "--semi-color-tertiary",
    "--semi-border-radius-medium",
    "--semi-font-family-regular"
  ],
  "variants": ["primary", "secondary", "outline", "ghost", "danger"],
  "sizes": ["sm", "md", "lg"],
  "states": ["default", "hover", "active", "focus", "disabled", "loading"],
  "priority": 1,
  "complexity": "low"
}
```

## Generator Implementation

```python
class TemplateGenerator:
    """Generate components by injecting tokens into pre-built templates."""
    
    TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "components"
    
    def __init__(self, tokens: Dict[str, str], framework: str = "react"):
        self.tokens = tokens
        self.framework = framework
    
    def generate(self, component: str) -> str:
        """Generate component code from template + tokens."""
        tmpl_file = self.TEMPLATE_DIR / component / f"{self.framework}.tsx.tmpl"
        
        if not tmpl_file.exists():
            raise ValueError(f"No template for {component}/{self.framework}")
        
        template = tmpl_file.read_text()
        
        # Inject tokens
        for token_name, token_value in self.tokens.items():
            template = template.replace(f"{{{{{token_name}}}}}", token_value)
        
        return template
    
    def generate_all(self, output_dir: Path):
        """Generate all available components."""
        for component_dir in sorted(self.TEMPLATE_DIR.iterdir()):
            if component_dir.is_dir() and not component_dir.name.startswith("_"):
                try:
                    code = self.generate(component_dir.name)
                    out = output_dir / component_dir.name
                    out.mkdir(parents=True, exist_ok=True)
                    (out / f"component.tsx").write_text(code)
                    
                    # Copy index.ts
                    index_code = f'export {{ {component_dir.name.title()} }} from "./component";\n'
                    (out / "index.ts").write_text(index_code)
                except Exception as e:
                    print(f"[WARN] Skipping {component_dir.name}: {e}")
```

## Component Priority List

| Priority | Component | Tokens Used |
|----------|-----------|-------------|
| 1 | Button | primary, border-radius, font |
| 2 | Input | text, border, focus-border, radius |
| 3 | Card | bg, shadow, radius |
| 4 | Tag/Badge | semantic colors, radius |
| 5 | Avatar | primary, radius-circle |
| 6 | Alert/Banner | semantic colors, radius |
| 7 | Typography | font-family, sizes, weights, text-colors |
| 8 | Divider | border-color |
| 9 | Tooltip | bg, text, shadow, radius |
| 10 | Dropdown | bg, shadow, border |
| 11 | Select | same as Input + Dropdown |
| 12 | Checkbox | primary, border |
| 13 | Radio | primary, border |
| 14 | Switch | primary, bg |
| 15 | Table | text, border, bg alternating |
| 16 | Modal | bg, shadow, overlay |
| 17 | Tabs | primary, text, border |
| 18 | Breadcrumb | text, link |
| 19 | Pagination | primary, border, text |
| 20 | Progress | primary, bg-track |
| 21 | Skeleton | fill, radius |
| 22 | Empty | text-muted |

## Acceptance Criteria

- [ ] 22 template files created and pass TSC compilation
- [ ] Generator replaces tokens correctly
- [ ] Each component renders correctly in a test React app
- [ ] Storybook stories for each component
- [ ] `generate_all()` produces working component library
