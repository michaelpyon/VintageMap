import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Tooltip, useMap } from "react-leaflet";
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
  // Return [lat, lng] for Leaflet
  return [lat / ring.length, lng / ring.length];
}

// Fit map to world bounds when year changes so all markers are visible
function FitWorld({ trigger }: { trigger: number | null }) {
  const map = useMap();
  useEffect(() => {
    if (trigger) {
      map.setView([20, 10], 2);
    }
  }, [trigger, map]);
  return null;
}

function RegionMarkers({ geojson }: { geojson: GeoJSON.FeatureCollection }) {
  return (
    <>
      {geojson.features.map((feature) => {
        const props = (feature.properties || {}) as Record<string, unknown>;
        const key = (props.region_key as string) || Math.random().toString();
        const score = (props.score as number) || 0;
        const tier = (props.quality_tier as string) || "no_data";
        const name = (props.display_name as string) || (props.region_key as string) || "Unknown";
        const country = (props.country as string) || "";
        const desc = (props.description as string) || "";
        const grapes = (props.primary_grapes as string[]) || [];
        const color = getColor(score);

        if (
          !feature.geometry ||
          feature.geometry.type !== "Polygon"
        ) {
          return null;
        }

        const [lat, lng] = centroid(
          (feature.geometry as GeoJSON.Polygon).coordinates
        );

        return (
          <CircleMarker
            key={key}
            center={[lat, lng]}
            radius={18}
            pathOptions={{
              fillColor: color,
              fillOpacity: 0.85,
              color: "#4A2C2A",
              weight: 2,
            }}
            eventHandlers={{
              mouseover: (e) => {
                e.target.setStyle({ radius: 22, fillOpacity: 0.98, weight: 3, color: "#722F37" });
              },
              mouseout: (e) => {
                e.target.setStyle({ radius: 18, fillOpacity: 0.85, weight: 2, color: "#4A2C2A" });
              },
            }}
          >
            <Tooltip
              className="region-tooltip"
              direction="top"
              offset={[0, -16]}
              sticky
            >
              <div className="tooltip-content">
                <div className="tooltip-header">
                  <strong>{name}</strong>
                  {score > 0 && (
                    <span className="tooltip-score">{score}/100</span>
                  )}
                </div>
                <div className="tooltip-sub">{country}</div>
                {score > 0 && (
                  <div className="tooltip-tier">
                    {stars(score)} {tierLabel(tier)}
                  </div>
                )}
                {desc && <div className="tooltip-desc">{desc}</div>}
                {grapes.length > 0 && (
                  <div className="tooltip-grapes">{grapes.join(", ")}</div>
                )}
              </div>
            </Tooltip>
          </CircleMarker>
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
        {geojson && year && <RegionMarkers geojson={geojson} />}
        {year && <Legend />}
      </MapContainer>
    </div>
  );
}
