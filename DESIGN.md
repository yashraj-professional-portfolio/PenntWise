---
name: Equilibrium Finance
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#434655'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#737686'
  outline-variant: '#c3c6d7'
  surface-tint: '#0053db'
  primary: '#004ac6'
  on-primary: '#ffffff'
  primary-container: '#2563eb'
  on-primary-container: '#eeefff'
  inverse-primary: '#b4c5ff'
  secondary: '#006c49'
  on-secondary: '#ffffff'
  secondary-container: '#6cf8bb'
  on-secondary-container: '#00714d'
  tertiary: '#784b00'
  on-tertiary: '#ffffff'
  tertiary-container: '#996100'
  on-tertiary-container: '#ffeedd'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dbe1ff'
  primary-fixed-dim: '#b4c5ff'
  on-primary-fixed: '#00174b'
  on-primary-fixed-variant: '#003ea8'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '800'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Work Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Work Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-caps:
    fontFamily: Work Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1'
    letterSpacing: 0.05em
  data-mono:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  container-padding-mobile: 16px
  container-padding-desktop: 40px
  gutter: 24px
  card-gap: 24px
  section-margin: 48px
---

## Brand & Style

The design system is built on the pillars of **clarity, agency, and optimism**. Designed for students and young professionals, it moves away from the intimidating, dense aesthetics of traditional banking toward a modern, accessible interface that treats financial management as a wellness practice rather than a chore.

The style is **Modern / Minimalist** with subtle **Tonal Layering**. It prioritizes heavy whitespace to reduce "math anxiety" and utilizes a clear hierarchy to highlight the most important data points—disposable income, upcoming bills, and savings goals. The interface should feel organized and lightweight, using soft shadows and refined borders to define the modular, card-based structure.

## Colors

This design system utilizes a semantic color palette to provide instant cognitive feedback on financial health:

*   **Primary (Trust Blue):** Used for main actions, navigation, and neutral account balances. It evokes stability and professionalism.
*   **Success (Growth Green):** Reserved exclusively for income, savings progress, and positive net cash flow.
*   **Warning (Alert Amber):** Used for approaching budget limits or upcoming due dates.
*   **Critical (Over-budget Red):** Used for exceeded budgets, late payments, or negative balances.
*   **Neutral (Slate):** A range of cool grays used for secondary text, borders, and UI scaffolding to keep the focus on the colorful data indicators.

The default mode is **Light**, providing a clean, paper-like canvas that feels studious and transparent.

## Typography

The typography strategy balances modern personality with functional data density. 

1.  **Manrope** is used for headlines and primary totals. Its geometric yet friendly character makes large currency amounts feel approachable.
2.  **Work Sans** is the workhorse for all body text and UI labels. Its optimized legibility ensures that fine-print transaction details are easy to read.
3.  **JetBrains Mono** is used sparingly for tabular data, transaction lists, and account numbers. The monospaced nature allows for perfect vertical alignment of decimal points in currency columns, making comparison easier for the eye.

Use `display-lg` exclusively for hero balances (e.g., total net worth). Use `label-caps` for table headers and small categories.

## Layout & Spacing

The layout follows a **Fixed-Fluid Hybrid** model. On desktop, the main content area is capped at 1280px with a 12-column grid. On mobile, it switches to a single-column fluid layout.

*   **Generous Margins:** All cards and containers use a minimum of 24px internal padding to ensure data "breathes."
*   **Modular Grid:** Dashboard elements are housed in cards that span 4, 6, or 12 columns.
*   **Vertical Rhythm:** A strict 8px baseline grid is used to maintain consistency between related elements (e.g., a label and its input field are 8px apart, while separate form groups are 24px apart).

## Elevation & Depth

Hierarchy is established through **Tonal Layers** and **Soft Shadows**:

1.  **Level 0 (Background):** Solid `#F8FAFC`. This is the canvas.
2.  **Level 1 (Cards):** White surfaces with a 1px border of `#E2E8F0` and a very soft, diffused shadow (`0px 4px 12px rgba(0,0,0,0.03)`).
3.  **Level 2 (Interactive/Floating):** Used for active dropdowns or modals. These use a more pronounced shadow to indicate they are closer to the user.

Avoid heavy dark shadows. The goal is to make cards feel like they are lightly resting on the background, not floating high above it. Use subtle background tints for "hover" states on list items rather than increasing elevation.

## Shapes

The design system uses **Rounded** geometry (`0.5rem` or `8px` base) to appear friendly and modern. 

*   **Standard Cards/Inputs:** 8px radius.
*   **Large Feature Cards:** 16px radius (`rounded-lg`).
*   **Interactive Elements:** Buttons and Chips use a `rounded-xl` or fully pill-shaped radius to distinguish them from static data containers.
*   **Progress Bars:** Always use pill-shaped (rounded-full) caps for a soft, approachable feel.

## Components

### Buttons
*   **Primary:** Filled Primary Blue with white text. High contrast, rounded-lg.
*   **Secondary:** Ghost style with a Primary Blue border and text.
*   **Success/Danger:** Only used for definitive "Add Income" or "Delete Account" actions.

### Cards
*   The fundamental unit of the UI. Every card must have a clear `headline-md` title.
*   Charts within cards should have a 16px inset from the card border.

### Transaction Tables
*   Rows should have a minimum height of 56px.
*   Use `data-mono` for all numerical values.
*   Alternating row stripes are not necessary; use thin `1px` dividers in `#F1F5F9`.
*   Category icons should be placed in a 32x32px circular background with a desaturated version of the category color.

### Data Entry
*   Inputs use a 1px border. On focus, the border thickens to 2px in Primary Blue with a soft blue outer glow.
*   Labels are always placed above the input, never inside as placeholders only.

### Progress Trackers
*   For budget tracking, use a horizontal bar.
*   The bar background is always a light gray (`#E2E8F0`), with the fill color changing from Success Green to Warning Amber as it approaches 80% capacity.