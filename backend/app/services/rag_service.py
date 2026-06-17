from app.paths import PLAYBOOKS_ROOT


PLAYBOOK_DIR = PLAYBOOKS_ROOT


def retrieve_context(attack_type: str) -> str:
    # Ten file playbook duoc suy ra truc tiep tu loai tan cong.
    filename = attack_type.lower().replace(" ", "-") + ".md"
    path = PLAYBOOK_DIR / filename
    if not path.exists():
        return "No local playbook found. Use only the alert fields."
    return path.read_text(encoding="utf-8")
