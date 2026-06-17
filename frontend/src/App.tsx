import { useEffect, useState } from "react";

import { loadAlertExplanation, loadAlertExplanationComparison, loadDashboardData } from "./api";
import {
  fallbackEvaluation,
  fallbackInferenceModel,
  fallbackInferenceResult,
  fallbackModelMetrics,
  sampleAlerts,
} from "./sampleData";
import type {
  Evaluation,
  Explanation,
  ExplanationComparison,
  InferenceModelInfo,
  InferenceResult,
  ModelMetric,
} from "./types";

function App() {
  // Frontend uu tien du lieu that tu backend, neu loi thi dung sample fallback.
  const [alerts, setAlerts] = useState(sampleAlerts);
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [explanation, setExplanation] = useState<Explanation | null>(null);
  const [comparison, setComparison] = useState<ExplanationComparison | null>(null);
  const [modelMetrics, setModelMetrics] = useState<ModelMetric[]>([]);
  const [inferenceModel, setInferenceModel] = useState<InferenceModelInfo | null>(null);
  const [inferenceResult, setInferenceResult] = useState<InferenceResult | null>(null);
  const selected = alerts[0];

  useEffect(() => {
    async function loadDashboard() {
      try {
        // Lay dong thoi alert, evaluation, metric va inference de dashboard co du lieu day du.
        const dashboardData = await loadDashboardData();
        setAlerts(dashboardData.alerts);
        setEvaluation(dashboardData.evaluation);
        setModelMetrics(dashboardData.modelMetrics);
        setInferenceModel(dashboardData.inferenceModel);
        setInferenceResult(dashboardData.inferenceResult);

        if (dashboardData.alerts[0]) {
          // Chi can mot alert dau tien de minh hoa phan giai thich va comparison.
          setExplanation(await loadAlertExplanation(dashboardData.alerts[0].alert_id));
          setComparison(await loadAlertExplanationComparison(dashboardData.alerts[0].alert_id));
        }
      } catch {
        // Neu backend chua chay, hien du lieu mau de giao dien van demo duoc.
        setEvaluation(fallbackEvaluation);
        setModelMetrics(fallbackModelMetrics);
        setInferenceModel(fallbackInferenceModel);
        setInferenceResult(fallbackInferenceResult);
      }
    }

    loadDashboard();
  }, []);

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Master Thesis Prototype</p>
        <h1>LLM-Assisted Intrusion Detection SOC</h1>
        <p>ML detects attacks. LLM/RAG explains alerts and recommends response steps.</p>
      </section>

      <section className="cards">
        <article><span>Total Alerts</span><strong>{alerts.length}</strong></article>
        <article><span>High Severity</span><strong>{alerts.filter((alert) => alert.severity === "High").length}</strong></article>
        <article><span>Accuracy</span><strong>{evaluation ? Math.round(evaluation.accuracy * 100) : 0}%</strong></article>
      </section>

      <section className="grid">
        <div className="panel">
          <h2>Security Alerts</h2>
          <table>
            <thead><tr><th>Type</th><th>Source</th><th>Severity</th><th>Priority</th><th>Confidence</th></tr></thead>
            <tbody>
              {alerts.map((alert) => (
                <tr key={alert.alert_id}>
                  <td>{alert.attack_type}</td>
                  <td>{alert.src_ip}</td>
                  <td><span className="badge">{alert.severity}</span></td>
                  <td>{alert.triage_priority}</td>
                  <td>{Math.round(alert.confidence * 100)}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="panel analysis">
          <h2>LLM Analysis</h2>
          <p><strong>{selected.attack_type}</strong> from {selected.src_ip} to {selected.dst_ip}</p>
          <p className="provider">
            MITRE: {explanation?.mitre_technique ?? selected.mitre_technique} | Priority: {explanation?.triage_priority ?? selected.triage_priority}
          </p>
          <p>{explanation?.summary ?? selected.reason}</p>
          <p className="provider">Provider: {explanation?.provider ?? "local fallback"}</p>
          <div className="feature-list">
            <span>Evidence features</span>
            {(explanation?.evidence_features ?? selected.top_features).map((feature) => <code key={feature}>{feature}</code>)}
          </div>
          <ul>
            {(explanation?.recommended_response ?? [
              "Block or rate-limit the source IP.",
              "Review related authentication/network logs.",
              "Escalate if successful access follows this alert.",
            ]).map((item) => <li key={item}>{item}</li>)}
          </ul>
        </div>
      </section>

      <section className="panel metrics-panel">
        <h2>Model Comparison</h2>
        <table>
          <thead><tr><th>Dataset</th><th>Model</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>FPR</th></tr></thead>
          <tbody>
            {modelMetrics.map((metric) => (
              <tr key={`${metric.dataset_id}-${metric.model_name}`}>
                <td>{metric.dataset_id}</td>
                <td>{metric.model_name}</td>
                <td>{formatPercent(metric.accuracy)}</td>
                <td>{formatPercent(metric.precision)}</td>
                <td>{formatPercent(metric.recall)}</td>
                <td>{formatPercent(metric.f1_score)}</td>
                <td>{formatPercent(metric.false_positive_rate)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="panel inference-panel">
        <h2>Model Inference</h2>
        <div className="inference-grid">
          <article>
            <span>Default Model</span>
            <strong>{inferenceModel?.dataset_id ?? "cicids2017-full"} / {inferenceModel?.model_name ?? "random_forest"}</strong>
            <p>{inferenceModel?.status ?? "not loaded"}</p>
          </article>
          <article>
            <span>Sample Prediction</span>
            <strong>{inferenceResult?.prediction_label ?? "unavailable"}</strong>
            <p>Confidence: {formatPercent(inferenceResult?.confidence ?? 0)}</p>
          </article>
          <article>
            <span>Attack Probability</span>
            <strong>{inferenceResult?.attack_probability === null || inferenceResult?.attack_probability === undefined ? "n/a" : formatPercent(inferenceResult.attack_probability)}</strong>
            <p>{inferenceResult?.model_available ? "CICIDS2017 artifact loaded" : inferenceResult?.status ?? "model unavailable"}</p>
          </article>
        </div>
        <div className="feature-list">
          <span>Model features</span>
          {(inferenceResult?.top_features.length ? inferenceResult.top_features : ["artifact unavailable"]).map((feature) => <code key={feature}>{feature}</code>)}
        </div>
      </section>

      <section className="panel comparison-panel">
        <h2>Explanation Comparison</h2>
        <div className="comparison-grid">
          {(comparison?.comparisons ?? []).map((item) => (
            <article key={item.mode}>
              <span>{item.mode}</span>
              <strong>{item.uses_rag ? "RAG" : "No RAG"}</strong>
              <p>{item.summary}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function formatPercent(value: number) {
  // Convert so 0-1 thanh phan tram de doc de hon tren UI.
  return `${Math.round(value * 100)}%`;
}

export default App;
