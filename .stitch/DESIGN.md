# VintageMap Design System

Derived from Stitch exploration. Editorial, warm, wine-book aesthetic.

## Palette

| Token | Hex | Role |
|---|---|---|
| `--page-bg` | `#fbf9f4` | Page canvas (warm cream) |
| `--surface-low` | `#f5f3ee` | Subtle surface (cards, sections) |
| `--surface-container` | `#f0eee9` | Container backgrounds |
| `--surface-high` | `#eae8e3` | Elevated containers |
| `--primary` | `#2a0002` | Deep wine (headings, primary text) |
| `--primary-container` | `#4a0e0e` | Dark wine (buttons, badges) |
| `--secondary` | `#af2b3e` | Red accent (highlights, hover) |
| `--gold` | `#e9c176` | Gold accent (dividers, highlights) |
| `--gold-dim` | `#c5a55a` | Muted gold (borders, labels) |
| `--outline` | `#877270` | Borders, subtle lines |
| `--outline-variant` | `#dac1bf` | Very light borders |
| `--on-surface` | `#1b1c19` | Primary text |
| `--on-surface-variant` | `#544341` | Secondary text |
| `--stone-400` | `#a8a29e` | Muted labels |
| `--stone-500` | `#78716c` | Muted text |

### Wine Type Colors
| Type | Hex |
|---|---|
| Red | `#722F37` |
| White | `#C8A96E` |
| Rose | `#E8936A` |
| Sparkling | `#9DB8C9` |

### Score Tier Colors
| Tier | Hex |
|---|---|
| Outstanding (90+) | `#722F37` |
| Excellent (80-89) | `#A0522D` |
| Good (70-79) | `#CD853F` |
| Average (60-69) | `#DEB887` |

## Typography

| Role | Family | Weight | Style |
|---|---|---|---|
| Display | Newsreader | 700-800 | Normal |
| Headline | Newsreader | 400-600 | Normal or Italic |
| Accent | Newsreader | 400 | Italic |
| Body | Work Sans | 300-400 | Normal |
| Label | Work Sans | 400-600 | Normal, uppercase |

### Scale
- Hero title: 6xl-8xl (3.75-6rem)
- Section heading: 2xl-3xl (1.5-1.875rem)
- Card heading: xl (1.25rem)
- Body: base-sm (0.875-1rem)
- Micro label: 9-11px, uppercase, letter-spacing 0.2-0.3em

## Shapes

- Border radius: 0px (sharp editorial edges on all containers)
- Interactive elements (pills, buttons): 0px
- Exception: score badges (rounded-full for circular display)
- Borders: 1px solid `--outline-variant`, hover to `--gold`
- No box-shadows on cards. Use borders only.

## Patterns

### Section Dividers
- Thin gold line: `w-24 h-px bg-gold`
- Or border-top with `--outline-variant` at 20% opacity

### Metadata Labels
- 9px Work Sans, uppercase, letter-spacing 0.3em, `--stone-400`
- Followed by content in body text

### Hover States
- Cards: border-color transition to gold (300ms)
- Links: color transition to `--secondary`
- Buttons: opacity-90

### Entrance Animations
- Keep existing staggerIn: opacity + translateY(12px) + blur(4px)
- 0.5s cubic-bezier(0.16, 1, 0.3, 1)
- Stagger: 80ms between sections, 50ms between items
