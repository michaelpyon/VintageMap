import { useState, useCallback } from "react";
import DateInput from "./components/DateInput/DateInput";
import WineMap from "./components/Map/WineMap";
import RecommendationCard from "./components/Recommendation/RecommendationCard";
import { fetchRegionsGeoJSON, fetchRecommendation } from "./api/client";
import type { RecommendationResponse } from "./types";
import "./App.css";

function App() {
  const [geojson, setGeojson] = useState<GeoJSON.FeatureCollection | null>(
    null
  );
  const [recommendation, setRecommendation] =
    useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeYear, setActiveYear] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = useCallback(
    async (year: number, significance: string) => {
      setLoading(true);
      setError(null);
      setActiveYear(year);
      try {
        const [geo, rec] = await Promise.all([
          fetchRegionsGeoJSON(year),
          fetchRecommendation(year, significance),
        ]);
        setGeojson(geo);
        setRecommendation(rec);

        setTimeout(() => {
          document
            .getElementById("map-section")
            ?.scrollIntoView({ behavior: "smooth" });
        }, 100);
      } catch (e) {
        setError(e instanceof Error ? e.message : "Something went wrong.");
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return (
    <div className="app">
      <header className="hero">
        <div className="hero-content">
          <h1 className="hero-title">VintageMap</h1>
          <p className="hero-subtitle">
            Enter a date that matters to you. We'll find the perfect wine from
            that year.
          </p>
          <DateInput onSubmit={handleSubmit} loading={loading} />
        </div>
      </header>

      {error && (
        <div className="error-banner">
          <p>{error}</p>
        </div>
      )}

      <section id="map-section" className="map-section">
        <WineMap geojson={geojson} year={activeYear} />
      </section>

      {recommendation && (
        <section className="recommendation-section">
          <RecommendationCard data={recommendation} />
        </section>
      )}

      <footer className="footer">
        <p>
          VintageMap &mdash; Wine vintage data sourced from public reviews and
          expert consensus. Boundaries are approximate.
        </p>
      </footer>
    </div>
  );
}

export default App;
