# Architecture Diagrams

These Mermaid diagrams can be used in the thesis, slides, or documentation. They describe the research prototype at three levels: system architecture, evaluation pipeline, and SOC analyst workflow.

## 1. System Architecture

```mermaid
flowchart TD
    A[Network-flow CSV data] --> B[Preprocessing Module]
    B --> C[IDS / ML Detection Layer]
    C --> D[Alert Generator]
    D --> E[Alert Intelligence Layer]
    E --> F[FastAPI Backend]
    F --> G[React SOC Dashboard]

    E --> H[RAG Retrieval Module]
    H --> I[Security Playbooks / MITRE Notes]
    I --> H
    H --> J[LLM Explanation Layer]
    E --> J
    J --> F

    C --> K[Model Metrics Artifacts]
    K --> L[Reports and Figures]
    J --> M[LLM Evaluation Artifacts]
    M --> L

    subgraph Detection
        B
        C
        D
    end

    subgraph Explanation
        E
        H
        I
        J
    end

    subgraph Presentation
        F
        G
    end

    subgraph Evaluation
        K
        M
        L
    end
```

## 2. Data And Model Evaluation Pipeline

```mermaid
flowchart LR
    A[Raw IDS Dataset<br/>UNSW-NB15 / CICIDS2017] --> B[Clean NaN and Infinity]
    B --> C[Encode categorical fields]
    C --> D[Processed CSV]
    D --> E[Train models]
    E --> F[Logistic Regression]
    E --> G[Decision Tree]
    E --> H[Random Forest]

    F --> I[Metrics JSON]
    G --> I
    H --> I

    I --> J[Model comparison CSV]
    I --> K[Confusion matrix SVG]
    H --> L[Feature importance CSV]
    G --> L

    J --> M[Thesis evaluation tables]
    K --> M
    L --> M
```

## 3. Alert Explanation And LLM Evaluation Pipeline

```mermaid
flowchart TD
    A[IDS Alert] --> B[Alert Intelligence]
    B --> C[Top Features]
    B --> D[MITRE Technique]
    B --> E[Triage Priority]

    C --> F[Explanation Comparison]
    D --> F
    E --> F

    F --> G[Template Explanation]
    F --> H[LLM Without RAG]
    F --> I[LLM With RAG]

    J[Security Playbooks] --> K[RAG Context]
    K --> I

    G --> L[Rubric Evaluation]
    H --> L
    I --> L

    L --> M[LLM Rubric Scores CSV]
    M --> N[RAG vs No-RAG Summary]
    M --> O[Incident Case Studies]
```

## 4. SOC Analyst Workflow

```mermaid
sequenceDiagram
    participant Analyst
    participant Dashboard
    participant API as FastAPI Backend
    participant IDS as IDS / Alert Engine
    participant RAG as RAG Playbooks
    participant LLM as LLM Explanation Layer

    Analyst->>Dashboard: Open SOC dashboard
    Dashboard->>API: GET /alerts
    API->>IDS: Generate alerts from events
    IDS-->>API: Enriched alerts
    API-->>Dashboard: Alerts with severity, confidence, MITRE, priority

    Analyst->>Dashboard: Select alert
    Dashboard->>API: GET /alerts/{id}/explanation
    API->>RAG: Retrieve playbook context
    RAG-->>API: Relevant response guidance
    API->>LLM: Build grounded explanation
    LLM-->>API: Summary and recommendations
    API-->>Dashboard: Explanation and evidence

    Analyst->>Dashboard: Compare explanation modes
    Dashboard->>API: GET /alerts/{id}/explanation/comparison
    API-->>Dashboard: Template vs no-RAG vs RAG outputs
```

## Thesis Figure Usage Notes

- Use **System Architecture** in Chapter 3: Proposed System.
- Use **Data And Model Evaluation Pipeline** in Chapter 4 or 5: Implementation and Experiments.
- Use **Alert Explanation And LLM Evaluation Pipeline** in Chapter 5: LLM/RAG evaluation.
- Use **SOC Analyst Workflow** in the demo slides to explain the end-to-end analyst interaction.

## Scope Boundary For Figures

The diagrams intentionally show an offline research prototype. They do not claim production realtime packet capture, automatic containment, or full SIEM/SOAR integration.
