# Integration Guide

## Plugin Architecture

The paper-assistant coordinates five specialized plugins:

```
paper-assistant (coordinator)
    ├── paper-literature-review
    ├── paper-hypothesis
    ├── paper-code
    ├── paper-experiment
    └── paper-writing
```

## Data Flow Between Stages

### Literature Review → Hypothesis

**Passed Data:**
- `research_gap`: Identified gap from literature
- `key_papers`: List of analyzed papers with methods and limitations
- `summary`: Synthesis of existing work

**Used by Hypothesis Plugin:**
- Gap analysis to formulate hypothesis
- Existing methods to identify improvement opportunities
- Paper summaries for positioning

### Hypothesis → Code

**Passed Data:**
- `hypotheses`: Array of hypothesis statements
- `variables`: Independent/dependent variables
- `experiment_designs`: Planned experimental setups
- `feasibility`: Assessment of data and method availability

**Used by Code Plugin:**
- Variable definitions for function signatures
- Expected metrics for evaluation functions
- Baseline methods for comparison implementation

### Code → Experiment

**Passed Data:**
- `repo_url`: Path to code repository
- `config`: Experiment configuration files
- `run_commands`: How to execute experiments
- `logging_format`: Expected output structure

**Used by Experiment Plugin:**
- Execution commands to run code
- Config parsing for hyperparameter grids
- Log format parsing to extract results

### Experiment → Writing

**Passed Data:**
- `results`: Raw experiment outputs
- `tables`: Formatted result tables with statistics
- `figures`: Generated visualizations
- `analysis`: Statistical significance tests

**Used by Writing Plugin:**
- Result tables for Results section
- Figures for Figures section
- Statistics to support claims

## Stage Transition Protocol

### 1. Pre-Transition Validation

Before moving to next stage:
1. Run stage-specific validator (see `state-checker.py`)
2. Check required outputs exist in context
3. Validate data format matches schema

Example:
```python
from scripts.state_checker import StageValidator

validator = StageValidator()
result = validator.validate_literature_review(context)

if not result.valid:
    print(f"Missing: {result.missing}")
    print(f"Errors: {result.errors}")
    # Do not transition
```

### 2. Context Update

When validation passes:
```python
from scripts.context_manager import ContextManager

manager = ContextManager("/path/to/project")
manager.update_stage("hypothesis", {
    "hypotheses": [...],
    "experiment_designs": [...]
})
manager.save_context()
```

### 3. Handshake with Next Plugin

Pass relevant data to next plugin:
```python
# Coordinator extracts from context
hypothesis_data = context["stages"]["hypothesis"]

# Next plugin receives
plugin_input = {
    "hypothesis": hypothesis_data["hypotheses"],
    "variables": hypothesis_data["variables"],
    "from_stage": "literature_review"
}
```

## Starting from Arbitrary Stages

### Skip Previous Stages

Users can start from any stage with existing data:

```bash
# Start directly from experiment stage
# Must provide:
- Working code repository
- Experiment configs
- Baseline results (optional)
```

### Context Initialization

When starting mid-workflow:
1. Load existing `.paper_context.json`
2. Mark skipped stages as `completed` (optional)
3. Set target stage as `in_progress`
4. Validate that required inputs are available

```python
manager = ContextManager("/path/to/project")
context = manager.load_context()

# User wants to start from experiment
context["current_stage"] = "experiment"
context["stages"]["literature_review"]["status"] = "completed"
context["stages"]["hypothesis"]["status"] = "completed"
context["stages"]["code"]["status"] = "completed"

manager.save_context()
```

## Error Handling and Recovery

### Stage Failure

If a stage fails to complete:
1. **Log failure**: Record error in context
2. **Keep state**: Do not mark as completed
3. **Options**:
   - Retry same stage
   - Rollback to previous stage
   - Modify inputs and retry

```python
# Stage failed
context["stages"]["experiment"]["status"] = "failed"
context["stages"]["experiment"]["error"] = "Runtime error: ..."

# User chooses rollback
manager.rollback_to_stage("code")

# Or user chooses retry
# Keep current stage, fix issue, try again
```

### Rollback Mechanism

Rollback to a previous stage:
1. Reset current stage to `pending`
2. Restore previous stage to `in_progress`
3. Preserve all completed stage outputs
4. Optionally revert dependent stages to `pending`

```python
def rollback_to_stage(target_stage):
    context = load_context()

    # Reset stages after target
    stages_order = ["literature_review", "hypothesis", "code", "experiment", "writing"]
    target_idx = stages_order.index(target_stage)

    for stage in stages_order[target_idx+1:]:
        context["stages"][stage]["status"] = "pending"
        # Optionally clear outputs
        # context["stages"][stage].clear_outputs()

    # Set target as current
    context["current_stage"] = target_stage
    context["stages"][target_stage]["status"] = "in_progress"

    save_context(context)
```

## Validation Criteria

Each stage must meet these criteria before transitioning:

| Stage | Required Outputs | Validation Checks |
|--------|-----------------|------------------|
| Literature Review | `research_gap`, `key_papers`, `summary` | Gap clearly articulated, papers analyzed (min 5), summary synthesizes findings |
| Hypothesis | `hypotheses`, `experiment_designs`, `feasibility` | At least 1 hypothesis, falsifiable statements, data availability confirmed |
| Code | `repo_url`, `config`, tests passing | Code runs without errors, unit tests pass, config documented |
| Experiment | `results`, `tables`, `figures`, `analysis` | Results statistically significant, visualizations generated, documentation complete |
| Writing | `sections`, citations formatted | All sections drafted, citations match style, abstract written |

## Plugin Independence

Each plugin can be used standalone:

```bash
# Use only literature review
paper-literature-review skill

# Use only code generation
paper-code skill

# Use only writing polish
paper-writing skill
```

When used standalone:
1. Plugin creates its own context file
2. No coordinator needed
3. User manages outputs manually

## Testing Integration

### Test Full Workflow

```bash
# Initialize project
python paper-assistant/scripts/context-manager.py init

# Run complete workflow
python paper-assistant/scripts/context-manager.py run_workflow

# Verify each stage
python paper-assistant/scripts/state-checker.py validate_all
```

### Test Individual Transitions

```bash
# Test literature → hypothesis
python paper-assistant/scripts/integration_test.py --transition literature_review hypothesis

# Test hypothesis → code
python paper-assistant/scripts/integration_test.py --transition hypothesis code
```
