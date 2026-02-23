import { useState, useCallback, useEffect, useRef } from "react";
import DateInput from "./components/DateInput/DateInput";
import WineMap from "./components/Map/WineMap";
import RecommendationCard from "./components/Recommendation/RecommendationCard";
import { fetchRegionsGeoJSON, fetchRecommendation } from "./api/client";
import type { RecommendationResponse } from "./types";
import "./App.css";

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
  const abortRef = useRef<AbortController | null>(null);

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

    setLoading(true);
    setError(null);
    setActiveYear(year);

    try {
      const [geo, rec] = await Promise.all([
        fetchRegionsGeoJSON(year, controller.signal),
        fetchRecommendation(year, significance, controller.signal),
      ]);
      setGeojson(geo);
      setRecommendation(rec);
    } catch (e) {
      if (e instanceof Error && e.name === "AbortError") return;
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }, []);

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
          <DateInput onSubmit={handleSubmit} loading={loading} />
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

      {/* Map section — only rendered when data is loaded */}
      {geojson ? (
        <section id="map-section" className="map-section">
          <WineMap geojson={geojson} year={activeYear} />
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
            <div className="featured-regions-grid">
              {FEATURED_REGIONS.map((r) => (
                <div
                  key={r.name}
                  className={`featured-region-card wine-type-${r.type}`}
                >
                  <div className="fr-header">
                    <span className="fr-flag">{r.flag}</span>
                    <span className={`fr-score wine-score-${r.type}`}>{r.score}</span>
                  </div>
                  <span className="fr-name">{r.name}</span>
                  <span className="fr-country">{r.country}</span>
                  <span className={`fr-style wine-badge-${r.type}`}>{r.style}</span>
                </div>
              ))}
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

      {recommendation && (
        <section className="recommendation-section">
          <RecommendationCard data={recommendation} />
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
