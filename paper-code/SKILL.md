---
name: paper-code
description: Use when implementing experimental code, scaffolding research projects, or following coding best practices for academic work
---

# Paper Code

Implement experimental code following best practices for reproducibility and academic standards.

## Project Structure

```
project/
├── configs/           # Hyperparameters, settings
├── data/              # Raw and processed data
├── models/            # Model implementations
├── scripts/           # Training and evaluation scripts
├── notebooks/        # Exploratory analysis
├── tests/             # Unit and integration tests
├── logs/              # Experiment tracking
└── README.md          # Documentation
```

## Code Quality Standards

### Reproducibility
- Fixed random seeds (torch.manual_seed, numpy.random.seed)
- Config files for all hyperparameters
- Exact command reproduction in logs
- Environment specification (requirements.txt, conda env)

### Style
- Clear variable and function names
- Comprehensive docstrings (Google/NumPy style)
- Type hints for function signatures
- Modular, reusable components

### Testing
- Test core functions individually
- Validate data preprocessing pipelines
- Check metric calculations match paper definitions

## Scripts

### code-scaffold.py
Generate project templates for common experiment types:
- Classification experiments
- Generation experiments
- RL training loops
- Baseline implementations
## References

- `references/best-practices.md`: Code quality standards and project structure

### code-validator.py
Check code quality:
- Linting (flake8, black)
- Type checking (mypy)
- Import validation

## Tips

- Start with a working baseline, then modify
- Keep experiment configs versioned
- Log everything (parameters, seeds, results)
- Use Weights & Biases or MLflow for tracking
