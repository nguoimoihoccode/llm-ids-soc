from app.models import Alert, Explanation, ExplanationComparison, ExplanationComparisonItem
from app.config import settings
from app.services.rag_service import retrieve_context


def explain_alert(alert: Alert) -> Explanation:
    # Tao phan giai thich doc duoc boi con nguoi, co context playbook kem theo.
    context = retrieve_context(alert.attack_type)
    return Explanation(
        alert_id=alert.alert_id,
        provider=settings.llm_provider,
        summary=(
            f"Alert {alert.alert_id} indicates possible {alert.attack_type} activity "
            f"from {alert.src_ip} to {alert.dst_ip} with {alert.confidence:.0%} confidence. "
            f"Mapped to {alert.mitre_technique} and triaged as {alert.triage_priority}."
        ),
        why_suspicious=alert.reason,
        evidence_features=alert.top_features,
        mitre_technique=alert.mitre_technique,
        triage_priority=alert.triage_priority,
        recommended_response=_recommendations(alert.attack_type),
        knowledge_context=context,
    )


def compare_explanation_modes(alert: Alert) -> ExplanationComparison:
    # Cho xem cung 1 alert se duoc trinh bay khac nhau nhu the nao khi co/khong co RAG.
    rag_context = retrieve_context(alert.attack_type)
    return ExplanationComparison(
        alert_id=alert.alert_id,
        comparisons=[
            ExplanationComparisonItem(
                mode="template",
                uses_rag=False,
                summary=f"{alert.attack_type} alert with {alert.severity} severity and {alert.confidence:.0%} confidence.",
                knowledge_context="",
            ),
            ExplanationComparisonItem(
                mode="llm_without_rag",
                uses_rag=False,
                summary=(
                    f"Possible {alert.attack_type} from {alert.src_ip} to {alert.dst_ip}. "
                    f"Evidence features: {', '.join(alert.top_features)}. MITRE mapping: {alert.mitre_technique}."
                ),
                knowledge_context="",
            ),
            ExplanationComparisonItem(
                mode="llm_with_rag",
                uses_rag=True,
                summary=(
                    f"Possible {alert.attack_type} from {alert.src_ip} to {alert.dst_ip}, triaged as {alert.triage_priority}. "
                    f"Grounded by retrieved playbook context and evidence features: {', '.join(alert.top_features)}."
                ),
                knowledge_context=rag_context,
            ),
        ],
    )


def _recommendations(attack_type: str) -> list[str]:
    # Khuyen nghi xu ly duoc chon theo loai attack, de khop nghiep vu SOC.
    if attack_type == "Brute Force":
        return [
            "Block or rate-limit the source IP.",
            "Check for successful login after repeated failures.",
            "Enable MFA and review password policy.",
        ]
    if attack_type == "DDoS":
        return [
            "Apply rate limiting or upstream filtering.",
            "Check service latency and availability.",
            "Preserve flow evidence for incident review.",
        ]
    if attack_type == "Port Scan":
        return [
            "Identify scanned hosts and exposed services.",
            "Block repeated scanner IPs.",
            "Review follow-up exploitation attempts.",
        ]
    return ["Escalate alert to analyst review."]
