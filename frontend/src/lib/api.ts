import type { PredictionResponse, PredictionsResponse, WineData } from "./types";

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL ?? "").replace(/\/$/, "");

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
    },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(`API request failed (${response.status}): ${message}`);
  }

  return (await response.json()) as T;
}

export function predictWineQuality(payload: WineData): Promise<PredictionResponse> {
  return request<PredictionResponse>("/predict", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function getPredictions(): Promise<PredictionsResponse> {
  return request<PredictionsResponse>("/predictions");
}
