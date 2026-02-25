---
name: paper-experiment
description: Use when running experiments, analyzing results, designing comparative experiments, or validating findings
---

# Paper Experiment

Execute experiments, analyze results, and validate findings with statistical rigor.

## Experiment Workflow

1. **Design** → Define hypotheses, metrics, baselines
2. **Execute** → Run experiments with logging
3. **Analyze** → Statistical tests, visualization
4. **Validate** → Reproduce key results, check robustness

## Metrics Selection

### Common ML Metrics
| Task | Metrics |
|------|---------|
| Classification | Accuracy, F1, AUC, Precision, Recall |
| Generation | BLEU, ROUGE, METEOR, BERTScore |
| QA | EM, F1 |
| Regression | MSE, MAE, R² |

### Statistical Tests
- **t-test**: Compare two means
- **ANOVA**: Compare multiple groups
- **Wilcoxon**: Paired non-parametric
- **Bonferroni**: Multiple comparison correction

## Results Analysis

### Visualization
- Learning curves (train/val over epochs)
- Bar charts for comparative results
- Confidence intervals / error bars
- Confusion matrices

### Tables
- Main results with statistical significance (* p<0.05)
- Ablation studies
- Hyperparameter sensitivity
- Runtime / resource comparisons

## Scripts

### experiment-runner.py
- Grid search and random search
- Parallel experiment execution
- Checkpointing and resume

### results-analyzer.py
- Auto-generate tables and figures
- Statistical significance testing
- Result aggregation from multiple runs

## Tips

- Run baseline first to establish comparison
- Save all intermediate results, not just final
- Check for statistical significance, not just improvement magnitude
- Document any unexpected observations
