import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { getPredictions, predictWineQuality } from "./lib/api";
import type { PredictionRecord, WineData } from "./lib/types";
import "./App.css";

const initialFormData: WineData = {
  fixed_acidity: 0,
  volatile_acidity: 0,
  citric_acid: 0,
  residual_sugar: 0,
  chlorides: 0,
  free_sulfur_dioxide: 0,
  total_sulfur_dioxide: 0,
  density: 0,
  pH: 0,
  sulphates: 0,
  alcohol: 0,
  Id: 1,
};

const fieldOrder: Array<{ key: keyof WineData; label: string; step?: string }> = [
  { key: "Id", label: "Sample ID", step: "1" },
  { key: "fixed_acidity", label: "Fixed acidity", step: "0.01" },
  { key: "volatile_acidity", label: "Volatile acidity", step: "0.01" },
  { key: "citric_acid", label: "Citric acid", step: "0.01" },
  { key: "residual_sugar", label: "Residual sugar", step: "0.01" },
  { key: "chlorides", label: "Chlorides", step: "0.0001" },
  { key: "free_sulfur_dioxide", label: "Free sulfur dioxide", step: "0.01" },
  { key: "total_sulfur_dioxide", label: "Total sulfur dioxide", step: "0.01" },
  { key: "density", label: "Density", step: "0.0001" },
  { key: "pH", label: "pH", step: "0.01" },
  { key: "sulphates", label: "Sulphates", step: "0.01" },
  { key: "alcohol", label: "Alcohol", step: "0.01" },
];

function App() {
  const [formData, setFormData] = useState<WineData>(initialFormData);
  const [predictedQuality, setPredictedQuality] = useState<number | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingHistory, setIsLoadingHistory] = useState(true);
  const [history, setHistory] = useState<PredictionRecord[]>([]);

  const sortedHistory = useMemo(
    () => [...history].sort((a, b) => b.prediction_id - a.prediction_id),
    [history]
  );

  const fetchHistory = async () => {
    setIsLoadingHistory(true);
    setHistoryError(null);
    try {
      const result = await getPredictions();
      setHistory(result.data);
    } catch (error) {
      setHistoryError(
        error instanceof Error ? error.message : "Could not load prediction history."
      );
    } finally {
      setIsLoadingHistory(false);
    }
  };

  useEffect(() => {
    void fetchHistory();
  }, []);

  const handleInputChange = (key: keyof WineData, value: string) => {
    const parsedValue = Number(value);
    setFormData((current) => ({
      ...current,
      [key]: Number.isNaN(parsedValue) ? 0 : parsedValue,
    }));
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setSubmitError(null);

    try {
      const result = await predictWineQuality(formData);
      setPredictedQuality(result.predicted_quality);
      await fetchHistory();
    } catch (error) {
      setSubmitError(error instanceof Error ? error.message : "Prediction request failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="page">
      <header>
        <h1>Wine Quality Predictor</h1>
        <p>Submit wine chemistry values to get quality predictions and view saved history.</p>
      </header>

      <section className="card">
        <h2>Predict quality</h2>
        <form className="form-grid" onSubmit={handleSubmit}>
          {fieldOrder.map((field) => (
            <label key={field.key}>
              {field.label}
              <input
                required
                type="number"
                step={field.step ?? "0.01"}
                value={formData[field.key]}
                onChange={(event) => handleInputChange(field.key, event.target.value)}
              />
            </label>
          ))}
          <div className="actions">
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? "Predicting..." : "Predict"}
            </button>
          </div>
        </form>
        {predictedQuality !== null && (
          <p className="success">Latest predicted quality: {predictedQuality}</p>
        )}
        {submitError && <p className="error">{submitError}</p>}
      </section>

      <section className="card">
        <div className="section-head">
          <h2>Prediction history</h2>
          <button type="button" className="secondary" onClick={() => void fetchHistory()}>
            Refresh
          </button>
        </div>
        {isLoadingHistory ? (
          <p>Loading history...</p>
        ) : sortedHistory.length === 0 ? (
          <p>No predictions stored yet.</p>
        ) : (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Prediction ID</th>
                  <th>Sample ID</th>
                  <th>Predicted quality</th>
                  <th>Alcohol</th>
                  <th>pH</th>
                  <th>Density</th>
                </tr>
              </thead>
              <tbody>
                {sortedHistory.map((row) => (
                  <tr key={row.prediction_id}>
                    <td>{row.prediction_id}</td>
                    <td>{row.Id}</td>
                    <td>{row.wine_quality}</td>
                    <td>{row.alcohol}</td>
                    <td>{row.pH}</td>
                    <td>{row.density}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {historyError && <p className="error">{historyError}</p>}
      </section>
    </main>
  );
}

export default App;
