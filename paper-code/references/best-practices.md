# Code Best Practices

## Project Structure

```bash
project/
├── configs/           # Hyperparameters and settings
├── data/              # Raw and processed data
├── models/            # Model implementations
├── scripts/           # Training and evaluation scripts
├── notebooks/        # Exploratory analysis
├── tests/             # Unit and integration tests
└── logs/              # Experiment tracking
```

## Code Quality Standards

### Reproducibility
- **Random Seeds**: `torch.manual_seed()`, `numpy.random.seed()` for all experiments
- **Config Files**: All hyperparameters in `configs/`
- **Exact Commands**: Reproduce experiments with exact commands in logs
- **Environment Specs**: Document in `requirements.txt` (conda env, dependencies)

### Style
- **Naming**: snake_case for files, PascalCase for classes
- **Docstrings**: Google/NumPy style for all functions
- **Type Hints**: All function signatures include type hints

### Testing
- **Unit Tests**: Test core functions individually
- **Integration Tests**: Validate end-to-end workflows
- **Minimum Coverage**: 80% for core functions

## Common Script Usage

### Classification Experiment
```bash
python3 code-scaffold.py --project ./my-exp --exp_type classification
```

### Generation Experiment
```bash
python3 code-scaffold.py --project ./my-exp --exp_type generation
```

### RL Training
```bash
python3 code-scaffold.py --project ./my-exp --exp_type rl_training
```

## Directory Guidelines

### data/
- Raw data goes in `data/raw/`
- Processed data goes in `data/processed/`

### models/
- Baseline models in `models/baselines/`
- Training state checkpoints in `models/checkpoints/`

### configs/
- YAML format for hyperparameters
- Use separate files for different experiments

### notebooks/
- Exploratory analysis only
- Don't include in production runs

### logs/
- Log format: `timestamp | seed | command | results_path | metrics`
