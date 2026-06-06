from app.services.datasets import list_datasets


def test_dataset_registry_lists_research_datasets() -> None:
    datasets = list_datasets()
    dataset_ids = [dataset.dataset_id for dataset in datasets]

    assert dataset_ids == ["sample", "unsw-nb15", "cicids2017"]
    assert datasets[0].status == "ready"
    assert datasets[1].status == "planned"
    assert datasets[2].status == "planned"
