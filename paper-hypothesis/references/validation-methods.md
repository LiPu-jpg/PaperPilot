# Validation Methods

## Validation Approaches by Discipline

### Quantitative Methods

#### Statistical Significance Testing
- **t-test**: Compare means between two groups
  - Use case: comparing two approaches
  - Requirements: Normal distribution, equal variance
  - Significance level: p < 0.05

- **ANOVA**: Compare means across multiple groups
  - Use case: comparing multiple algorithms
  - Requirements: Normal distribution, equal variance
  - Post-hoc tests: Tukey HSD, Bonferroni correction

- **Effect Size**: Cohen's d, partial eta squared
  - Use case: Small, medium, large
  - Interpretation: 0.2=small, 0.5=medium, 0.8=large

- **Correlation Analysis**
  - Pearson correlation coefficient
  - Use case: Relationship between variables
  - Significance: p < 0.05 or |r| > 0.5

#### Validation Metrics for ML
- **Accuracy**: Percentage of correct predictions
  - Baselines: 70% accuracy for simple tasks

- **Precision/Recall/F1-score**
  - Precision = TP / (TP + FP)
  - Recall = TP / (TP + FN)
  - F1 = 2 * (Precision * Recall) / (Precision + Recall)

- **Confusion Matrix**: True positives, false positives, etc.
  - Use case: Binary or multi-class classification

### Qualitative Methods

#### Content Analysis
- **Thematic Analysis**: Code responses and identify themes
  - Use case: Categorize open-ended responses
  - Validation: Inter-rater reliability >= 0.7

- **Discourse Analysis**: Analyze language patterns
  - Use case: Identify rhetorical strategies

#### Experimental Validation
- **A/B Testing**: Compare different treatments
  - Use case: Random assignment to groups
  - Validation: Statistical significance

- **User Studies**: Field validation of claims
  - Use case: Longitudinal observation

## Validation Workflow

### 1. Pre-Registration (Optional)
- Register hypotheses before data collection
- Declare primary outcomes
- Prevents HARKing (hypothesizing after results)
- Increases credibility and reduces bias

### 2. Data Collection
- Collect empirical data to test predictions
- Ensure sufficient sample size (power analysis)
- Control for confounding variables
- Maintain data quality and reproducibility

### 3. Analysis
- Apply appropriate statistical tests
- Check assumptions (normality, equal variance)
- Report effect sizes and confidence intervals
- Visualize results with appropriate plots

### 4. Conclusion
- Support or refute hypothesis based on evidence
- Document limitations and boundary conditions
- Suggest follow-up studies

## Common Validation Pitfalls

### P-hacking
- **Definition**: Testing multiple hypotheses without correction
- **Consequence**: Inflated false positive rate
- **Prevention**: Pre-register all hypotheses
- **Example**: Testing H1, H2, H3 simultaneously
- **Best Practice**: Sequential testing with holdout set

### Confirmation Bias
- **Definition**: Interpreting ambiguous results as supportive
- **Consequence**: Flawed research
- **Prevention**: Blind analysis procedures
- **Best Practice**: Use statistical criteria, avoid subjective interpretation

### Insufficient Sample Size
- **Definition**: Sample too small to detect effect
- **Consequence**: Type II error (false negative)
- **Prevention**: Power analysis before data collection
- **Guideline**: Minimum 80% power at 0.05 significance

### Multiple Comparisons
- **Definition**: Testing many comparisons increases false positive rate
- **Consequence**: Spurious findings
- **Prevention**: Use adjustment methods (Bonferroni, FDR)
- **Best Practice**: Focus on primary comparisons, limit exploratory tests

## Discipline-Specific Validation

### Computer Science
- **Cross-validation**: K-fold for ML models
- **Ablation studies**: Remove components to test individual contributions
- **Reproducibility**: Share code and data

### Biomedical
- **Clinical trials**: Multi-center, randomized controlled
- **Meta-analysis**: Combine results from multiple studies

### Psychology
- **Replication**: Independent replication of key findings
- **Pre-registered protocols**: OSF, clinicaltrials.gov

## Sample Size Calculators

### Simple Calculator
```
Power = 0.8 (medium effect)
Alpha = 0.05
Required n = (Z_alpha + Z_beta)^2 * Effect^2 / (2 * SD^2)
      where Z_beta = 1.96 for 80% power
```

### Online Calculators
- G*Power: https://www.ncbi.nlm.nih.gov/tools/power/
- SOCR Calculator: https://www.danielsoper.com/rma/calculator/
