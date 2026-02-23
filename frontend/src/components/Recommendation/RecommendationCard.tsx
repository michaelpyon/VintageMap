import type { RecommendationResponse, Recommendation } from "../../types";
import "./RecommendationCard.css";

interface Props {
  data: RecommendationResponse;
  year?: number | null;
}

/** Map wine_style to a food pairing icon */
function foodPairingIcon(wineStyle: string): string {
  const s = wineStyle.toLowerCase();
  if (s === "white" || s.includes("chardonnay") || s.includes("riesling") ||
      s.includes("sauvignon blanc") || s.includes("pinot grigio")) return "🐟";
  if (s === "rosé" || s.includes("rosé") || s.includes("rose")) return "🍓";
  // Default: bold red
  return "🥩";
}

/** Return a CSS class suffix based on wine style */
function wineTypeClass(wineStyle: string): string {
  const s = wineStyle.toLowerCase();
  if (s === "white" || s.includes("chardonnay") || s.includes("sauvignon")) return "white";
  if (s === "rosé" || s.includes("rosé") || s.includes("rose")) return "rosé";
  if (s === "sparkling" || s.includes("champagne") || s.includes("prosecco")) return "sparkling";
  return "red";
}

function ScoreBadge({ score }: { score: number }) {
  return (
    <div className="score-badge">
      <span className="score-number">{score}</span>
      <span className="score-label">/ 100</span>
    </div>
  );
}

function WineCard({
  rec,
  isPrimary,
  year,
  index = 0,
}: {
  rec: Recommendation;
  isPrimary?: boolean;
  year?: number | null;
  index?: number;
}) {
  const typeClass = wineTypeClass(rec.wine_style);
  const pairingIcon = foodPairingIcon(rec.wine_style);
  const staggerDelay = `${index * 50}ms`;

  return (
    <div
      className={`wine-card wine-card-type-${typeClass} ${isPrimary ? "wine-card-primary" : ""}`}
      style={{ animationDelay: staggerDelay } as React.CSSProperties}
    >
      {/* Vintage year badge — top-right corner */}
      {year && (
        <div className="vintage-year-badge">{year}</div>
      )}

      <div className="wine-card-top">
        <div className="wine-card-info">
          <h3 className="wine-card-region">{rec.region_name}</h3>
          <span className="wine-card-country">{rec.country}</span>
          <div className="wine-card-meta">
            <span className="wine-card-style">{rec.wine_style}</span>
            <span className="wine-pairing-icon" title="Food pairing">{pairingIcon}</span>
          </div>
        </div>
        <ScoreBadge score={rec.score} />
      </div>

      <p className="wine-card-text">{rec.recommendation_text}</p>

      {rec.grapes.length > 0 && (
        <p className="wine-card-grapes">{rec.grapes.join(", ")}</p>
      )}

      {rec.suggestion && (
        <p className="wine-card-suggestion">{rec.suggestion}</p>
      )}

      {rec.notable_wines.length > 0 && (
        <div className="wine-card-notable">
          <span className="notable-label">Notable producers:</span>{" "}
          {rec.notable_wines.join(" \u00B7 ")}
        </div>
      )}
    </div>
  );
}

export default function RecommendationCard({ data, year }: Props) {
  if (data.message) {
    return (
      <div className="rec-container">
        <p className="rec-message">{data.message}</p>
      </div>
    );
  }

  if (!data.primary) return null;

  return (
    <div className="rec-container">
      <h2 className="rec-title">Your {data.year} Vintage</h2>

      <WineCard rec={data.primary} isPrimary year={year ?? data.year} index={0} />

      {data.alternatives.length > 0 && (
        <>
          <h3 className="alt-title">Also Worth Exploring</h3>
          <div className="alt-grid">
            {data.alternatives.map((alt, i) => (
              <WineCard
                key={alt.region_key}
                rec={alt}
                year={year ?? data.year}
                index={i + 1}
              />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
