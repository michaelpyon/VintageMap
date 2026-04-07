import "./WineMap.css";

const ITEMS = [
  { color: "var(--heatmap-outstanding)", label: "Outstanding (90+)" },
  { color: "var(--heatmap-excellent)", label: "Excellent (80-89)" },
  { color: "var(--heatmap-good)", label: "Good (70-79)" },
  { color: "var(--heatmap-average)", label: "Average (60-69)" },
  { color: "var(--heatmap-no-data)", label: "No Data" },
];

export default function Legend() {
  return (
    <div className="map-legend">
      <h4>Vintage Quality</h4>
      {ITEMS.map((item) => (
        <div key={item.label} className="legend-item">
          <span
            className="legend-swatch"
            style={{ backgroundColor: item.color }}
          />
          <span>{item.label}</span>
        </div>
      ))}
    </div>
  );
}
