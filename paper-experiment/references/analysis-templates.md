# Analysis Templates

Templates for common experiment analysis tasks.

## Result Table Template

```markdown
| Model | Metric 1 | Metric 2 | Metric 3 |
|-------|----------|----------|----------|
| Baseline | 0.850 | 0.820 | 0.870 |
| Ours | **0.890** | **0.860** | **0.910** |
| Δ | +4.0% | +4.9% | +4.6% |
```

Statistical significance: * p<0.05, ** p<0.01

## Ablation Study Template

```markdown
| Configuration | Val Acc | Test Acc |
|--------------|---------|----------|
| Full Model | 92.1 | 91.5 |
| - Component A | 90.3 | 89.8 |
| - Component B | 89.7 | 89.2 |
| - Both | 87.5 | 87.1 |
```

## Learning Curve Template

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 101)
train_loss = ...  # your data
val_loss = ...

plt.figure(figsize=(10, 6))
plt.plot(epochs, train_loss, label='Train', marker='o', markersize=3)
plt.plot(epochs, val_loss, label='Validation', marker='s', markersize=3)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Curves')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('learning_curves.pdf', dpi=300, bbox_inches='tight')
```

## Error Analysis Template

```python
# Top-K Error Analysis
for k in [1, 5, 10]:
    correct = sum(1 for pred, label in zip(top_k_preds, labels) if label in pred[:k])
    accuracy = correct / len(labels)
    print(f"Top-{k}: {accuracy:.4f}")

# Confusion Matrix
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(labels, predictions)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.savefig('confusion_matrix.pdf')
```

## Statistical Significance Template

```python
from scipy import stats

# Paired t-test (for same dataset, different models)
t_stat, p_value = stats.ttest_rel(model_a_scores, model_b_scores)
print(f"t={t_stat:.3f}, p={p_value:.4f}")

# Wilcoxon signed-rank (non-parametric)
w_stat, p_value = stats.wilcoxon(model_a_scores, model_b_scores)
print(f"W={w_stat:.3f}, p={p_value:.4f}")

# Effect size (Cohen's d)
def cohens_d(x, y):
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x)**2 + (ny-1)*np.std(y)**2) / dof)
```
