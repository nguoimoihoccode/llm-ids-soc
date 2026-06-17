from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = PROJECT_ROOT / "data"
RAW_DATA_ROOT = DATA_ROOT / "raw"
PROCESSED_DATA_ROOT = DATA_ROOT / "processed"
MODELS_ROOT = PROJECT_ROOT / "models"
REPORTS_ROOT = PROJECT_ROOT / "reports"
KNOWLEDGE_BASE_ROOT = PROJECT_ROOT / "knowledge_base"
PLAYBOOKS_ROOT = KNOWLEDGE_BASE_ROOT / "playbooks"
