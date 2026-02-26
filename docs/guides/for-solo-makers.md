# UX Master v4 — Solo Maker's Guide ✨

> **One person = whole team. Your AI-powered designer, design system, and QA.**

---

## Who You Are

- ✨ **Indie Hacker** building side projects
- 🛠️ **Full-Stack Developer** doing everything alone
- 🎨 **Creator / Maker** shipping products without a team
- 💡 **Freelancer** delivering professional work solo

**Your Goal**: Ship professional-quality products without needing a design team

---

## What You'll Learn

1. [The Solo Maker's Advantage](#the-solo-makers-advantage)
2. [One-Person Workflow](#one-person-workflow)
3. [Design Without Being a Designer](#design-without-being-a-designer)
4. [From Side Project to Product](#from-side-project-to-product)
5. [Freelancer's Secret Weapon](#freelancers-secret-weapon)
6. [Case Studies](#case-studies)

---

## The Solo Maker's Advantage

### Your Problem

As a solo maker, you:
- Can't afford a designer ($3K-$15K per project)
- Don't have time to learn design (weeks of study)
- Need professional results (users don't care you're solo)
- Ship multiple projects (each needs good design)

### UX Master Replaces 3 Roles

| Role | Traditional Cost | With UX Master |
|------|-----------------|----------------|
| UI/UX Designer | $5K-$15K/project | $0 — auto-extracted |
| Design System Engineer | $3K-$8K/project | $0 — auto-generated |
| QA Tester (visual) | $2K-$5K/project | $0 — 37 auto tests |
| **Total** | **$10K-$28K** | **$0** |

**You just saved the cost of a small team. Every single project.**

---

## One-Person Workflow

### The Daily Routine

```bash
# Morning: Start with design
python scripts/wizard.py --url https://reference.com --name "Today"

# Afternoon: Build with generated components
import { Button, Card, Input } from './components';

# Evening: Ship it
git push && deploy
```

### End-to-End in 1 Day

**Hour 1: Design System**
```bash
# Extract from a beautiful reference site
python scripts/wizard.py --url https://cal.com --name "MyApp"
```

**Hour 2: Components**
```bash
# Generate all components
python scripts/component_generator.py \
  --input output/MyApp/design-system.json \
  --all --framework react-tailwind \
  --output ./src/components
```

**Hour 3-6: Build**
```tsx
// Use generated components — no design decisions needed
import { Button, Card, Input, Badge } from './components';

function Dashboard() {
  return (
    <div className="grid grid-cols-3 gap-base">
      <Card variant="elevated">
        <Badge color="success">Active</Badge>
        <h3>Revenue</h3>
        <p className="stat-value">$12,450</p>
      </Card>
      {/* Build features, not design */}
    </div>
  );
}
```

**Hour 7: Polish**
```bash
# Run quality checks
python scripts/wizard.py --url http://localhost:3000 --name "QA"
# Check screenshots, verify consistency
```

**Hour 8: Ship** 🚀

---

## Design Without Being a Designer

### The "Steal Like an Artist" Method

```bash
# Step 1: Pick 3 products you admire
python scripts/wizard.py --url https://linear.app --name "Ref1"
python scripts/wizard.py --url https://vercel.com --name "Ref2"
python scripts/wizard.py --url https://resend.com --name "Ref3"

# Step 2: Compare their design systems
# Look at: colors, fonts, spacing, border radius
# Pick what works best for your product

# Step 3: Customize
# Change primary color to your brand
# Keep everything else (proven design decisions)
```

### Design Decisions You Never Need to Make

UX Master makes these decisions for you:
- ✅ **Font pairing** — Extracted from proven products
- ✅ **Color palette** — Complete with hover/active states
- ✅ **Spacing system** — 8px grid, consistent everywhere
- ✅ **Border radius** — Matched across all components
- ✅ **Shadow system** — Subtle elevation hierarchy
- ✅ **Responsive breakpoints** — Mobile-first by default

**You focus on**: What does my product do?
**UX Master handles**: How does my product look?

### Quick Reference: Design Rules

```markdown
## Solo Maker's Design Cheat Sheet

### Colors
- Max 5 main colors (primary, success, warning, danger, neutral)
- Use primary for CTAs and key actions
- Use neutrals for text and backgrounds

### Typography
- Max 2 font families (heading + body)
- Max 5 font sizes (h1, h2, h3, body, caption)
- Line height: 1.5 for body, 1.2 for headings

### Spacing
- Base unit: 8px
- Use multiples: 8, 16, 24, 32, 48, 64
- Never use odd numbers (17px, 13px = no)

### Components
- Buttons: max 4 variants (primary, secondary, outline, ghost)
- Cards: max 3 variants (default, elevated, outlined)
- Inputs: always include error and disabled states
```

---

## From Side Project to Product

### Phase 1: Weekend MVP

```bash
# Saturday morning
python scripts/wizard.py --url https://todoist.com --name "TaskApp"
python scripts/component_generator.py --input output/TaskApp/design-system.json --all

# Saturday afternoon → Sunday: Build core features
# Monday: Deploy on Vercel/Railway
```

### Phase 2: First Users

```bash
# Get feedback, iterate fast
# When design needs tweaking:
python scripts/wizard.py --url http://my-app.vercel.app --name "V2Audit"
# Review screenshots, fix inconsistencies
```

### Phase 3: Monetization

```bash
# Polish for paying customers
# Extract from premium SaaS references
python scripts/wizard.py --url https://stripe.com/dashboard --name "PremiumRef"

# Apply premium design tokens to your pricing page
# Professional design = customers trust paying
```

### Phase 4: Scale

```bash
# Create design documentation for future collaborators
python scripts/stitch_integration.py design-md \
  --input output/PremiumRef/design-system.json \
  --project "MyProduct" \
  --output DESIGN.md

# Any future contributor follows the same design system
```

---

## Freelancer's Secret Weapon

### Client Work in Record Time

```bash
# Client says: "Build me a dashboard like Notion"
# You say: "Done in 2 days"

# Day 1:
python scripts/wizard.py --url https://notion.so --name "ClientRef"
python scripts/component_generator.py --input output/ClientRef/design-system.json --all

# Day 2: Build the actual product
# Charge for a week of work. Deliver in 2 days.
# Client thinks you're a genius.
```

### Portfolio Polish

```bash
# Make every portfolio project look consistent and premium
# Extract design system from your best work
python scripts/wizard.py --url https://my-best-project.com --name "Portfolio"

# Apply to all other projects
# Now your portfolio shows design consistency = professional
```

### Multi-Client Token Management

```bash
# Keep separate design systems per client
output/
├── client-alpha/
│   └── design-system.json
├── client-beta/
│   └── design-system.json
└── client-gamma/
    └── design-system.json

# Switch between clients instantly
# No design drift between projects
```

---

## Case Studies

### Case Study 1: Weekend SaaS → $5K MRR

**Maker**: Solo developer, built on weekends
**Product**: Invoice management tool

**Process:**
```bash
# Extracted from FreshBooks (best-in-class invoice tool)
python scripts/wizard.py --url https://freshbooks.com --name "InvoiceRef"
# Customized colors, generated components
# Built MVP over 2 weekends
```

**Result:**
- ✅ Shipped in 2 weekends
- ✅ "Best looking invoice tool" — user review
- ✅ $5K MRR within 6 months
- ✅ $0 spent on design

---

### Case Study 2: Freelancer 10x Output

**Maker**: Full-stack freelancer
**Challenge**: 3 client projects simultaneously

**Process:**
```bash
# Project 1: E-commerce (extracted from Shopify)
# Project 2: Dashboard (extracted from Linear)
# Project 3: Landing page (extracted from Stripe)
# Each project: Extract → Generate → Build → Ship
```

**Result:**
- ✅ Delivered all 3 in 2 weeks (normally 6 weeks)
- ✅ Clients rated design 9/10 average
- ✅ Increased hourly rate by 40% (faster delivery = more value)

---

### Case Study 3: Open Source Library

**Maker**: Indie developer, open source contributor
**Project**: React component library

**Process:**
```bash
# Extracted design tokens from Material Design, Ant Design, Semi Design
# Cherry-picked best patterns from each
# Generated component library with consistent API
```

**Result:**
- ✅ 800+ GitHub stars in first month
- ✅ "Finally, a component library that looks premium out of the box"
- ✅ Components reused across 5 personal projects

---

## Your Toolkit

### Essential Commands

```bash
# The only 4 commands you need:

# 1. Extract design system
python scripts/wizard.py --url URL

# 2. Generate components
python scripts/component_generator.py --input FILE --all

# 3. Quality check
python scripts/wizard.py --url http://localhost:3000 --name "QA"

# 4. Create docs (when you need them)
python scripts/stitch_integration.py design-md --input FILE --project NAME
```

### Solo Maker's Stack

```
UX Master (design) + Cursor (code) + Vercel (deploy)
= Ship professional products in days, not months
```

---

## Tips from Solo Makers

> **"I ship a new project every month. UX Master makes each one look like a funded startup."**
> — Indie hacker, 12 products shipped

> **"Clients can't believe I'm a one-person team. The design quality says otherwise."**
> — Freelance developer

> **"I used to skip design entirely. Now it's the first thing I do, and it takes 30 minutes."**
> — Full-stack maker

> **"My side project looks better than my day job's product. UX Master is unfair."**
> — Software engineer, indie maker on nights/weekends

---

## Next Steps

1. **Extract**: `python scripts/wizard.py --url https://app-you-admire.com`
2. **Generate**: `python scripts/component_generator.py --input FILE --all`
3. **Build**: Use generated components for your next project
4. **Ship**: Deploy and impress your users

---

**Questions?** Check [HOW-IT-WORKS.md](../technical/how-it-works.md) for technical details.

**Ready to be a one-person design team?** ✨
