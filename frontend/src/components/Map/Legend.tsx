import "./WineMap.css";

const ITEMS = [
  { color: "#722F37", label: "Outstanding (90+)" },
  { color: "#A0522D", label: "Excellent (80-89)" },
  { color: "#CD853F", label: "Good (70-79)" },
  { color: "#DEB887", label: "Average (60-69)" },
  { color: "#C0C0C0", label: "No Data" },
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
