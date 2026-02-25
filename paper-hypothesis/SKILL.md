---
name: paper-hypothesis
description: Use when generating research hypotheses, designing experiments, or evaluating hypothesis feasibility
---

# Paper Hypothesis

Generate and validate research hypotheses based on identified research gaps.

## Hypothesis Generation Framework

### 1. Gap Analysis
Based on literature review output, identify:
- What problem remains unsolved
- Why current approaches fail
- What new angle can be explored

### 2. Hypothesis Structure

```
H1: [Independent variable] affects [dependent variable] because [mechanism]

Example:
H1: Using larger context windows improves reasoning performance 
    in LLM benchmarks because longer contexts provide more 
    contextual information for inference.
```

### 3. Feasibility Assessment
- **Data availability**: Can you obtain necessary data?
- **Method feasibility**: Can you implement the approach?
- **Resource requirements**: Time, compute, tools needed
- **Validation path**: How will you prove/disprove the hypothesis?

## Experiment Design

| Component | Description |
|-----------|-------------|
| Control | Baseline method to compare against |
| Treatment | Your proposed approach |
| Metrics | How to measure success |
| Statistics | Test selection, significance level |

## Output Format

```json
{
  "hypotheses": [
    {
      "id": "H1",
      "statement": "...",
      "variables": {"independent": "...", "dependent": "..."},
      "feasibility": {"data": "available", "method": "feasible"},
      "experiment_design": {...}
    }
  ],
  "recommended_experiments": ["exp1", "exp2"],
  "potential_challenges": ["challenge1", "challenge2"]
}
```

## Tips

- Start with one clear hypothesis, add secondary ones later
- Make hypotheses falsifiable (provable wrong)
- Consider both positive and negative results as publishable
- Use brainstorming skill for idea exploration
|- Use brainstorming skill for idea exploration

## Scripts

`scripts/hypothesis-generator.py`: Generate hypotheses, assess feasibility, design experiments
