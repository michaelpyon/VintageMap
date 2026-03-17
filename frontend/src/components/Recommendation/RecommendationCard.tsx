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

/** Map drinking_window key → human label + icon */
function drinkingWindowLabel(dw: string): { label: string; icon: string; cls: string } {
  switch (dw) {
    case "young": return { label: "Drink Now", icon: "🟢", cls: "dw-young" };
    case "at_peak": return { label: "At Peak — Drink Now", icon: "⭐", cls: "dw-peak" };
    case "mature": return { label: "Mature — Still Good", icon: "🍂", cls: "dw-mature" };
    case "past_peak": return { label: "Past Peak", icon: "⚠️", cls: "dw-past" };
    case "cellaring": return { label: "Needs Cellaring", icon: "🕐", cls: "dw-cellar" };
    default: return { label: dw.replace(/_/g, " "), icon: "🍷", cls: "" };
  }
}

function ScoreBadge({ score, typeClass }: { score: number; typeClass?: string }) {
  return (
    <div className={`score-badge${typeClass ? ` score-badge-${typeClass}` : ""}`}>
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
  const staggerDelay = `${index * 80}ms`;

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
          {rec.drinking_window && (() => {
            const dw = drinkingWindowLabel(rec.drinking_window);
            return (
              <span className={`drinking-window-badge ${dw.cls}`}>
                {dw.icon} {dw.label}
              </span>
            );
          })()}
        </div>
        <ScoreBadge score={rec.score} typeClass={typeClass} />
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

      {year && (
        <a
          href={`https://www.vivino.com/search/wines?q=${encodeURIComponent(rec.region_name + " " + year)}`}
          target="_blank"
          rel="noopener noreferrer"
          className="vivino-link"
        >
          Check prices on Vivino →
        </a>
      )}
    </div>
  );
}

/** Map quality_tier → human summary + class */
function qualityTierSummary(tier: string): { label: string; cls: string } {
  switch (tier) {
    case "outstanding": return { label: "🌟 Outstanding Vintage", cls: "qt-outstanding" };
    case "excellent":   return { label: "⭐ Excellent Vintage", cls: "qt-excellent" };
    case "good":        return { label: "✓ Good Vintage", cls: "qt-good" };
    case "average":     return { label: "○ Average Vintage", cls: "qt-average" };
    case "poor":        return { label: "↓ Challenging Year", cls: "qt-poor" };
    default:            return { label: "", cls: "" };
  }
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

  const tierInfo = qualityTierSummary(data.primary.quality_tier);

  return (
    <div className="rec-container">
      <h2 className="rec-title">Your {data.year} Vintage</h2>
      {tierInfo.label && (
        <p className={`rec-quality-tier ${tierInfo.cls}`}>{tierInfo.label}</p>
      )}

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
