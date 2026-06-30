from app.models import Alert, Explanation, ExplanationComparison, ExplanationComparisonItem
from app.config import settings
from app.services.rag_service import retrieve_context
from app.services.llm_provider import get_llm_provider


def _build_provider():
    return get_llm_provider(
        provider=settings.llm_provider,
        openai_api_key=settings.openai_api_key or None,
        openai_model=settings.openai_model,
        gemini_api_key=settings.gemini_api_key or None,
        gemini_model=settings.gemini_model,
        ollama_model=settings.ollama_model,
        ollama_base_url=settings.ollama_base_url,
    )


def _explanation_prompt(alert: Alert, context: str, mode: str) -> str:
    context_block = ""
    if context and context.strip():
        context_block = f"\nRelevant security playbook context:\n{context}\n"

    prompt = (
        f"You are a SOC analyst assistant. Explain the following IDS alert in plain language "
        f"that a junior analyst can understand.\n\n"
        f"Alert ID: {alert.alert_id}\n"
        f"Attack type: {alert.attack_type}\n"
        f"Source IP: {alert.src_ip} → Destination IP: {alert.dst_ip}\n"
        f"Severity: {alert.severity}\n"
        f"Confidence: {alert.confidence:.0%}\n"
        f"Evidence features: {', '.join(alert.top_features)}\n"
        f"MITRE ATT&CK: {alert.mitre_technique}\n"
        f"Triage priority: {alert.triage_priority}\n"
        f"Detection reason: {alert.reason}\n"
        f"{context_block}"
        f"\nProvide:\n"
        f"1. Summary: what happened in 1-2 sentences.\n"
        f"2. Why it is suspicious.\n"
        f"3. Recommended response actions.\n"
    )
    return prompt


def explain_alert(alert: Alert) -> Explanation:
    provider = _build_provider()
    context = retrieve_context(alert.attack_type)
    prompt = _explanation_prompt(alert, context, "rag")
    llm_output = provider.generate(prompt)

    return Explanation(
        alert_id=alert.alert_id,
        provider=provider.provider_name,
        summary=llm_output,
        why_suspicious=alert.reason,
        evidence_features=alert.top_features,
        mitre_technique=alert.mitre_technique,
        triage_priority=alert.triage_priority,
        recommended_response=_recommendations(alert.attack_type),
        knowledge_context=context,
    )


def compare_explanation_modes(alert: Alert) -> ExplanationComparison:
    provider = _build_provider()
    rag_context = retrieve_context(alert.attack_type)

    template_summary = (
        f"{alert.attack_type} alert from {alert.src_ip} to {alert.dst_ip} "
        f"with {alert.severity} severity and {alert.confidence:.0%} confidence."
    )

    no_rag_prompt = _explanation_prompt(alert, "", "no-rag")
    no_rag_summary = provider.generate(no_rag_prompt)

    rag_prompt = _explanation_prompt(alert, rag_context, "rag")
    rag_summary = provider.generate(rag_prompt)

    return ExplanationComparison(
        alert_id=alert.alert_id,
        comparisons=[
            ExplanationComparisonItem(
                mode="template",
                uses_rag=False,
                summary=template_summary,
                knowledge_context="",
            ),
            ExplanationComparisonItem(
                mode="llm_without_rag",
                uses_rag=False,
                summary=no_rag_summary,
                knowledge_context="",
            ),
            ExplanationComparisonItem(
                mode="llm_with_rag",
                uses_rag=True,
                summary=rag_summary,
                knowledge_context=rag_context,
            ),
        ],
    )


def _recommendations(attack_type: str) -> list[str]:
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
