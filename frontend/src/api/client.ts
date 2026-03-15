const BASE = import.meta.env.VITE_API_URL || "/api";

export async function fetchRegionsGeoJSON(year: number, signal?: AbortSignal) {
  const res = await fetch(`${BASE}/regions/${year}`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch regions: ${res.statusText}`);
  return res.json();
}

export async function fetchRecommendation(
  year: number,
  significance: string,
  signal?: AbortSignal
) {
  const res = await fetch(
    `${BASE}/recommend?year=${year}&significance=${significance}`,
    { signal }
  );
  if (!res.ok)
    throw new Error(`Failed to fetch recommendation: ${res.statusText}`);
  return res.json();
}

export async function fetchYearReport(year: number, signal?: AbortSignal) {
  const res = await fetch(`${BASE}/vintage/${year}/report`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch vintage report: ${res.statusText}`);
  return res.json();
}
