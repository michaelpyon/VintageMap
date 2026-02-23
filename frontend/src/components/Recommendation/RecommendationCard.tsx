import type { RecommendationResponse, Recommendation } from "../../types";
import "./RecommendationCard.css";

interface Props {
  data: RecommendationResponse;
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
}: {
  rec: Recommendation;
  isPrimary?: boolean;
}) {
  return (
    <div className={`wine-card ${isPrimary ? "wine-card-primary" : ""}`}>
      <div className="wine-card-top">
        <div className="wine-card-info">
          <h3 className="wine-card-region">{rec.region_name}</h3>
          <span className="wine-card-country">{rec.country}</span>
          <span className="wine-card-style">{rec.wine_style}</span>
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

export default function RecommendationCard({ data }: Props) {
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

      <WineCard rec={data.primary} isPrimary />

      {data.alternatives.length > 0 && (
        <>
          <h3 className="alt-title">Also Worth Exploring</h3>
          <div className="alt-grid">
            {data.alternatives.map((alt) => (
              <WineCard key={alt.region_key} rec={alt} />
            ))}
          </div>
        </>
      )}
    </div>
  );
}
