import csv
from pathlib import Path

from app.models import NetworkEvent


SAMPLE_DATA_PATH = Path(__file__).resolve().parents[3] / "data" / "samples" / "network_events.csv"


def load_sample_events(path: Path = SAMPLE_DATA_PATH) -> list[NetworkEvent]:
    with path.open(newline="", encoding="utf-8") as file:
        rows = csv.DictReader(file)
        return [NetworkEvent(**_coerce_row(row)) for row in rows]


def _coerce_row(row: dict[str, str]) -> dict[str, object]:
    int_fields = {
        "src_port",
        "dst_port",
        "flow_duration_ms",
        "total_fwd_packets",
        "total_bwd_packets",
        "syn_flag_count",
        "failed_login_count",
    }
    float_fields = {"flow_bytes_s", "flow_packets_s"}
    coerced: dict[str, object] = {}
    for key, value in row.items():
        if key in int_fields:
            coerced[key] = int(value)
        elif key in float_fields:
            coerced[key] = float(value)
        else:
            coerced[key] = value
    return coerced
