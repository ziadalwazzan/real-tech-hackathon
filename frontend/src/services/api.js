const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchRiskAssessment(payload) {
  const response = await fetch(`${API_BASE_URL}/risk-assessment`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || "Unable to fetch risk assessment");
  }

  return response.json();
}

export async function fetchFrontierComparables(city, topN = 3) {
  const response = await fetch(
    `${API_BASE_URL}/frontier-comparables?city=${encodeURIComponent(city)}&top_n=${topN}`
  );

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || "Unable to fetch frontier comparables");
  }

  return response.json();
}

export async function fetchSeasonalPrices(city) {
  const response = await fetch(
    `${API_BASE_URL}/seasonal-prices?city=${encodeURIComponent(city)}`
  );

  if (!response.ok) {
    const detail = await response.json().catch(() => ({}));
    throw new Error(detail.detail || "Unable to fetch seasonal prices");
  }

  return response.json();
}
