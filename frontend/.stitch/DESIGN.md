# VintageMap Design Tokens

## Stitch Prompt

```
Mood: Warm, sophisticated, inviting. Like the best page of a wine menu. Not pretentious. "Let me help you find a bottle."
Colors: Warm cream background (#faf5eb). Deep burgundy accent (#722f37). Heatmap: green (great) through amber (average) to muted gray (poor). Map: warm-toned vintage style.
Fonts: Newsreader (headlines), Work Sans (body)
```

## Token Mapping

### Palette (Dark Editorial Mode)

The design uses a warm-dark palette rather than the cream background from the Stitch prompt.
This is intentional: the dark surface makes the map tiles readable and gives wine-menu gravitas.

| Token | Value | Usage |
|---|---|---|
| `--page-bg` | `#171311` | Page background |
| `--surface-low` | `#1e1a17` | Slightly elevated surfaces |
| `--surface-container` | `#252120` | Card backgrounds, containers |
| `--surface-high` | `#2e2926` | Highest elevation surface |
| `--primary` | `#e8ddd0` | Headlines, primary text |
| `--primary-container` | `#3a1a1a` | Button backgrounds, badges |
| `--secondary` | `#d4636f` | Error text, destructive actions |
| `--gold` | `#e9c176` | Star ratings, peak badges |
| `--gold-dim` | `#c5a55a` | Subtle gold accents, borders |
| `--outline` | `#5a4e4c` | Default borders |
| `--outline-variant` | `#3a3230` | Subtle borders, dividers |
| `--on-surface` | `#d5cac0` | Body text |
| `--on-surface-variant` | `#a89a90` | Secondary body text |

### Wine Type Colors

| Token | Value | Usage |
|---|---|---|
| `--wine-red` | `#722F37` | Red wine accent (also primary burgundy from Stitch) |
| `--wine-white` | `#C8A96E` | White wine accent |
| `--wine-rose` | `#E8936A` | Rose wine accent |
| `--wine-sparkling` | `#9DB8C9` | Sparkling wine accent |
| `--wine-white-accent` | `#a07840` | White wine on dark backgrounds |
| `--wine-rose-accent` | `#c26a50` | Rose wine on dark backgrounds |
| `--wine-sparkling-accent` | `#6a8ea8` | Sparkling wine on dark backgrounds |
| `--wine-badge-red` | `#c07080` | Red wine inline badge text |
| `--wine-badge-white` | `#c8a860` | White wine inline badge text |
| `--wine-badge-rose` | `#d08060` | Rose wine inline badge text |
| `--wine-badge-sparkling` | `#7ab0c8` | Sparkling wine inline badge text |

### Heatmap Scale (Vintage Quality)

| Token | Value | Range |
|---|---|---|
| `--heatmap-outstanding` | `#722F37` | 90+ |
| `--heatmap-excellent` | `#A0522D` | 80-89 |
| `--heatmap-good` | `#CD853F` | 70-79 |
| `--heatmap-average` | `#DEB887` | 60-69 |
| `--heatmap-below-avg` | `#D2B48C` | 50-59 |
| `--heatmap-poor` | `#C8B89A` | 1-49 |
| `--heatmap-no-data` | `#AAAAAA` | 0 / no data |

### Semantic Colors

| Token | Value | Usage |
|---|---|---|
| `--color-positive` | `#7aaa7a` | Good state, positive empty states |
| `--color-on-badge` | `#f0e8de` | Light text on colored badges |

### Overlay Backgrounds

| Token | Value | Usage |
|---|---|---|
| `--overlay-bg` | `rgba(30, 26, 23, 0.95)` | Map legend, hints, tooltips |
| `--overlay-bg-strong` | `rgba(30, 26, 23, 0.98)` | Popups, bottom sheets |

### Typography

| Token | Value | Usage |
|---|---|---|
| `--font-heading` | `Newsreader, Georgia, serif` | Headlines, region names, scores |
| `--font-body` | `Work Sans, Segoe UI, sans-serif` | Body text, labels, buttons |

Loaded via Google Fonts: `Newsreader` (ital, opsz, 200-800) and `Work Sans` (300, 400, 500, 600).

## Design Decisions

- **Dark mode over cream:** The Stitch prompt specified `#faf5eb` cream background, but the dark editorial palette was chosen because (1) map tiles are dark-themed CARTO basemaps, (2) the dark surface creates better contrast for the wine bottle markers, and (3) it reads more like an intimate wine cellar than a bright retail page. The warm undertones of the dark palette (`#171311` has warm brown bias) honor the "warm" directive from the Stitch prompt.
- **Burgundy `#722f37` is the keystone:** Used for `--wine-red`, `--heatmap-outstanding`, and region hover states. This is the single most important color in the system.
- **No Tailwind:** All styles are vanilla CSS with CSS custom properties. No utility classes.
- **Heatmap uses warm tones:** Burgundy (outstanding) through amber/tan (average) to muted gray (no data). This avoids traffic-light green/red associations that would clash with the wine palette.
