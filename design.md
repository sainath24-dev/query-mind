## Overview

Apple's web presence is a masterclass in **reverent product photography framed by near-invisible UI**. Every page is a stack of edge-to-edge product "tiles" — alternating light and dark canvases, each centered on a hero headline, a one-line tagline, two tiny blue pill CTAs, and an impossibly crisp product render. Nothing competes with the product. Typography is confident but quiet; color is either pure white, an off-white parchment, or a near-black tile; interactive elements are a single, quiet blue.

Density is unusually low even by contemporary SaaS standards. Each tile occupies roughly one viewport, and there is no decorative chrome — no borders, no gradients, no decorative frames, no shadows on headlines. Elevation appears only when a product image rests on a surface (a single soft `rgba(0, 0, 0, 0.22) 3px 5px 30px` drop for visual weight). The result is a catalog that feels more like a museum gallery: the wall disappears and the artifact takes over.

Store and shop surfaces retain the same chassis but switch modes. The product configurator (iPhone 17 Pro, accessories grid) introduces a tight grid of white utility cards at `{rounded.lg}` (18px) radius with a thin border, paired with a persistent thin sub-nav strip. The environment page leans darker and more editorial. Across all five surfaces the typographic system, spacing rhythm, and the single blue accent are consistent — this is one design language expressed at different volumes.

**Key Characteristics:**
- Photography-first presentation; UI recedes so the product can speak.
- Alternating full-bleed tile sections: white/parchment ↔ near-black, with the color change itself acting as the section divider.
- Single blue accent (`{colors.primary}` — #0066cc) carries every interactive element. No second brand color exists.
- Two button grammars: tiny blue pill CTAs (`{rounded.pill}`) and compact utility rects (`{rounded.sm}`).
- SF Pro Display + SF Pro Text — negative letter-spacing at display sizes for the signature "Apple tight" headline feel.
- Whisper-soft elevation used only when a product image needs to breathe — exactly one drop-shadow in the entire system.
- Tight two-row nav: slim `{component.global-nav}` + product-specific `{component.sub-nav-frosted}` with persistent right-aligned primary CTA.
- Section rhythm across multiple pages: light hero → dark product tile → light utility tile → dark tile → parchment footer — a predictable pulse.

## Colors

### Brand & Accent
- **Action Blue** (`{colors.primary}` — #0066cc): The single brand-level interactive color. All text links, all blue pill CTAs ("Learn more", "Buy"), and the focus ring root.
- **Focus Blue** (`{colors.primary-focus}` — #0071e3): Focus ring on buttons (`outline: 2px solid`).
- **Sky Link Blue** (`{colors.primary-on-dark}` — #2997ff): Brighter blue used on dark surfaces for in-copy links and inline callouts.

### Surface
- **Pure White** (`{colors.canvas}` — #ffffff): The dominant canvas. Content, utility cards.
- **Parchment** (`{colors.canvas-parchment}` — #f5f5f7): Signature Apple off-white. Light tiles, footer, chat background.
- **Pearl Button** (`{colors.surface-pearl}` — #fafafc): Fill for secondary ghost buttons.
- **Near-Black Tile 1** (`{colors.surface-tile-1}` — #272729): Primary dark tile, code editor/SQL block.
- **Near-Black Tile 2** (`{colors.surface-tile-2}` — #2a2a2c).
- **Near-Black Tile 3** (`{colors.surface-tile-3}` — #252527).
- **Pure Black** (`{colors.surface-black}` — #000000): Global nav bar background.
- **Translucent Chip Gray** (`{colors.surface-chip-translucent}` — #d2d2d7): Circular control buttons, ~64% alpha.

### Text
- **Near-Black Ink** (`{colors.ink}` — #1d1d1f): Headlines, body text.
- **Body** (`{colors.body}` — #1d1d1f).
- **Body On Dark** (`{colors.body-on-dark}` — #ffffff).
- **Body Muted** (`{colors.body-muted}` — #cccccc).
- **Ink Muted 80** (`{colors.ink-muted-80}` — #333333).
- **Ink Muted 48** (`{colors.ink-muted-48}` — #7a7a7a).

### Hairlines & Borders
- **Divider Soft** (`{colors.divider-soft}` — #f0f0f0): Subtle separation.
- **Hairline** (`{colors.hairline}` — #e0e0e0): 1px hairline border on utility cards.

### Brand Gradient
**No decorative gradients.** Clean, authentic surfaces.

## Typography
- **Display**: `SF Pro Display, system-ui, -apple-system, sans-serif`
- **Body / UI**: `SF Pro Text, system-ui, -apple-system, sans-serif`
- **Hero headline**: 56px, weight 600, line-height 1.07, tracking -0.28px
- **Tile headline**: 40px, weight 600, line-height 1.10
- **Body**: 17px, weight 400, line-height 1.47, tracking -0.374px
- **Button utility / caption**: 14px, weight 400/600

## Shapes
- `{rounded.none}`: 0px
- `{rounded.sm}`: 8px
- `{rounded.md}`: 11px
- `{rounded.lg}`: 18px (cards)
- `{rounded.pill}`: 9999px (pill buttons, input bars)

