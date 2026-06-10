import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

type Alert = {
  alert_id: string;
  timestamp: string;
  src_ip: string;
  dst_ip: string;
  attack_type: string;
  severity: string;
  confidence: number;
  reason: string;
  top_features: string[];
  mitre_technique: string;
  triage_priority: string;
};

type Evaluation = {
  model_name: string;
  sample_count: number;
  accuracy: number;
  attack_recall: number;
  benign_recall: number;
};

type Explanation = {
  alert_id: string;
  provider: string;
  summary: string;
  why_suspicious: string;
  evidence_features: string[];
  mitre_technique: string;
  triage_priority: string;
  recommended_response: string[];
};

type ExplanationComparisonItem = {
  mode: string;
  uses_rag: boolean;
  summary: string;
  knowledge_context: string;
};

type ExplanationComparison = {
  alert_id: string;
  comparisons: ExplanationComparisonItem[];
};

type ModelMetric = {
  model_name: string;
  dataset_id: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  false_positive_rate: number;
};

const sampleAlerts: Alert[] = [
  {
    alert_id: "alert-evt-002",
    timestamp: "2026-06-03T09:02:05Z",
    src_ip: "192.168.1.45",
    dst_ip: "10.0.0.8",
    attack_type: "Brute Force",
    severity: "High",
    confidence: 0.94,
    reason: "80 failed login attempts against port 22.",
    top_features: ["failed_login_count", "dst_port", "flow_packets_s"],
    mitre_technique: "T1110 - Brute Force",
    triage_priority: "P1",
  },
  {
    alert_id: "alert-evt-003",
    timestamp: "2026-06-03T09:04:31Z",
    src_ip: "172.16.4.20",
    dst_ip: "10.0.0.12",
    attack_type: "DDoS",
    severity: "High",
    confidence: 0.92,
    reason: "High packet rate targeting web service.",
    top_features: ["flow_packets_s", "total_fwd_packets", "flow_bytes_s"],
    mitre_technique: "T1498 - Network Denial of Service",
    triage_priority: "P1",
  },
];

function App() {
  // Frontend uu tien du lieu that tu backend, neu loi thi dung sample fallback.
  const [alerts, setAlerts] = useState<Alert[]>(sampleAlerts);
  const [evaluation, setEvaluation] = useState<Evaluation | null>(null);
  const [explanation, setExplanation] = useState<Explanation | null>(null);
  const [comparison, setComparison] = useState<ExplanationComparison | null>(null);
  const [modelMetrics, setModelMetrics] = useState<ModelMetric[]>([]);
  const selected = alerts[0];

  useEffect(() => {
    async function loadDashboard() {
      try {
        // Lay dong thoi alert, evaluation va metric de dashboard co du lieu day du.
        const [alertsResponse, evaluationResponse, metricsResponse] = await Promise.all([
          fetch("http://localhost:8000/alerts"),
          fetch("http://localhost:8000/ml/evaluate"),
          fetch("http://localhost:8000/ml/metrics"),
        ]);
        const nextAlerts = (await alertsResponse.json()) as Alert[];
        const nextEvaluation = (await evaluationResponse.json()) as Evaluation;
        const nextModelMetrics = (await metricsResponse.json()) as ModelMetric[];
        setAlerts(nextAlerts);
        setEvaluation(nextEvaluation);
        setModelMetrics(nextModelMetrics);

        if (nextAlerts[0]) {
          // Chi can mot alert dau tien de minh hoa phan giai thich va comparison.
          const explanationResponse = await fetch(
            `http://localhost:8000/alerts/${nextAlerts[0].alert_id}/explanation`,
          );
          setExplanation((await explanationResponse.json()) as Explanation);
          const comparisonResponse = await fetch(
            `http://localhost:8000/alerts/${nextAlerts[0].alert_id}/explanation/comparison`,
          );
          setComparison((await comparisonResponse.json()) as ExplanationComparison);
        }
      } catch {
        // Neu backend chua chay, hien du lieu mau de giao dien van demo duoc.
        setEvaluation({
          model_name: "RuleBasedBaseline",
          sample_count: 5,
          accuracy: 1,
          attack_recall: 1,
          benign_recall: 1,
        });
        setModelMetrics([
          { model_name: "logistic_regression", dataset_id: "fixture", accuracy: 1, precision: 1, recall: 1, f1_score: 1, false_positive_rate: 0 },
          { model_name: "decision_tree", dataset_id: "fixture", accuracy: 1, precision: 1, recall: 1, f1_score: 1, false_positive_rate: 0 },
          { model_name: "random_forest", dataset_id: "fixture", accuracy: 1, precision: 1, recall: 1, f1_score: 1, false_positive_rate: 0 },
        ]);
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

createRoot(document.getElementById("root")!).render(<App />);
