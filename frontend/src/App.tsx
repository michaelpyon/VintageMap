import { useState, useCallback, useEffect, useRef } from "react";
import DateInput from "./components/DateInput/DateInput";
import type { DateInputHandle } from "./components/DateInput/DateInput";
import WineMap from "./components/Map/WineMap";
import RecommendationCard from "./components/Recommendation/RecommendationCard";
import { fetchRegionsGeoJSON, fetchRecommendation } from "./api/client";
import type { RecommendationResponse } from "./types";
import "./App.css";

// ── localStorage Favorites ──────────────────────────
interface SavedVintage {
  year: number;
  region_name: string;
  wine_style: string;
  score: number;
  recommendation_text: string;
}

const STORAGE_KEY = "vintagemap_saved";

function loadSaved(): SavedVintage[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
  } catch {
    return [];
  }
}

function saveFavorites(items: SavedVintage[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items));
}

function isSaved(saved: SavedVintage[], year: number, region: string): boolean {
  return saved.some((s) => s.year === year && s.region_name === region);
}

// ── Surprise Me ─────────────────────────────────────
const GREAT_VINTAGES = [1945, 1961, 1966, 1970, 1975, 1978, 1982, 1985, 1989, 1990, 1996, 2000, 2005, 2009, 2010, 2012, 2015, 2016, 2019, 2020];

// Wine type categories for color coding
type WineType = "red" | "white" | "rosé" | "sparkling";

const FEATURED_REGIONS: {
  name: string;
  flag: string;
  style: string;
  country: string;
  score: number;
  type: WineType;
}[] = [
  { name: "Bordeaux", flag: "🇫🇷", style: "Cabernet Blend", country: "France", score: 96, type: "red" },
  { name: "Burgundy", flag: "🇫🇷", style: "Pinot Noir", country: "France", score: 98, type: "red" },
  { name: "Napa Valley", flag: "🇺🇸", style: "Cabernet Sauvignon", country: "USA", score: 95, type: "red" },
  { name: "Tuscany", flag: "🇮🇹", style: "Sangiovese", country: "Italy", score: 94, type: "red" },
  { name: "Barossa Valley", flag: "🇦🇺", style: "Shiraz", country: "Australia", score: 93, type: "red" },
  { name: "Rioja", flag: "🇪🇸", style: "Tempranillo", country: "Spain", score: 91, type: "red" },
];

const SUGGESTED_VINTAGES = [
  { year: 2016, label: "2016 Bordeaux", hint: "Legendary vintage" },
  { year: 2010, label: "2010 Burgundy", hint: "Exceptional" },
  { year: 2019, label: "2019 Napa", hint: "Outstanding" },
  { year: 1990, label: "1990 Barolo", hint: "Historic" },
  { year: 1982, label: "1982 Bordeaux", hint: "Iconic" },
  { year: 2015, label: "2015 Rhône", hint: "Near perfect" },
];

const HOW_IT_WORKS = [
  { icon: "📅", step: "1", title: "Pick a Year", desc: "Enter any year from 1970–2023" },
  { icon: "🗺️", step: "2", title: "See the Map", desc: "Explore vintage quality by region" },
  { icon: "🍷", step: "3", title: "Find Your Wine", desc: "Get a personalised recommendation" },
];

function App() {
  const [geojson, setGeojson] = useState<GeoJSON.FeatureCollection | null>(null);
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeYear, setActiveYear] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fading, setFading] = useState(false);
  const [animKey, setAnimKey] = useState(0);
  const abortRef = useRef<AbortController | null>(null);
  const dateInputRef = useRef<DateInputHandle>(null);

  const [copied, setCopied] = useState(false);

  // Favorites
  const [saved, setSaved] = useState<SavedVintage[]>(loadSaved);

  const toggleSave = useCallback(() => {
    if (!recommendation?.primary || !activeYear) return;
    const r = recommendation.primary;
    setSaved((prev) => {
      const exists = isSaved(prev, activeYear, r.region_name);
      const next = exists
        ? prev.filter((s) => !(s.year === activeYear && s.region_name === r.region_name))
        : [...prev, { year: activeYear, region_name: r.region_name, wine_style: r.wine_style, score: r.score, recommendation_text: r.recommendation_text }];
      saveFavorites(next);
      return next;
    });
  }, [recommendation, activeYear]);

  const removeSaved = useCallback((year: number, region: string) => {
    setSaved((prev) => {
      const next = prev.filter((s) => !(s.year === year && s.region_name === region));
      saveFavorites(next);
      return next;
    });
  }, []);

  const clearAllSaved = useCallback(() => {
    setSaved([]);
    saveFavorites([]);
  }, []);

  // Surprise Me
  const handleSurprise = useCallback(() => {
    const year = GREAT_VINTAGES[Math.floor(Math.random() * GREAT_VINTAGES.length)];
    dateInputRef.current?.setYearAndSubmit(year);
  }, []);

  // Scroll to map when data loads
  useEffect(() => {
    if (geojson) {
      document.getElementById("map-section")?.scrollIntoView({ behavior: "smooth" });
    }
  }, [geojson]);

  const handleSubmit = useCallback(async (year: number, significance: string) => {
    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;

    // Start fade-out of existing content
    setFading(true);
    setLoading(true);
    setError(null);
    setActiveYear(year);

    // After 150ms fade-out, clear old data
    setTimeout(() => {
      setGeojson(null);
      setRecommendation(null);
      setFading(false);
    }, 150);

    try {
      const [geo, rec] = await Promise.all([
        fetchRegionsGeoJSON(year, controller.signal),
        fetchRecommendation(year, significance, controller.signal),
      ]);
      setGeojson(geo);
      setRecommendation(rec);
      setAnimKey((k) => k + 1); // trigger re-animation
      history.replaceState({}, "", `?year=${year}`);
    } catch (e) {
      if (e instanceof Error && e.name === "AbortError") return;
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Auto-search from URL param on mount
  useEffect(() => {
    const yearParam = new URLSearchParams(window.location.search).get("year");
    if (yearParam) {
      const y = parseInt(yearParam, 10);
      if (!isNaN(y) && y >= 1970 && y <= 2023) {
        handleSubmit(y, "gift");
      }
    }
  }, [handleSubmit]);

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <div className="hero-badge">✦ Wine Vintage Explorer ✦</div>
          <h1 className="hero-title">VintageMap</h1>
          <p className="hero-subtitle">
            Every great wine tells the story of its year. Enter a date that
            matters to you — we'll find the perfect vintage.
          </p>
          <div className="suggested-vintages">
            {SUGGESTED_VINTAGES.map((v) => (
              <button
                key={v.year}
                className="vintage-pill"
                onClick={() => handleSubmit(v.year, "gift")}
              >
                <span className="vintage-pill-label">{v.label}</span>
                <span className="vintage-pill-hint">{v.hint}</span>
              </button>
            ))}
          </div>
          <DateInput ref={dateInputRef} onSubmit={handleSubmit} loading={loading} />
          <button
            type="button"
            className="surprise-btn"
            onClick={handleSurprise}
            disabled={loading}
            title="Try a random great vintage year"
          >
            ✦ Surprise me
          </button>
        </div>
        <div className="hero-divider">
          <span className="hero-divider-ornament">❧</span>
        </div>
      </header>

      {error && (
        <div className="error-banner">
          <p>⚠ {error}</p>
        </div>
      )}

      {/* Map section — only rendered when data is loaded or loading */}
      {geojson ? (
        <section
          id="map-section"
          className={`map-section${fading ? " section-fading" : ""}`}
        >
          <WineMap geojson={geojson} year={activeYear} />
        </section>
      ) : loading ? (
        /* Skeleton map placeholder during load */
        <section id="map-section" className="map-section skeleton-map">
          <div className="skeleton-map-inner" />
        </section>
      ) : (
        <section id="map-section" className="explore-placeholder">
          {/* How It Works */}
          <div className="how-it-works">
            {HOW_IT_WORKS.map((step) => (
              <div key={step.step} className="hiw-step">
                <div className="hiw-icon">{step.icon}</div>
                <div className="hiw-body">
                  <span className="hiw-title">{step.title}</span>
                  <span className="hiw-desc">{step.desc}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Featured regions preview */}
          <div className="placeholder-top">
            <p className="placeholder-label">✦ Featured Regions ✦</p>
            <p className="placeholder-scale-note">Scores on a 100-point scale · 90+ Outstanding · 80–89 Excellent</p>
            <div className="featured-regions-grid">
              {FEATURED_REGIONS.map((r) => (
                <div
                  key={r.name}
                  className={`featured-region-card wine-type-${r.type}`}
                >
                  <div className="fr-header">
                    <span className="fr-flag">{r.flag}</span>
                    <div className={`fr-score-wrap wine-score-${r.type}`}>
                      <span className="fr-score-num">{r.score}</span>
                      <span className="fr-score-denom">/100</span>
                    </div>
                  </div>
                  <span className="fr-name">{r.name}</span>
                  <span className="fr-country">{r.country}</span>
                  <span className={`fr-style wine-badge-${r.type}`}>{r.style}</span>
                </div>
              ))}
            </div>
            <div className="wine-type-legend">
              <span className="wtl-label">Wine type:</span>
              <span className="wtl-item wtl-red">● Red</span>
              <span className="wtl-item wtl-white">● White</span>
              <span className="wtl-item wtl-rosé">● Rosé</span>
              <span className="wtl-item wtl-sparkling">● Sparkling</span>
            </div>
          </div>

          <div className="explore-placeholder-inner">
            <span className="explore-placeholder-icon">🍷</span>
            <p className="explore-placeholder-text">
              Enter a year above to explore wine regions from that vintage.
            </p>
          </div>
        </section>
      )}

      {/* Recommendation section: skeleton while loading, real data when ready */}
      {loading && !recommendation ? (
        <section className="recommendation-section skeleton-rec-section">
          <div className="skeleton-rec-title" />
          <div className="skeleton-card skeleton-card-primary" />
          <div className="skeleton-alt-row">
            <div className="skeleton-card" />
            <div className="skeleton-card" />
            <div className="skeleton-card" />
          </div>
        </section>
      ) : recommendation ? (
        <section
          key={animKey}
          className={`recommendation-section${fading ? " section-fading" : ""}`}
        >
          <RecommendationCard data={recommendation} year={activeYear} />
          {recommendation?.primary && (
            <div className="rec-actions">
              <button
                onClick={toggleSave}
                className={`save-btn${activeYear && isSaved(saved, activeYear, recommendation.primary.region_name) ? " save-btn-active" : ""}`}
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill={activeYear && isSaved(saved, activeYear, recommendation.primary.region_name) ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
                {activeYear && isSaved(saved, activeYear, recommendation.primary.region_name)
                  ? "Saved ✓"
                  : `Save ${activeYear} · ${recommendation.primary.region_name}`}
              </button>
              <button
                onClick={() => {
                  navigator.clipboard?.writeText(window.location.href);
                  setCopied(true);
                  setTimeout(() => setCopied(false), 2000);
                }}
                className="share-btn"
              >
                {copied ? "Copied!" : "Share this vintage →"}
              </button>
            </div>
          )}
        </section>
      ) : null}

      {saved.length > 0 && (
        <section className="saved-section">
          <h3 className="saved-title">Saved Vintages</h3>
          <div className="saved-grid">
            {saved.map((s) => (
              <div key={`${s.year}-${s.region_name}`} className="saved-card">
                <button className="saved-remove" onClick={() => removeSaved(s.year, s.region_name)}>×</button>
                <span className="saved-year">{s.year}</span>
                <span className="saved-region">{s.region_name}</span>
                <span className="saved-meta">{s.score}pts · {s.wine_style}</span>
              </div>
            ))}
          </div>
          <button className="saved-clear" onClick={clearAllSaved}>Clear all</button>
        </section>
      )}

      <footer className="footer">
        <div className="footer-ornament">❧</div>
        <p>
          VintageMap &mdash; Wine vintage data sourced from public reviews and
          expert consensus. Boundaries are approximate.
        </p>
      </footer>
    </div>
  );
}

export default App;
