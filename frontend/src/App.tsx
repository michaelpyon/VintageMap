import { useState, useCallback, useEffect, useRef } from "react";
import DateInput from "./components/DateInput/DateInput";
import type { DateInputHandle } from "./components/DateInput/DateInput";
import WineMap from "./components/Map/WineMap";
import RecommendationCard from "./components/Recommendation/RecommendationCard";
import { fetchRegionsGeoJSON, fetchRecommendation, fetchYearReport } from "./api/client";
import type { RecommendationResponse, HarvestReport, HarvestReportRegion } from "./types";
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
  bestYear: number;
}[] = [
  { name: "Bordeaux", flag: "🇫🇷", style: "Cabernet Blend", country: "France", score: 96, type: "red", bestYear: 2016 },
  { name: "Burgundy", flag: "🇫🇷", style: "Pinot Noir", country: "France", score: 98, type: "red", bestYear: 2010 },
  { name: "Champagne", flag: "🇫🇷", style: "Sparkling Blend", country: "France", score: 97, type: "sparkling", bestYear: 2008 },
  { name: "Napa Valley", flag: "🇺🇸", style: "Cabernet Sauvignon", country: "USA", score: 95, type: "red", bestYear: 2019 },
  { name: "Mosel", flag: "🇩🇪", style: "Riesling", country: "Germany", score: 94, type: "white", bestYear: 2019 },
  { name: "Tuscany", flag: "🇮🇹", style: "Sangiovese", country: "Italy", score: 94, type: "red", bestYear: 2010 },
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
  const [yearReport, setYearReport] = useState<HarvestReport | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeYear, setActiveYear] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [fading, setFading] = useState(false);
  const [animKey, setAnimKey] = useState(0);
  const abortRef = useRef<AbortController | null>(null);
  const fadeTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
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

    // Cancel any pending fade timeout from a previous call
    if (fadeTimeoutRef.current) {
      clearTimeout(fadeTimeoutRef.current);
      fadeTimeoutRef.current = null;
    }

    // After 150ms fade-out, clear old data
    fadeTimeoutRef.current = setTimeout(() => {
      setGeojson(null);
      setRecommendation(null);
      setYearReport(null);
      setFading(false);
      fadeTimeoutRef.current = null;
    }, 150);

    try {
      // Fetch all three in parallel. Map + recommendation are critical;
      // year report is additive (a failure won't block the core flow).
      const [geoResult, recResult, reportResult] = await Promise.allSettled([
        fetchRegionsGeoJSON(year, controller.signal),
        fetchRecommendation(year, significance, controller.signal),
        fetchYearReport(year, controller.signal),
      ]);

      // If critical calls failed, throw so the catch block handles it
      if (geoResult.status === "rejected") throw geoResult.reason;
      if (recResult.status === "rejected") throw recResult.reason;

      // Cancel the fade timeout — data arrived before it fired
      if (fadeTimeoutRef.current) {
        clearTimeout(fadeTimeoutRef.current);
        fadeTimeoutRef.current = null;
        setFading(false);
      }

      // Set all state in one synchronous batch so React renders everything together
      setGeojson(geoResult.value);
      setRecommendation(recResult.value);
      setYearReport(reportResult.status === "fulfilled" ? reportResult.value : null);
      setAnimKey((k) => k + 1);
      history.replaceState({}, "", `?year=${year}&occasion=${significance}`);
    } catch (e) {
      if (e instanceof Error && e.name === "AbortError") return;
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }, []);

  // Auto-search from URL param on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const yearParam = params.get("year");
    const occasionParam = params.get("occasion") || "other";
    if (yearParam) {
      const y = parseInt(yearParam, 10);
      if (!isNaN(y) && y >= 1970 && y <= 2023) {
        handleSubmit(y, occasionParam);
      }
    }
  }, [handleSubmit]);

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <div className="hero-badge stagger-in" style={{"--stagger": "0ms"} as React.CSSProperties}>✦ Wine Vintage Explorer ✦</div>
          <h1 className="hero-title stagger-in" style={{"--stagger": "80ms"} as React.CSSProperties}>VintageMap</h1>
          <p className="hero-subtitle stagger-in" style={{"--stagger": "160ms"} as React.CSSProperties}>
            Every great wine tells the story of its year. Enter a date that
            matters to you — we'll find the perfect vintage.
          </p>
          <div className="suggested-vintages stagger-in" style={{"--stagger": "240ms"} as React.CSSProperties}>
            {SUGGESTED_VINTAGES.map((v) => (
              <button
                key={v.year}
                className="vintage-pill"
                onClick={() => handleSubmit(v.year, "other")}
              >
                <span className="vintage-pill-label">{v.label}</span>
                <span className="vintage-pill-hint">{v.hint}</span>
              </button>
            ))}
          </div>
          <div className="stagger-in" style={{"--stagger": "320ms"} as React.CSSProperties}>
            <DateInput ref={dateInputRef} onSubmit={handleSubmit} loading={loading} />
          </div>
          <button
            type="button"
            className="surprise-btn stagger-in"
            style={{"--stagger": "400ms"} as React.CSSProperties}
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

      {/* Results — side by side map + info when active, placeholder when idle */}
      {(geojson || loading) ? (
        <div className="results-layout">
          {/* Left: Map */}
          <div className="results-left">
            {geojson ? (
              <section
                id="map-section"
                className={`map-section${fading ? " section-fading" : ""}`}
              >
                <WineMap geojson={geojson} year={activeYear} />
              </section>
            ) : (
              <section id="map-section" className="map-section skeleton-map">
                <div className="skeleton-map-inner" />
              </section>
            )}
          </div>

          {/* Right: Harvest Report + Recommendation */}
          <div className="results-right">
            {/* Harvest Report */}
            {loading && !yearReport && activeYear && (
              <section className="harvest-report-section skeleton-harvest">
                <div className="skeleton-harvest-title" />
                <div className="skeleton-harvest-summary" />
                <div className="skeleton-harvest-cols">
                  <div className="skeleton-harvest-col" />
                  <div className="skeleton-harvest-col" />
                </div>
              </section>
            )}
            {yearReport && (
              <section key={animKey} className={`harvest-report-section${fading ? " section-fading" : ""}`}>
                <h2 className="harvest-report-title">✦ {yearReport.year} Harvest Report</h2>
                <p className="harvest-report-summary">{yearReport.summary}</p>

                <div className="harvest-columns">
                  {/* Winners */}
                  <div className="harvest-col harvest-winners">
                    <h3 className="harvest-col-title">
                      🏆 Standout Regions
                      {yearReport.total_winners > 0 && (
                        <span className="harvest-count">{yearReport.total_winners}</span>
                      )}
                    </h3>
                    {yearReport.winners.length === 0 ? (
                      <p className="harvest-empty">No region scored 90+ this vintage — a difficult year across the board.</p>
                    ) : (
                      <ul className="harvest-list">
                        {yearReport.winners.map((r: HarvestReportRegion) => (
                          <li key={r.region_key} className="harvest-item harvest-item-win">
                            <div className="hi-header">
                              <span className="hi-name">{r.display_name}</span>
                              <span className="hi-score hi-score-win">{r.score}/100</span>
                            </div>
                            <span className="hi-country">{r.country}</span>
                            <p className="hi-desc">{r.description}</p>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>

                  {/* Strugglers */}
                  <div className="harvest-col harvest-strugglers">
                    <h3 className="harvest-col-title">
                      ⚠️ Difficult Conditions
                      {yearReport.total_strugglers > 0 && (
                        <span className="harvest-count harvest-count-struggle">{yearReport.total_strugglers}</span>
                      )}
                    </h3>
                    {yearReport.strugglers.length === 0 ? (
                      <p className="harvest-empty harvest-empty-positive">Every region performed solidly — no major struggles this vintage.</p>
                    ) : (
                      <ul className="harvest-list">
                        {yearReport.strugglers.map((r: HarvestReportRegion) => (
                          <li key={r.region_key} className="harvest-item harvest-item-struggle">
                            <div className="hi-header">
                              <span className="hi-name">{r.display_name}</span>
                              <span className="hi-score hi-score-struggle">{r.score}/100</span>
                            </div>
                            <span className="hi-country">{r.country}</span>
                            <p className="hi-desc">{r.description}</p>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </div>

                {yearReport.best_pick && (
                  <div className="harvest-best-pick">
                    <span className="hbp-label">Top Pick for {yearReport.year}</span>
                    <span className="hbp-region">{yearReport.best_pick.display_name}</span>
                    <span className="hbp-score">{yearReport.best_pick.score}/100</span>
                    <p className="hbp-desc">{yearReport.best_pick.description}</p>
                  </div>
                )}
              </section>
            )}

            {/* Recommendation */}
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
                      type="button"
                      onClick={() => {
                        navigator.clipboard?.writeText(window.location.href);
                        setCopied(true);
                        setTimeout(() => setCopied(false), 2000);
                      }}
                      className="share-btn"
                      aria-live="polite"
                    >
                      {copied ? "Copied!" : "Share this vintage →"}
                    </button>
                  </div>
                )}
              </section>
            ) : null}
          </div>{/* /results-right */}
        </div>{/* /results-layout */}
      ) : (
        <section id="map-section" className="explore-placeholder">
          {/* How It Works */}
          <div className="how-it-works">
            {HOW_IT_WORKS.map((step, i) => (
              <div key={step.step} className="hiw-step stagger-in" style={{"--stagger": `${100 + i * 80}ms`} as React.CSSProperties}>
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
              {FEATURED_REGIONS.map((r, i) => (
                <button
                  key={r.name}
                  type="button"
                  className={`featured-region-card wine-type-${r.type} stagger-in`}
                  style={{"--stagger": `${200 + i * 80}ms`} as React.CSSProperties}
                  onClick={() => handleSubmit(r.bestYear, "other")}
                  aria-label={`Explore ${r.name} ${r.bestYear} vintage`}
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
                </button>
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

      {saved.length > 0 && (
        <section className="saved-section">
          <h3 className="saved-title">Saved Vintages</h3>
          <div className="saved-grid">
            {saved.map((s) => (
              <div
                key={`${s.year}-${s.region_name}`}
                className="saved-card"
                onClick={() => handleSubmit(s.year, "other")}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => { if (e.key === "Enter") handleSubmit(s.year, "other"); }}
              >
                <button type="button" className="saved-remove" aria-label="Remove saved vintage" onClick={(e) => { e.stopPropagation(); removeSaved(s.year, s.region_name); }}>×</button>
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
          VintageMap, wine vintage data sourced from public reviews and
          expert consensus. Boundaries are approximate.
        </p>
      </footer>
    </div>
  );
}

export default App;
