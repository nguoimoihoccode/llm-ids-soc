from pydantic import BaseModel


class DatasetInfo(BaseModel):
    # Metadata co ban cho dataset trong demo.
    dataset_id: str
    name: str
    status: str
    source_url: str
    purpose: str


class PreprocessingSummary(BaseModel):
    # Tom tat ket qua xu ly du lieu de in ra sau khi preprocess.
    row_count: int
    feature_count: int
    label_column: str
    attack_categories: list[str]


class DatasetProfile(BaseModel):
    # Ho so dataset: kich thuoc, cot, phan bo label va muc lech lop.
    row_count: int
    column_count: int
    columns: list[str]
    label_distribution: dict[str, int]
    label_percentages: dict[str, float]
    label_imbalance_ratio: float
    attack_category_distribution: dict[str, int]
    attack_category_percentages: dict[str, float]
    attack_category_imbalance_ratio: float
    missing_value_count: int


class DatasetSplitSummary(BaseModel):
    # Tom tat sau khi tach train/test de biet so dong va label co can bang khong.
    total_rows: int
    train_rows: int
    test_rows: int
    label_column: str
    test_size: float
    random_state: int
    stratified: bool
    split_strategy: str
    train_label_distribution: dict[str, int]
    test_label_distribution: dict[str, int]


class DatasetValidationResult(BaseModel):
    valid: bool
    row_count: int
    column_count: int
    required_columns: list[str]
    missing_required_columns: list[str]
    errors: list[str]
