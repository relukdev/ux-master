# Semi Design Token Specification

Complete reference for all ~200 CSS variables in the Semi Design token system. Source: `DouyinFE/semi-design/packages/semi-theme-default/scss/global.scss`.

## Table of Contents

1. [Brand Colors](#brand-colors)
2. [Semantic Colors](#semantic-colors)
3. [Background Colors](#background-colors)
4. [Fill Colors](#fill-colors)
5. [Text Colors](#text-colors)
6. [Border Colors](#border-colors)
7. [Link Colors](#link-colors)
8. [Disabled Colors](#disabled-colors)
9. [Special Colors](#special-colors)
10. [Typography](#typography)
11. [Spacing](#spacing)
12. [Border & Radius](#border--radius)
13. [Shadows](#shadows)
14. [Sizing](#sizing)
15. [Dark Mode Strategy](#dark-mode-strategy)

---

## Brand Colors

Each brand color has 7 state variants:

```css
/* Primary — Main brand/action color */
--semi-color-primary                  /* Base: e.g. #0F79F3 */
--semi-color-primary-hover            /* darken(base, 10%) */
--semi-color-primary-active           /* darken(base, 20%) */
--semi-color-primary-disabled         /* lighten(base, 60%) */
--semi-color-primary-light-default    /* lighten(base, 88%) — light bg */
--semi-color-primary-light-hover      /* lighten(base, 82%) */
--semi-color-primary-light-active     /* lighten(base, 75%) */

/* Secondary — Same pattern ×7 */
--semi-color-secondary
--semi-color-secondary-hover
--semi-color-secondary-active
--semi-color-secondary-disabled
--semi-color-secondary-light-default
--semi-color-secondary-light-hover
--semi-color-secondary-light-active

/* Tertiary — Same pattern ×7 */
--semi-color-tertiary
--semi-color-tertiary-hover
--semi-color-tertiary-active
--semi-color-tertiary-disabled
--semi-color-tertiary-light-default
--semi-color-tertiary-light-hover
--semi-color-tertiary-light-active
```

**Derivation formula:**
```python
hover    = darken(base, 0.10)   # Multiply RGB by 0.9
active   = darken(base, 0.20)   # Multiply RGB by 0.8
disabled = lighten(base, 0.60)  # Blend 60% toward white
light-default = lighten(base, 0.88)
light-hover   = lighten(base, 0.82)
light-active  = lighten(base, 0.75)
```

---

## Semantic Colors

Each semantic color follows the same 7-state pattern as brand colors:

```css
/* Success — Green tones */
--semi-color-success                  /* e.g. #00B69B */
--semi-color-success-hover
--semi-color-success-active
--semi-color-success-disabled
--semi-color-success-light-default
--semi-color-success-light-hover
--semi-color-success-light-active

/* Warning — Orange/yellow tones */
--semi-color-warning                  /* e.g. #F59E0B */
/* ... ×7 */

/* Danger — Red tones */
--semi-color-danger                   /* e.g. #EF4444 */
/* ... ×7 */

/* Info — Blue/cyan tones */
--semi-color-info                     /* e.g. #3B82F6 */
/* ... ×7 */
```

---

## Background Colors

5 levels from page background to elevated surfaces:

```css
--semi-color-bg-0    /* Page background (lightest in light mode) — e.g. #FFFFFF */
--semi-color-bg-1    /* Card/container background — e.g. #FFFFFF */
--semi-color-bg-2    /* Nested container — e.g. #F9FAFB */
--semi-color-bg-3    /* Header/sidebar — e.g. #F3F4F6 */
--semi-color-bg-4    /* Elevated surface — e.g. #E5E7EB */
```

---

## Fill Colors

3 levels for subtle interactive backgrounds (hover states, selected items):

```css
--semi-color-fill-0  /* Lightest — 5% opacity of neutral — e.g. rgba(0,0,0,0.05) */
--semi-color-fill-1  /* Medium — 10% opacity — e.g. rgba(0,0,0,0.10) */
--semi-color-fill-2  /* Strongest — 15% opacity — e.g. rgba(0,0,0,0.15) */
```

---

## Text Colors

4 levels from primary (headings) to disabled:

```css
--semi-color-text-0  /* Primary text: headings, important content — e.g. #1C1F23 (darkest) */
--semi-color-text-1  /* Secondary text: body content — e.g. #475569 */
--semi-color-text-2  /* Tertiary text: descriptions, captions — e.g. #919AA3 */
--semi-color-text-3  /* Disabled/placeholder text — e.g. #C0C4CC (lightest) */
```

**Rule**: text-0 must always be the darkest, text-3 the lightest. If extraction inverts these, swap the values.

---

## Border Colors

```css
--semi-color-border        /* Default border — e.g. #E5E7EB */
--semi-color-focus-border  /* Focus ring color — usually primary or blue */
```

---

## Link Colors

```css
--semi-color-link          /* Default link — e.g. primary color */
--semi-color-link-hover    /* Hover — darken(link, 10%) */
--semi-color-link-active   /* Active — darken(link, 20%) */
--semi-color-link-visited  /* Visited — desaturated variant */
```

---

## Disabled Colors

```css
--semi-color-disabled-bg      /* Disabled background — e.g. #F5F5F5 */
--semi-color-disabled-text    /* Disabled text — e.g. #C0C4CC */
--semi-color-disabled-border  /* Disabled border — e.g. #E5E7EB */
--semi-color-disabled-fill    /* Disabled fill — e.g. #F5F5F5 */
```

---

## Special Colors

```css
--semi-color-white        /* Always #FFFFFF */
--semi-color-black        /* Always #000000 */
--semi-color-overlay-bg   /* Modal overlay — e.g. rgba(0,0,0,0.6) */
--semi-color-nav-bg       /* Navigation background */
--semi-color-shadow        /* Shadow base color — e.g. rgba(0,0,0,0.1) */
--semi-color-highlight-bg  /* Search/text highlight — e.g. rgba(primary, 0.15) */
```

---

## Typography

```css
/* Font Families */
--semi-font-family-regular  /* Body: e.g. "Inter", -apple-system, sans-serif */
--semi-font-family-light    /* Light weight family (if different from regular) */
--semi-font-family-bold     /* Bold weight family (if different from regular) */

/* Font Sizes */
--semi-font-size-extra-small   /* 12px */
--semi-font-size-small         /* 12px */
--semi-font-size-regular       /* 14px */
--semi-font-size-header-6      /* 16px */
--semi-font-size-header-5      /* 18px */
--semi-font-size-header-4      /* 20px */
--semi-font-size-header-3      /* 24px */
--semi-font-size-header-2      /* 28px */
--semi-font-size-header-1      /* 32px */

/* Font Weights */
--semi-font-weight-light       /* 200 */
--semi-font-weight-regular     /* 400 */
--semi-font-weight-semibold    /* 600 */
--semi-font-weight-bold        /* 700 */

/* Line Heights */
--semi-line-height-regular     /* 1.5 */
--semi-line-height-loose       /* 1.7 */
```

---

## Spacing

Named scale from none to super-loose:

```css
--semi-spacing-none            /* 0px */
--semi-spacing-super-tight     /* 2px */
--semi-spacing-extra-tight     /* 4px */
--semi-spacing-tight           /* 8px */
--semi-spacing-base-tight      /* 12px */
--semi-spacing-base            /* 16px */
--semi-spacing-base-loose      /* 20px */
--semi-spacing-loose           /* 24px */
--semi-spacing-extra-loose     /* 32px */
--semi-spacing-super-loose     /* 40px */
```

---

## Border & Radius

```css
/* Border Radius */
--semi-border-radius-extra-small  /* 3px */
--semi-border-radius-small        /* 3px */
--semi-border-radius-medium       /* 6px */
--semi-border-radius-large        /* 12px */
--semi-border-radius-full         /* 9999px (pill shape) */
--semi-border-radius-circle       /* 50% (perfect circle) */

/* Border Thickness */
--semi-border-thickness               /* 0px (no borders by default) */
--semi-border-thickness-control       /* 1px (input/button borders) */
--semi-border-thickness-control-focus /* 2px (focus state borders) */
```

---

## Shadows

3 elevation levels:

```css
--semi-shadow-sm        /* Subtle: 0 0 1px rgba(0,0,0,0.1) */
--semi-shadow-elevated  /* Medium: 0 0 1px rgba(0,0,0,0.3), 0 4px 14px rgba(0,0,0,0.1) */
--semi-shadow-lg        /* Large:  0 0 1px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.12) */
```

---

## Sizing

Control element heights and icon sizes:

```css
/* Control Heights */
--semi-height-control-small    /* 24px */
--semi-height-control-default  /* 32px */
--semi-height-control-large    /* 40px */

/* Icon Sizes */
--semi-width-icon-extra-small  /* 8px */
--semi-width-icon-small        /* 12px */
--semi-width-icon-medium       /* 16px */
--semi-width-icon-large        /* 20px */
--semi-width-icon-extra-large  /* 24px */
```

---

## Dark Mode Strategy

Semi Design uses CSS variable switching — no class-based approach:

```css
/* Light mode (default) */
:root {
  --semi-color-bg-0: #FFFFFF;
  --semi-color-bg-1: #FFFFFF;
  --semi-color-text-0: #1C1F23;
  --semi-color-text-1: #475569;
  --semi-color-border: #E5E7EB;
  --semi-color-fill-0: rgba(0, 0, 0, 0.05);
}

/* Dark mode */
body[theme-mode="dark"] {
  --semi-color-bg-0: #16161A;
  --semi-color-bg-1: #1E1E22;
  --semi-color-text-0: #F9F9F9;
  --semi-color-text-1: #EEEEEE;
  --semi-color-border: #3E3E44;
  --semi-color-fill-0: rgba(255, 255, 255, 0.08);
}
```

When generating dark mode tokens:
- Invert background levels (bg-0 becomes darkest)
- Invert text levels (text-0 becomes lightest)
- Keep brand/semantic colors the same (or slightly desaturate)
- Adjust fill opacities for dark backgrounds
