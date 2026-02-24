import { useEffect } from "react";
import L from "leaflet";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import Legend from "./Legend";
import "./WineMap.css";

interface Props {
  geojson: GeoJSON.FeatureCollection | null;
  year: number | null;
}

const TILE_URL =
  "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png";
const TILE_ATTR =
  '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>';

function getColor(score: number): string {
  if (score >= 90) return "#722F37";
  if (score >= 80) return "#A0522D";
  if (score >= 70) return "#CD853F";
  if (score >= 60) return "#DEB887";
  if (score >= 50) return "#D2B48C";
  if (score > 0) return "#C8B89A";
  return "#AAAAAA";
}

function tierLabel(tier: string): string {
  const labels: Record<string, string> = {
    outstanding: "Outstanding",
    excellent: "Excellent",
    good: "Good",
    average: "Average",
    poor: "Poor",
    no_data: "No Data",
  };
  return labels[tier] || tier;
}

function stars(score: number): string {
  if (score >= 90) return "★★★★★";
  if (score >= 80) return "★★★★";
  if (score >= 70) return "★★★";
  if (score >= 60) return "★★";
  if (score > 0) return "★";
  return "";
}

/** Compute centroid of a GeoJSON polygon ring */
function centroid(coords: number[][][]): [number, number] {
  const ring = coords[0];
  let lat = 0;
  let lng = 0;
  for (const pt of ring) {
    lng += pt[0];
    lat += pt[1];
  }
  return [lat / ring.length, lng / ring.length];
}

/** Create a custom wine bottle DivIcon */
function createWineBottleIcon(score: number): L.DivIcon {
  const color = getColor(score);
  // Wine bottle SVG: capsule top, neck, body with label highlight
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 36" width="20" height="36">
    <rect x="7" y="0" width="6" height="4" rx="2" fill="${color}" opacity="0.9"/>
    <rect x="7.5" y="4" width="5" height="7" fill="${color}"/>
    <path d="M4.5 11 Q3 13 3 15 L3 30 Q3 33 5.5 33 L14.5 33 Q17 33 17 30 L17 15 Q17 13 15.5 11 Z" fill="${color}"/>
    <rect x="6" y="18" width="8" height="9" rx="1.5" fill="rgba(255,255,255,0.22)"/>
    <rect x="6.5" y="10" width="7" height="2.5" rx="0.5" fill="${color}" opacity="0.6"/>
  </svg>`;

  return L.divIcon({
    html: svg,
    className: "wine-bottle-marker",
    iconSize: [20, 36],
    iconAnchor: [10, 36],
    popupAnchor: [0, -38],
  });
}

// Fit map to world bounds when year changes
function FitWorld({ trigger }: { trigger: number | null }) {
  const map = useMap();
  useEffect(() => {
    if (trigger) {
      map.setView([20, 10], 2);
    }
  }, [trigger, map]);
  return null;
}

/** Human label for drinking window values */
function drinkingWindowText(dw: string): string {
  const map: Record<string, string> = {
    young:     "🟢 Drink Now — Still Young",
    at_peak:   "⭐ At Peak — Best Time to Drink",
    mature:    "🍂 Mature — Still Enjoyable",
    past_peak: "⚠️ Past Peak",
    cellaring: "🕐 Needs More Cellaring",
  };
  return map[dw] || dw.replace(/_/g, " ");
}

function RegionMarkers({
  geojson,
  year,
}: {
  geojson: GeoJSON.FeatureCollection;
  year: number | null;
}) {
  return (
    <>
      {geojson.features.map((feature) => {
        const props = (feature.properties || {}) as Record<string, unknown>;
        const key = (props.region_key as string) || Math.random().toString();
        const score = (props.score as number) || 0;
        const tier = (props.quality_tier as string) || "no_data";
        const name =
          (props.display_name as string) ||
          (props.region_key as string) ||
          "Unknown";
        const country = (props.country as string) || "";
        const wineStyle = (props.wine_style as string) || "";
        const grapes = (props.primary_grapes as string[]) || [];
        const drinkingWindow = (props.drinking_window as string) || "";

        if (!feature.geometry || feature.geometry.type !== "Polygon") {
          return null;
        }

        const [lat, lng] = centroid(
          (feature.geometry as GeoJSON.Polygon).coordinates
        );

        const icon = createWineBottleIcon(score);

        return (
          <Marker key={key} position={[lat, lng]} icon={icon}>
            <Popup className="wine-popup">
              <div className="wine-popup-content">
                <div className="wp-header">
                  <strong className="wp-name">{name}</strong>
                  {score > 0 && (
                    <span className="wp-score">{score}/100</span>
                  )}
                </div>
                {country && <div className="wp-country">{country}</div>}
                {wineStyle && (
                  <div className="wp-style">{wineStyle}</div>
                )}
                {score > 0 && (
                  <div className="wp-tier">
                    {stars(score)} {tierLabel(tier)}
                  </div>
                )}
                {drinkingWindow && (
                  <div className="wp-drinking-window">{drinkingWindowText(drinkingWindow)}</div>
                )}
                {grapes.length > 0 && (
                  <div className="wp-grapes">{grapes.join(", ")}</div>
                )}
                {year && (
                  <div className="wp-vintage">{year} vintage</div>
                )}
              </div>
            </Popup>
          </Marker>
        );
      })}
    </>
  );
}

export default function WineMap({ geojson, year }: Props) {
  return (
    <div className="wine-map-container">
      {!year && (
        <div className="map-placeholder">
          <p>Enter a year above to explore vintage quality around the world.</p>
        </div>
      )}
      {geojson && year && (
        <div className="map-hint">
          🍾 Click bottle markers to see vintage details
        </div>
      )}
      <MapContainer
        center={[20, 10]}
        zoom={2}
        minZoom={2}
        maxZoom={10}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer url={TILE_URL} attribution={TILE_ATTR} />
        <FitWorld trigger={year} />
        {geojson && year && <RegionMarkers geojson={geojson} year={year} />}
        {year && <Legend />}
      </MapContainer>
    </div>
  );
}
