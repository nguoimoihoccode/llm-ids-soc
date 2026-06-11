# Dataset Source And Validation Guide

This project supports IDS-style CSV datasets for thesis experiments. Raw benchmark files should stay local and should not be committed to git.

## Supported Datasets

| Dataset | Status | Notes |
| --- | --- | --- |
| Sample fixture | Ready | Tiny UNSW-NB15-style CSV for pipeline tests only. |
| UNSW-NB15 | Planned full experiment | Use official CSV files, then validate before preprocessing. |
| CICIDS2017 or CSE-CIC-IDS2018 | Planned full experiment | May require column normalization before using the current UNSW-style preprocessing path. |

## Raw Data Placement

Place downloaded benchmark files under `data/raw/`:

```text
data/raw/UNSW_NB15_training-set.csv
data/raw/UNSW_NB15_testing-set.csv
data/raw/CICIDS2017_*.csv
```

`data/raw/` is ignored by git because these files are large and often subject to dataset license terms.

## Minimum CSV Requirements

The current validation step expects these columns:

- `label`: binary benign/attack target.
- `attack_cat`: attack family/category label.

The UNSW-style preprocessing path also benefits from flow/protocol fields such as `proto`, `service`, `state`, and numeric traffic features.

## Validate Before Pipeline

Run validation before profiling, splitting, preprocessing, or training:

```bash
backend/.venv/bin/python scripts/validate_dataset.py \
  --input data/raw/UNSW_NB15_training-set.csv \
  --output reports/evaluation/unsw-nb15-validation.json \
  --min-rows 1000
```

The command writes JSON with row count, column count, required columns, missing columns, and errors. It exits with status `1` when validation fails.

## Recommended Research Workflow

1. Download the benchmark dataset from its official source.
2. Store raw CSV files under `data/raw/`.
3. Run `scripts/validate_dataset.py`.
4. Run `scripts/profile_dataset.py` to inspect class balance and missing values.
5. Run `scripts/run_dataset_pipeline.py` with explicit `--dataset-id` and output directory.
6. Use generated reports and figures in thesis chapters only after confirming the dataset source, split strategy, and metric definitions.

## Reporting Notes

Use fixture results only to prove the pipeline runs. Do not report fixture metrics as research performance. Full thesis results should come from complete benchmark datasets with documented train/test split, preprocessing, model versions, and random seed.
