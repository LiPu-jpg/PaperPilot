# Context Management

## File Location

Context is stored in `.paper_context.json` at project root.

## Schema

```json
{
  "project": {
    "name": "string",
    "created_at": "ISO8601",
    "last_updated": "ISO8601"
  },
  "current_stage": "literature_review|hypothesis|code|experiment|writing",
  "stages": {
    "literature_review": {
      "status": "pending|in_progress|completed",
      "query": "search query used",
      "papers_found": 50,
      "papers_analyzed": 15,
      "research_gap": "string",
      "key_papers": [...],
      "summary": "string"
    },
    "hypothesis": {
      "status": "pending|in_progress|completed",
      "hypotheses": [...],
      "experiment_designs": [...]
    },
    "code": {
      "status": "pending|in_progress|completed",
      "repo_url": "string",
      "config": "string"
    },
    "experiment": {
      "status": "pending|in_progress|completed",
      "results": {...},
      "tables": [...],
      "figures": [...]
    },
    "writing": {
      "status": "pending|in_progress|completed",
      "sections": {...}
    }
  },
  "user_preferences": {
    "discipline": "cs|bio|psych|...",
    "methodology": "quantitative|qualitative|mixed",
    "language": "zh|en",
    "citation_style": "IEEE|APA|MLA|..."
  }
}
```

## Operations

### Save Context
After each stage completion, save output to context file.

### Load Context
On session start, load existing context to restore state.

### Rollback
If stage fails or user requests changes, rollback to previous stage output.

### Resume
Continue from current stage without redoing completed stages.

## Integration

The coordinator manages context automatically:
- `paper-assistant` reads/writes context
- Plugins receive relevant stage data
- Plugins return outputs for next stage
