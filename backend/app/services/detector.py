from app.models import Alert, NetworkEvent


def generate_alerts(events: list[NetworkEvent]) -> list[Alert]:
    alerts: list[Alert] = []
    for event in events:
        if event.label.lower() != "attack":
            continue
        alerts.append(_event_to_alert(event))
    return alerts


def _event_to_alert(event: NetworkEvent) -> Alert:
    confidence = _confidence(event)
    severity = _severity(event.attack_type, confidence)
    return Alert(
        alert_id=f"alert-{event.event_id}",
        event_id=event.event_id,
        timestamp=event.timestamp,
        src_ip=event.src_ip,
        dst_ip=event.dst_ip,
        attack_type=event.attack_type,
        severity=severity,
        confidence=confidence,
        reason=_reason(event),
        top_features=_top_features(event),
        mitre_technique=_mitre_technique(event.attack_type),
        triage_priority=_triage_priority(severity, confidence),
    )


def _confidence(event: NetworkEvent) -> float:
    if event.attack_type == "Brute Force" and event.failed_login_count >= 50:
        return 0.94
    if event.attack_type == "DDoS" and event.flow_packets_s >= 1000:
        return 0.92
    if event.attack_type == "Port Scan" and event.dst_port <= 1024:
        return 0.86
    return 0.75


def _severity(attack_type: str, confidence: float) -> str:
    if attack_type in {"DDoS", "Brute Force"} and confidence >= 0.9:
        return "High"
    if attack_type == "Port Scan":
        return "Medium"
    return "Low"


def _reason(event: NetworkEvent) -> str:
    if event.attack_type == "Brute Force":
        return f"{event.failed_login_count} failed login attempts against port {event.dst_port}."
    if event.attack_type == "DDoS":
        return f"High packet rate of {event.flow_packets_s} packets/s targeting port {event.dst_port}."
    if event.attack_type == "Port Scan":
        return f"Connection probing detected against low-numbered port {event.dst_port}."
    return "Traffic matched attack-labeled IDS pattern."


def _top_features(event: NetworkEvent) -> list[str]:
    if event.attack_type == "Brute Force":
        return ["failed_login_count", "dst_port", "flow_packets_s"]
    if event.attack_type == "DDoS":
        return ["flow_packets_s", "total_fwd_packets", "flow_bytes_s"]
    if event.attack_type == "Port Scan":
        return ["syn_flag_count", "dst_port", "flow_duration_ms"]
    return ["label", "attack_type", "confidence"]


def _mitre_technique(attack_type: str) -> str:
    mapping = {
        "Brute Force": "T1110 - Brute Force",
        "DDoS": "T1498 - Network Denial of Service",
        "Port Scan": "T1046 - Network Service Discovery",
    }
    return mapping.get(attack_type, "Unmapped")


def _triage_priority(severity: str, confidence: float) -> str:
    if severity == "High" and confidence >= 0.9:
        return "P1"
    if severity in {"High", "Medium"}:
        return "P2"
    return "P3"
