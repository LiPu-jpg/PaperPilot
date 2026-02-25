# Section Templates

Section outlines and writing templates for different paper types.

## Machine Learning/NLP Paper

### Abstract
```
[Problem] [Method] [Results] [Conclusion]

[150-300 words]
- Background: 1-2 sentences
- Problem: What gap exists?
- Method: What do you propose?
- Results: Key quantitative findings
- Conclusion: 1-2 sentences on significance
```

### Introduction
```
1. Background (2-3 paragraphs)
   - General context
   - Specific problem area
   - Current state of art

2. Problem Statement (1 paragraph)
   - What gap exists?
   - Why is it important?
   - What are limitations of existing work?

3. Contributions (1 paragraph, bulleted)
   - Novel method/architecture
   - Theoretical analysis
   - Empirical findings
   - Resources (code, data)
```

### Method
```
1. Overview (1 paragraph + diagram)
   - High-level architecture
   - Pipeline/workflow

2. Background/Preliminaries (1-2 paragraphs)
   - Define notation
   - Related methods (brief)

3. Proposed Method (2-4 paragraphs)
   - Core components
   - Technical details
   - Variants/ablations

4. Training/Setup (1-2 paragraphs)
   - Loss functions
   - Optimization
   - Hyperparameters
```

### Experiments
```
1. Setup (1-2 paragraphs)
   - Datasets
   - Baselines
   - Metrics

2. Main Results (1-2 paragraphs + table)
   - Quantitative comparison
   - Statistical significance

3. Ablation Studies (1-2 paragraphs + table)
   - Component analysis
   - Hyperparameter sensitivity

4. Qualitative Analysis (1-2 paragraphs + figures)
   - Examples
   - Error analysis
   - Visualizations
```

### Related Work
```
[Organize by topic/approach, not by paper]

1. Topic A (1-2 paragraphs)
   - Summary of approaches
   - Relation to your work

2. Topic B (1-2 paragraphs)
   ...
```

### Conclusion
```
1. Summary (1-2 paragraphs)
   - Restate contributions
   - Key findings

2. Limitations (1 paragraph)
   - Honest assessment

3. Future Work (1 paragraph)
   - Extensions
   - Open questions
```

## System Paper

### Abstract
```
[Context] [Challenge] [Solution] [Results]

- Problem domain
- Key challenge
- Your approach/system
- Performance improvements
```

### Introduction
```
1. Problem Domain (2-3 paragraphs)
   - Why it matters
   - Current approaches

2. Challenges (1-2 paragraphs)
   - Technical challenges
   - Trade-offs

3. Contributions (bulleted)
   - System design
   - Novel techniques
   - Results
```

### System Overview
```
[Architecture diagram]

1. Design Goals (1 paragraph)
2. High-level Architecture (1-2 paragraphs)
3. Component Overview (2-3 paragraphs)
```

### Implementation
```
1. Core Components (3-4 paragraphs)
   - Design decisions
   - Optimizations

2. Scaling/Optimization (1-2 paragraphs)
   - Performance techniques
   - Resource management
```

### Evaluation
```
1. Testbed (1 paragraph)
   - Hardware/environment
   - Workloads

2. Performance Results (2-3 paragraphs + tables/graphs)
   - Throughput, latency
   - Scalability
   - Comparison with baselines

3. Case Studies (1-2 paragraphs)
```

## Short Paper / Workshop Paper

### Abstract (150 words)
```
One sentence background
One sentence problem
One sentence approach
One sentence results
```

### Introduction (1-2 pages)
```
1. Problem + Motivation (1 paragraph)
2. Approach Overview (1 paragraph)
3. Contributions (bullet list, 3 items max)
4. ...
```

### (Omit or shorten sections as needed)
- Related Work can be merged into Introduction
- Ablation can be minimal
- Focus on one key contribution

## Checklist Before Submission

- [ ] Abstract reads as standalone summary
- [ ] Introduction motivates problem clearly
- [ ] Contributions are concrete and verifiable
- [ ] Method section is complete and reproducible
- [ ] Experiments are fair (same data, same compute)
- [ ] Results include error bars/statistical tests
- [ ] Related Work is organized by topic
- [ ] Conclusion acknowledges limitations
- [ ] Supplementary materials planned
- [ ] Paper length matches venue requirements
