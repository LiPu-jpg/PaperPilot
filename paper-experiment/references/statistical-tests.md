# Statistical Tests Guide

Guide for selecting appropriate statistical tests for experiment analysis.

## Test Selection Flowchart

```
Is data paired? ──yes──> Is data normal? ──yes──> Paired t-test
      │                           │
      no                          no
      ▼                           ▼
Is there >2 groups? ──yes──> ANOVA
      │
      no
      ▼
Two groups? ──yes──> Is data normal? ──yes──> t-test
      │                           │
      no                          no
      ▼                           ▼
      └─────────────> Wilcoxon/Mann-Whitney
```

## Common Tests

### Parametric Tests

| Test | Use Case | Python |
|------|----------|--------|
| t-test (paired) | Compare means, same samples | `scipy.stats.ttest_rel` |
| t-test (unpaired) | Compare means, different samples | `scipy.stats.ttest_ind` |
| ANOVA | Compare ≥3 groups | `scipy.stats.f_oneway` |
| Pearson correlation | Linear relationship | `scipy.stats.pearsonr` |

### Non-Parametric Tests

| Test | Use Case | Python |
|------|----------|--------|
| Wilcoxon | Paired, non-normal | `scipy.stats.wilcoxon` |
| Mann-Whitney | Unpaired, non-normal | `scipy.stats.mannwhitneyu` |
| Kruskal | ≥3 groups, non-normal | `scipy.stats.kruskal` |
| Spearman | Monotonic relationship | `scipy.stats.spearmanr` |

## Multiple Comparison Correction

### Bonferroni
```python
from statsmodels.stats.multitest import multipletests
reject, pvals, _, _ = multipletests(p_values, alpha=0.05, method='bonferroni')
```

### Benjamini-Hochberg (FDR)
```python
reject, pvals, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
```

## Effect Size

### Cohen's d
- Small: 0.2
- Medium: 0.5
- Large: 0.8

### Pearson's r
- Small: 0.1
- Medium: 0.3
- Large: 0.5

## Confidence Intervals

```python
import numpy as np
from scipy import stats

def ci_mean(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    h = se * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean - h, mean + h

lower, upper = ci_mean(scores)
print(f"95% CI: [{lower:.4f}, {upper:.4f}]")
```

## Reporting Format

```
Results are reported as mean ± standard deviation.
Statistical significance was determined using [test name] with α=0.05.
Effect size is reported as Cohen's d = [value].
```

Example:
```
Our method achieves 89.2% accuracy (±1.3%), significantly outperforming
the baseline (85.1% ± 1.8%) with a paired t-test (t=4.21, p<0.001)
and a large effect size (d=0.94).
```
