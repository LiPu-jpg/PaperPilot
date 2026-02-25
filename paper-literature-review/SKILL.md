---
name: paper-literature-review
description: Use when conducting literature review, searching for academic papers, identifying research gaps, or analyzing existing work
---

# Paper Literature Review

Search, analyze, and synthesize academic literature to identify research gaps and inform hypothesis generation.

## Supported Databases

- **arXiv**: Preprints in physics, mathematics, CS, AI (http://export.arxiv.org/api/query)
- **Semantic Scholar**: Academic paper search with citation analysis
- **PubMed**: Biomedical literature
- **CrossRef**: DOI metadata and citation lookup

## Key Functions

### 1. Literature Search
- Keyword optimization and query refinement
- Multi-database search with deduplication
- Citation network exploration

### 2. Paper Analysis
- Abstract and key contribution extraction
- Method summary
- Limitation identification

### 3. Gap Identification
- Compare findings across papers
- Identify unexplored combinations
- Highlight methodological improvements needed

## Output Format

After literature review, output:

```json
{
  "research_gap": "Clear articulation of the gap",
  "key_papers": [
    {"title": "...", "year": 2024, "method": "...", "limitation": "..."}
  ],
  "summary": "2-3 paragraph synthesis",
  "recommended_directions": ["direction 1", "direction 2"]
}
```

## Scripts

- `scripts/arxiv-search.py`: arXiv API integration
- `scripts/citation-extractor.py`: Extract citations from PDFs
- `scripts/review-generator.py`: Generate literature review draft

## Tips

- Start with broader searches, then refine
- Check recent papers (last 2-3 years) for current state
- Look for systematic reviews in your area
- Note: Quality over quantity - 10 relevant papers > 100 irrelevant ones
