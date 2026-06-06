from app.models import DatasetInfo


def list_datasets() -> list[DatasetInfo]:
    return [
        DatasetInfo(
            dataset_id="sample",
            name="Sample Network Events",
            status="ready",
            source_url="local sample data",
            purpose="Deterministic MVP demo and smoke tests.",
        ),
        DatasetInfo(
            dataset_id="unsw-nb15",
            name="UNSW-NB15",
            status="planned",
            source_url="https://research.unsw.edu.au/projects/unsw-nb15-dataset",
            purpose="Primary thesis dataset for reproducible ML IDS experiments.",
        ),
        DatasetInfo(
            dataset_id="cicids2017",
            name="CICIDS2017",
            status="planned",
            source_url="https://www.unb.ca/cic/datasets/ids-2017.html",
            purpose="Secondary benchmark for cross-dataset validation.",
        ),
    ]
