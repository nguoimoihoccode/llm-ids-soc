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
        const dashboardData = await loadDashboardData();
        setAlerts(dashboardData.alerts);
        setEvaluation(dashboardData.evaluation);
        setModelMetrics(dashboardData.modelMetrics);
        setInferenceModel(dashboardData.inferenceModel);
        setInferenceResult(dashboardData.inferenceResult);

        if (dashboardData.alerts[0]) {
          setExplanation(await loadAlertExplanation(dashboardData.alerts[0].alert_id));
          setComparison(await loadAlertExplanationComparison(dashboardData.alerts[0].alert_id));
        }
      } catch {
        setEvaluation(fallbackEvaluation);
        setModelMetrics(fallbackModelMetrics);
        setInferenceModel(fallbackInferenceModel);
        setInferenceResult(fallbackInferenceResult);
      }
    }

    loadDashboard();
  }, []);

  const severityCounts = alerts.reduce<Record<string, number>>((acc, a) => {
    acc[a.severity] = (acc[a.severity] || 0) + 1;
    return acc;
  }, {});

  return (
    <main className="shell">
      <section className="hero">
        <p className="eyebrow">Master Thesis Prototype</p>
        <h1>LLM-Assisted Intrusion Detection SOC</h1>
        <p>ML detects attacks. LLM/RAG explains alerts and recommends response steps.</p>
      </section>

      <section className="cards">
        <article><span>Total Alerts</span><strong>{alerts.length}</strong></article>
        <article><span>High Severity</span><strong>{alerts.filter((a) => a.severity === "High").length}</strong></article>
        <article><span>Accuracy</span><strong>{evaluation ? Math.round(evaluation.accuracy * 100) : 0}%</strong></article>
      </section>

      <section className="charts-row">
        <SeverityChart counts={severityCounts} />
        <ModelF1Chart metrics={modelMetrics} />
        <AttackTypeChart alerts={alerts} />
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
          <div className="panel-header">
            <h2>LLM Analysis</h2>
            <button className="btn-export" onClick={() => exportIncidentReport(selected, explanation)}>
              Export Report
            </button>
          </div>
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
        <h2>Model Inference — Why This Alert?</h2>
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
          <span>Top contributing features (SHAP)</span>
          {inferenceResult?.top_features.length ? (
            inferenceResult.top_features.map((fi) => (
              <div key={fi.feature} className="feature-bar">
                <span className="feature-name">{fi.feature}</span>
                <div className="feature-bar-track">
                  <div
                    className="feature-bar-fill"
                    style={{
                      width: `${Math.min(Math.abs(fi.importance) * 100, 100)}%`,
                      backgroundColor: fi.importance > 0 ? "#e74c3c" : "#3498db",
                    }}
                  />
                </div>
                <span className="feature-value">{fi.importance.toFixed(4)}</span>
              </div>
            ))
          ) : (
            <code>artifact unavailable</code>
          )}
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
              {item.knowledge_context && (
                <details className="rag-context">
                  <summary>Retrieved context</summary>
                  <pre>{item.knowledge_context}</pre>
                </details>
              )}
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function SeverityChart({ counts }: { counts: Record<string, number> }) {
  const max = Math.max(...Object.values(counts), 1);
  const colors: Record<string, string> = { High: "#e74c3c", Medium: "#f39c12", Low: "#3498db" };
  return (
    <div className="panel chart-panel">
      <h2>Severity Distribution</h2>
      {Object.entries(counts).map(([severity, count]) => (
        <div key={severity} className="chart-bar-row">
          <span className="chart-label">{severity}</span>
          <div className="chart-bar-track">
            <div
              className="chart-bar-fill"
              style={{ width: `${(count / max) * 100}%`, backgroundColor: colors[severity] || "#67e8f9" }}
            />
          </div>
          <span className="chart-value">{count}</span>
        </div>
      ))}
    </div>
  );
}

function ModelF1Chart({ metrics }: { metrics: ModelMetric[] }) {
  if (!metrics.length) return null;
  const max = Math.max(...metrics.map((m) => m.f1_score), 0.01);
  return (
    <div className="panel chart-panel">
      <h2>F1 Score by Model</h2>
      {metrics.map((m) => (
        <div key={`${m.dataset_id}-${m.model_name}`} className="chart-bar-row">
          <span className="chart-label">{m.model_name}</span>
          <div className="chart-bar-track">
            <div
              className="chart-bar-fill chart-fill-green"
              style={{ width: `${(m.f1_score / max) * 100}%` }}
            />
          </div>
          <span className="chart-value">{m.f1_score.toFixed(3)}</span>
        </div>
      ))}
    </div>
  );
}

function AttackTypeChart({ alerts }: { alerts: { attack_type: string }[] }) {
  const counts = alerts.reduce<Record<string, number>>((acc, a) => {
    acc[a.attack_type] = (acc[a.attack_type] || 0) + 1;
    return acc;
  }, {});
  const max = Math.max(...Object.values(counts), 1);
  return (
    <div className="panel chart-panel">
      <h2>Attack Types</h2>
      {Object.entries(counts).map(([type, count]) => (
        <div key={type} className="chart-bar-row">
          <span className="chart-label">{type}</span>
          <div className="chart-bar-track">
            <div
              className="chart-bar-fill chart-fill-purple"
              style={{ width: `${(count / max) * 100}%` }}
            />
          </div>
          <span className="chart-value">{count}</span>
        </div>
      ))}
    </div>
  );
}

function exportIncidentReport(alert: typeof sampleAlerts[0], explanation: Explanation | null) {
  const lines = [
    "# Incident Report",
    "",
    `**Alert ID**: ${alert.alert_id}`,
    `**Timestamp**: ${alert.timestamp}`,
    `**Attack Type**: ${alert.attack_type}`,
    `**Source**: ${alert.src_ip} → ${alert.dst_ip}`,
    `**Severity**: ${alert.severity}`,
    `**Confidence**: ${Math.round(alert.confidence * 100)}%`,
    `**MITRE ATT&CK**: ${alert.mitre_technique}`,
    `**Triage Priority**: ${alert.triage_priority}`,
    "",
    "## Analysis",
    "",
    explanation?.summary ?? alert.reason,
    "",
    "## Evidence Features",
    "",
    ...(explanation?.evidence_features ?? alert.top_features).map((f) => `- ${f}`),
    "",
    "## Recommended Response",
    "",
    ...(explanation?.recommended_response ?? ["Escalate to analyst review."]).map((r) => `- ${r}`),
    "",
    "## Provider",
    "",
    explanation?.provider ?? "local-template",
    "",
  ];
  const blob = new Blob([lines.join("\n")], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `incident-${alert.alert_id}.md`;
  a.click();
  URL.revokeObjectURL(url);
}

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

export default App;
