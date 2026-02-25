---
name: paper-assistant
description: Use when coordinating the complete academic paper writing workflow, managing stage transitions, or initializing a new paper project
---

# Paper Assistant

The central orchestrator for AI-assisted academic paper writing, managing the complete workflow from literature review to publication.

## Workflow Stages

1. **Literature Review** → Research gap identification
2. **Hypothesis Generation** → Hypothesis formulation and experiment design
3. **Code Implementation** → Experimental code development
4. **Experiment Execution** → Running experiments and analyzing results
5. **Paper Writing** → Drafting and polishing the manuscript

## Context Management

The assistant maintains context through `.paper_context.json`:

```json
{
  "project_name": "my-paper",
  "current_stage": "literature_review",
  "stages": {
    "literature_review": {
      "status": "completed",
      "research_gap": "...",
      "summary": "..."
    },
    "hypothesis": { "status": "pending" },
    "code": { "status": "pending" },
    "experiment": { "status": "pending" },
    "writing": { "status": "pending" }
  },
  "user_preferences": {
    "discipline": "cs",
    "methodology": "quantitative",
    "language": "zh",
    "citation_style": "IEEE"
  }
}
```

## Usage

### Start New Project
```
I want to write a paper about [topic]
```

### Continue from Stage
```
Continue to hypothesis generation
Skip to experiment stage
```

### Query Status
```
What's the current status of my paper?
Show me the literature review summary
```

## Stage Validation

Each stage must meet completion criteria before proceeding:

- **Literature Review**: Research gap identified, key papers summarized
- **Hypothesis**: Feasibility assessed, experiment design approved
- **Code**: Implementation complete, tests passing
- **Experiment**: Results collected, statistical significance verified
- **Writing**: All sections drafted, citations formatted

## Integration

This coordinator delegates to specialized skills:
- `paper-literature-review`: Literature search and analysis
- `paper-hypothesis`: Hypothesis generation and validation
- `paper-code`: Code scaffolding and best practices
- `paper-experiment`: Experiment execution and analysis
- `paper-writing`: Manuscript drafting and polishing

Each plugin can be used independently or as part of the full workflow.
## Scripts

The coordinator provides three core scripts for context management:

- `scripts/context-manager.py`: Load, save, and update .paper_context.json
- `scripts/state-checker.py`: Validate stage completion and transitions
- `scripts/discipline-config.py`: Manage discipline-specific configurations

### Usage Examples

```bash
# Initialize new project
python scripts/context-manager.py init --project ./my-paper

# Check project status
python scripts/context-manager.py status

# Validate current stage
python scripts/state-checker.py literature_review

# List supported disciplines
python scripts/discipline-config.py list

# Get discipline info
python scripts/discipline-config.py info --discipline cs
```
