# VintageMap Sprint 4 Plan

## Current State Assessment

**Working well:** Core flow (year input → map + recommendation) is solid. Dark theme, vintage pills, favorites, sharing, Surprise Me all functional. Backend data is rich (20 regions, 54 years each). Skeleton loading states exist. Deploy pipeline works (Docker + Railway).

**Issues found:**
1. **Mobile: Legend overlaps map controls** — map legend covers zoom buttons on small screens
2. **Mobile: Region info popup positioning breaks** — uses absolute pixel coords from click event, goes off-screen on mobile
3. **No loading feedback on vintage pills** — clicking a pill fires search but no visual indicator on the pill itself
4. **CLAUDE.md is stale** — says "no Dockerfile" but Dockerfile exists; says client.ts hardcodes localhost but it doesn't
5. **Saved section colors wrong in dark theme** — `.saved-title` uses `var(--oak)` which is dark brown, invisible on dark bg
6. **Map hint banner clips on mobile** — "Click a region..." overflows on 375px
7. **No meta tags / OG tags** — shared URLs have no preview card (title, description, image)
8. **Featured region cards not clickable** — `pointer-events: none` prevents interaction; they should trigger a search
9. **Error banner uses light theme colors** — red/white error banner clashes with dark theme
10. **Accessibility: no skip-to-content, no aria-live for loading states**
11. **No favicon or app icon** — uses default Vite icon
12. **Year range hardcoded in frontend** — DateInput says 1970-2023 but backend has API for this

## Sprint 4 Tasks (Ranked by Impact)

### Task 1: Fix dark theme color issues (saved section, error banner)
**Files:** `frontend/src/App.css`
**Changes:** Update `.saved-title`, `.saved-year`, `.saved-region` to use cream/light colors. Restyle `.error-banner` for dark theme.
**Validation:** Saved cards and error messages readable on dark background at 375px.

### Task 2: Fix mobile region popup positioning
**Files:** `frontend/src/components/Map/WineMap.tsx`, `frontend/src/components/Map/WineMap.css`
**Changes:** Replace absolute pixel positioning with a fixed bottom-sheet style popup on mobile. Clamp position to viewport on desktop.
**Validation:** Click region on 375px — popup fully visible, dismissible.

### Task 3: Make featured region cards clickable
**Files:** `frontend/src/App.tsx`, `frontend/src/App.css`
**Changes:** Remove `pointer-events: none`, add onClick to trigger search for a representative year for each region, add hover cursor.
**Validation:** Clicking "Bordeaux" card searches a great Bordeaux year.

### Task 4: Fix mobile legend and map hint
**Files:** `frontend/src/components/Map/WineMap.css`
**Changes:** Make legend collapsible on mobile or move to bottom-left. Truncate/wrap map hint on small screens.
**Validation:** Legend doesn't overlap zoom controls at 375px. Hint text doesn't overflow.

### Task 5: Add OG meta tags for link previews
**Files:** `frontend/index.html`
**Changes:** Add og:title, og:description, og:image meta tags for social sharing.
**Validation:** Paste URL in Telegram/iMessage — shows preview card.

### Task 6: Fix error banner for dark theme
**Files:** `frontend/src/App.css`
**Changes:** Dark-themed error banner with appropriate contrast.
**Validation:** Trigger error (search year outside range on slow connection) — readable.

### Task 7: Update CLAUDE.md to reflect current state
**Files:** `CLAUDE.md`
**Changes:** Remove stale deployment notes, update file paths, reflect current features.
**Validation:** New developer can onboard from CLAUDE.md alone.

### Task 8: Add aria-live region for loading/results
**Files:** `frontend/src/App.tsx`
**Changes:** Wrap loading/result area in aria-live="polite" region.
**Validation:** Screen reader announces when results load.

### Task 9: Add wine glass favicon
**Files:** `frontend/index.html`, `frontend/public/`
**Changes:** Replace Vite favicon with wine-themed SVG favicon.
**Validation:** Browser tab shows wine glass icon.

### Task 10: Fetch year range from API instead of hardcoding
**Files:** `frontend/src/components/DateInput/DateInput.tsx`, `frontend/src/App.tsx`
**Changes:** Call `/api/year-range` on mount, pass min/max to DateInput.
**Validation:** If backend range changes, frontend adapts automatically.
