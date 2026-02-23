const isLocalhost =
  typeof window !== "undefined" &&
  (window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1");

const BASE =
  import.meta.env.VITE_API_URL ||
  (isLocalhost ? "/api" : "https://vintagemap-production.up.railway.app/api");

export async function fetchRegionsGeoJSON(year: number, signal?: AbortSignal) {
  const res = await fetch(`${BASE}/regions/${year}`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch regions: ${res.statusText}`);
  return res.json();
}

export async function fetchVintage(year: number, signal?: AbortSignal) {
  const res = await fetch(`${BASE}/vintage/${year}`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch vintage: ${res.statusText}`);
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

export async function fetchYearRange(signal?: AbortSignal) {
  const res = await fetch(`${BASE}/year-range`, { signal });
  if (!res.ok) throw new Error(`Failed to fetch year range: ${res.statusText}`);
  return res.json();
}
