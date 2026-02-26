# Semi Design Reference — Token Specification

## Source

Official Semi Design token spec from:
- GitHub: https://github.com/DouyinFE/semi-design
- Token file: `packages/semi-theme-default/scss/global.scss`
- Doc: https://semi.design/en-US/basic/tokens

## Complete Token List

### Color System (~70 variables)

```scss
// Brand Colors
--semi-color-primary                  // Main brand color
--semi-color-primary-hover            // Hover state (-10% luminance)
--semi-color-primary-active           // Active/pressed (-20% luminance)
--semi-color-primary-disabled         // Disabled (50% opacity)
--semi-color-primary-light-default    // Light variant bg
--semi-color-primary-light-hover      // Light variant hover
--semi-color-primary-light-active     // Light variant active

--semi-color-secondary               // Same pattern ×7
--semi-color-tertiary                // Same pattern ×7

// Semantic Colors (each ×7 states)
--semi-color-success
--semi-color-warning
--semi-color-danger
--semi-color-info

// Background (5 levels)
--semi-color-bg-0                    // Page background (darkest in dark mode)
--semi-color-bg-1                    // Card/container background
--semi-color-bg-2                    // Nested container
--semi-color-bg-3                    // Header/sidebar
--semi-color-bg-4                    // Elevated surface

// Fill (3 levels — subtle backgrounds for hover/selected)
--semi-color-fill-0                  // Lightest (5% opacity)
--semi-color-fill-1                  // Medium (10% opacity)
--semi-color-fill-2                  // Strongest (15% opacity)

// Text (4 levels)
--semi-color-text-0                  // Primary text (headings)
--semi-color-text-1                  // Secondary text (body)
--semi-color-text-2                  // Tertiary (descriptions)
--semi-color-text-3                  // Disabled/placeholder

// Border
--semi-color-border                  // Default border
--semi-color-focus-border            // Focus ring color

// Disabled
--semi-color-disabled-bg
--semi-color-disabled-text
--semi-color-disabled-border
--semi-color-disabled-fill

// Link
--semi-color-link
--semi-color-link-hover
--semi-color-link-active
--semi-color-link-visited

// Special
--semi-color-white
--semi-color-black
--semi-color-overlay-bg              // Modal overlay
--semi-color-nav-bg                  // Navigation background
--semi-color-shadow                  // Shadow base color
--semi-color-highlight-bg            // Search highlight
```

### Typography (~15 variables)

```scss
--semi-font-family-regular           // Body font
--semi-font-family-light             // Light weight family (if different)
--semi-font-family-bold              // Bold weight family (if different)

--semi-font-size-extra-small         // 12px
--semi-font-size-small               // 12px
--semi-font-size-regular             // 14px
--semi-font-size-header-6            // 16px
--semi-font-size-header-5            // 18px
--semi-font-size-header-4            // 20px
--semi-font-size-header-3            // 24px
--semi-font-size-header-2            // 28px
--semi-font-size-header-1            // 32px

--semi-font-weight-light             // 200
--semi-font-weight-regular           // 400
--semi-font-weight-semibold          // 600
--semi-font-weight-bold              // 700

--semi-line-height-regular           // 1.5
--semi-line-height-loose             // 1.7
```

### Spacing (~10 variables)

```scss
--semi-spacing-none                  // 0
--semi-spacing-super-tight           // 2px
--semi-spacing-extra-tight           // 4px
--semi-spacing-tight                 // 8px
--semi-spacing-base-tight            // 12px
--semi-spacing-base                  // 16px
--semi-spacing-base-loose            // 20px
--semi-spacing-loose                 // 24px
--semi-spacing-extra-loose           // 32px
--semi-spacing-super-loose           // 40px
```

### Border & Radius (~10 variables)

```scss
--semi-border-radius-extra-small     // 3px
--semi-border-radius-small           // 3px
--semi-border-radius-medium          // 6px
--semi-border-radius-large           // 12px
--semi-border-radius-full            // 9999px
--semi-border-radius-circle          // 50%

--semi-border-thickness              // 0 (no borders by default)
--semi-border-thickness-control      // 1px
--semi-border-thickness-control-focus // 2px
```

### Shadows (~3 variables)

```scss
--semi-shadow-sm                     // 0 0 1px rgba(0,0,0,0.1)
--semi-shadow-elevated               // 0 0 1px rgba(0,0,0,0.3), 0 4px 14px rgba(0,0,0,0.1)
--semi-shadow-lg                     // 0 0 1px rgba(0,0,0,0.3), 0 8px 24px rgba(0,0,0,0.12)
```

### Sizing (~8 variables)

```scss
--semi-height-control-small          // 24px
--semi-height-control-default        // 32px
--semi-height-control-large          // 40px

--semi-width-icon-extra-small        // 8px
--semi-width-icon-small              // 12px
--semi-width-icon-medium             // 16px
--semi-width-icon-large              // 20px
--semi-width-icon-extra-large        // 24px
```

## Semi Design Component List (60+)

### Basic
- Typography, Icon, Button, Divider, Grid, Layout, Space

### Input
- Input, InputNumber, AutoComplete, Cascader, Checkbox, ColorPicker,
  DatePicker, Form, Radio, Rating, Select, Slider, Switch, TagInput,
  TextArea, TimePicker, Transfer, TreeSelect, Upload

### Navigation
- Anchor, Breadcrumb, Navigation, Pagination, Steps, Tabs, Tree

### Display
- Avatar, Badge, Calendar, Card, Carousel, Collapse, Descriptions,
  Dropdown, Empty, Image, List, Modal, OverflowList, Popover,
  ScrollList, SideSheet, Table, Tag, Timeline, Tooltip, Typography

### Feedback
- Banner, Modal, Notification, Popconfirm, Progress, Skeleton, Spin, Toast

## Semi Design Foundation/Adapter Pattern

```
Component Architecture:
├── Foundation (framework-agnostic)
│   ├── buttonFoundation.ts      # State management, event handling
│   └── constants.ts             # Token references
└── Adapter (framework-specific)
    ├── Button.tsx               # React rendering
    └── ButtonAdapter.ts         # React ↔ Foundation bridge
```

Key insight: Foundation handles all logic, Adapter handles rendering.
This allows the same logic to work across React, Vue, Web Components.

## Dark Mode Strategy

Semi uses CSS variable switching:
```css
/* Light (default) */
:root {
  --semi-color-bg-0: #FFFFFF;
  --semi-color-text-0: #1C1F23;
}

/* Dark */
body[theme-mode="dark"] {
  --semi-color-bg-0: #16161A;
  --semi-color-text-0: #F9F9F9;
}
```

No class-based switching — pure CSS variable override.
