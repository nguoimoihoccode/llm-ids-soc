# Abstract

## English Abstract

Network intrusion detection is an important task in modern cybersecurity operations. Intrusion Detection Systems (IDS) and machine-learning-based detectors can identify suspicious network behavior, but their outputs are often difficult for Security Operations Center (SOC) analysts to interpret quickly. A detector may produce an attack label, probability score, or technical feature values, but analysts still need to understand why an event is suspicious, how serious it is, which attack technique it resembles, and what response actions should be considered.

This thesis proposes a research prototype that combines machine-learning-based intrusion detection, explainable alert intelligence, Retrieval-Augmented Generation (RAG), and Large Language Model (LLM)-style alert explanation. The system separates detection from explanation. The IDS and machine-learning layer is responsible for detection and measurable evaluation using structured network-flow data. The alert intelligence layer enriches detected events with severity, confidence, evidence features, MITRE ATT&CK mapping, and triage priority. The RAG/LLM layer then generates analyst-readable explanations and response recommendations using structured alert context and retrieved security playbooks.

The prototype is implemented as a modular application with a FastAPI backend, React/Vite SOC dashboard, preprocessing and model training scripts, local markdown playbooks, and reproducible report exports. It supports UNSW-NB15-style preprocessing, baseline model training using Logistic Regression, Decision Tree, and Random Forest, model metric export, confusion matrix figures, feature importance artifacts, explanation comparison, rubric-based LLM evaluation, RAG summary generation, and incident case study reports.

The current fixture-based evaluation validates the end-to-end workflow and demonstrates that the system can generate IDS alerts, enrich them with explainable context, compare explanation modes, and export thesis-supporting artifacts. The fixture results are not intended to represent final detection performance. Full experiments on public IDS datasets such as UNSW-NB15 and CICIDS2017 or CSE-CIC-IDS2018 are required for final empirical conclusions.

The main contribution of this work is an integrated and reproducible research prototype for SOC-style security alert analysis. The thesis argues that LLMs should not replace measurable IDS/ML detection mechanisms. Instead, LLMs are most useful as a controlled explanation and triage support layer when grounded by structured alert evidence and retrieved security knowledge.

## Vietnamese Abstract

Phát hiện xâm nhập mạng là một nhiệm vụ quan trọng trong vận hành an ninh mạng hiện đại. Các hệ thống phát hiện xâm nhập và các mô hình học máy có thể nhận diện hành vi mạng bất thường hoặc độc hại, nhưng kết quả đầu ra của chúng thường khó được phân tích nhanh bởi chuyên viên SOC. Một cảnh báo có thể chỉ cung cấp nhãn tấn công, điểm xác suất hoặc một số đặc trưng kỹ thuật, trong khi người phân tích vẫn cần hiểu vì sao sự kiện đó đáng nghi, mức độ nghiêm trọng ra sao, liên quan đến kỹ thuật tấn công nào và cần thực hiện phản ứng như thế nào.

Luận văn này đề xuất một nguyên mẫu nghiên cứu kết hợp phát hiện xâm nhập dựa trên học máy, lớp thông minh cảnh báo có khả năng giải thích, Retrieval-Augmented Generation (RAG) và giải thích cảnh báo theo phong cách mô hình ngôn ngữ lớn. Hệ thống tách biệt nhiệm vụ phát hiện và nhiệm vụ giải thích. Lớp IDS/học máy chịu trách nhiệm phát hiện và đánh giá bằng các thước đo định lượng trên dữ liệu network-flow có cấu trúc. Lớp thông minh cảnh báo bổ sung mức độ nghiêm trọng, độ tin cậy, đặc trưng bằng chứng, ánh xạ MITRE ATT&CK và mức ưu tiên xử lý. Sau đó, lớp RAG/LLM tạo giải thích dễ đọc cho người phân tích và đề xuất hướng phản ứng dựa trên ngữ cảnh cảnh báo có cấu trúc và playbook an ninh được truy xuất.

Nguyên mẫu được triển khai theo kiến trúc mô-đun gồm backend FastAPI, dashboard SOC dùng React/Vite, các script tiền xử lý và huấn luyện mô hình, playbook markdown cục bộ và các báo cáo có thể tái lập. Hệ thống hỗ trợ tiền xử lý theo phong cách UNSW-NB15, huấn luyện các mô hình baseline như Logistic Regression, Decision Tree và Random Forest, xuất metric mô hình, biểu đồ confusion matrix, artifact feature importance, so sánh các chế độ giải thích, đánh giá LLM bằng rubric, tạo báo cáo RAG summary và incident case study.

Đánh giá hiện tại dựa trên fixture dataset nhằm xác nhận workflow end-to-end và chứng minh rằng hệ thống có thể tạo cảnh báo IDS, bổ sung ngữ cảnh giải thích, so sánh các chế độ giải thích và xuất artifact phục vụ luận văn. Kết quả fixture không được dùng để kết luận hiệu năng phát hiện cuối cùng. Các thí nghiệm đầy đủ trên các bộ dữ liệu IDS công khai như UNSW-NB15 và CICIDS2017 hoặc CSE-CIC-IDS2018 là cần thiết để đưa ra kết luận thực nghiệm cuối cùng.

Đóng góp chính của luận văn là một nguyên mẫu nghiên cứu tích hợp và có khả năng tái lập cho phân tích cảnh báo an ninh theo phong cách SOC. Luận văn cho rằng LLM không nên thay thế cơ chế phát hiện IDS/học máy có thể đo lường được. Thay vào đó, LLM phù hợp nhất với vai trò hỗ trợ giải thích và triage khi được ràng buộc bởi bằng chứng cảnh báo có cấu trúc và tri thức an ninh được truy xuất.

## Keywords

- Intrusion Detection System
- Machine Learning
- Network Security
- Security Operations Center
- Explainable AI
- Large Language Model
- Retrieval-Augmented Generation
- MITRE ATT&CK
- Alert Triage
- Cybersecurity

## Contribution Summary

This thesis contributes:

1. A reproducible research prototype for ML-based network intrusion detection and security alert analysis.
2. An alert intelligence layer that enriches IDS alerts with evidence features, severity, confidence, MITRE mapping, and triage priority.
3. A RAG-grounded LLM-style explanation workflow for generating analyst-readable alert explanations and response recommendations.
4. A rubric-based evaluation workflow for comparing template, no-RAG, and RAG-assisted explanation modes.
5. A SOC-style dashboard and exported evaluation artifacts that support experimentation, thesis writing, and defense demonstration.
