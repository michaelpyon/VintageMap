const BASE = import.meta.env.VITE_API_URL || "/api";

export async function fetchRegionsGeoJSON(year: number) {
  const res = await fetch(`${BASE}/regions/${year}`);
  if (!res.ok) throw new Error(`Failed to fetch regions: ${res.statusText}`);
  return res.json();
}

export async function fetchVintage(year: number) {
  const res = await fetch(`${BASE}/vintage/${year}`);
  if (!res.ok) throw new Error(`Failed to fetch vintage: ${res.statusText}`);
  return res.json();
}

export async function fetchRecommendation(year: number, significance: string) {
  const res = await fetch(
    `${BASE}/recommend?year=${year}&significance=${significance}`
  );
  if (!res.ok)
    throw new Error(`Failed to fetch recommendation: ${res.statusText}`);
  return res.json();
}

export async function fetchYearRange() {
  const res = await fetch(`${BASE}/year-range`);
  if (!res.ok) throw new Error(`Failed to fetch year range: ${res.statusText}`);
  return res.json();
}
