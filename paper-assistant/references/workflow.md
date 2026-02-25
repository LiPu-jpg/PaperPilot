# Workflow

## Full Pipeline

```
[文献调研] → [假设生成] → [代码编写] → [实验执行] → [论文撰写]
     ↓            ↓            ↓           ↓            ↓
  research_   hypothesis  code artifacts results    manuscript
    gap         design      logs        tables      drafts
```

## Stage Transitions

### 1. Literature Review → Hypothesis

**Input**: Research gap summary, key papers
**Output**: Hypothesis statements, experiment designs

**Handshake**:
- Coordinator passes: gap analysis, paper summaries
- Hypothesis plugin receives: research problem statement

### 2. Hypothesis → Code

**Input**: Hypothesis statements, experiment designs
**Output**: Implemented code, test results

**Handshake**:
- Hypothesis passes: variable definitions, evaluation metrics
- Code plugin receives: expected inputs/outputs, baseline methods

### 3. Code → Experiment

**Input**: Working implementation, configs
**Output**: Experiment results, statistics

**Handshake**:
- Code passes: run commands, logging format
- Experiment plugin receives: raw results directory

### 4. Experiment → Writing

**Input**: Results tables, figures, analysis
**Output**: Complete manuscript

**Handshake**:
- Experiment passes: result summaries, key findings
- Writing plugin receives: figures, tables, statistics

## Partial Workflows

Users can start from any stage:

```
Start from experiment:
  - Need: Existing code, configs
  - Skip: Literature review, hypothesis, code

Start from writing:
  - Need: Experiment results
  - Skip: All earlier stages
```

## Context File

`.paper_context.json` stores:
- Current stage
- Stage outputs
- User preferences
- Project metadata

See `context-management.md` for details.
