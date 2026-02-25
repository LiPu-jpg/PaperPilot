---
name: paper-writing
description: Use when drafting manuscript sections, formatting citations, polishing writing style, or preparing paper for submission
---

# Paper Writing

Draft, format, and polish academic papers following journal/conference standards.

## Paper Structure (IMRaD)

| Section | Content |
|---------|---------|
| Abstract | Problem, method, results, conclusion (150-300 words) |
| Introduction | Background, problem statement, contributions |
| Related Work | Literature review, positioning |
| Method | Technical approach, model, algorithm |
| Experiments | Setup, baselines, results, analysis |
| Conclusion | Summary, limitations, future work |

## Citation Styles

Supported formats:
- **IEEE**: Numbered citations [1], [2]
- **APA**: Author (Year) format
- **MLA**: Author Page format
- **Chicago**: Footnote or author-date

Use reference managers (Zotero, Mendeley) for BibTeX export.

## Writing Tips

### Clarity
- One idea per paragraph
- Active voice when possible
- Define acronyms on first use
- Use figures to illustrate complex concepts

### Conciseness
- Remove redundant words
- Cut unnecessary adjectives
- Prefer direct statements over hedged ones

### Technical
- Define terms precisely
- Explain "why" not just "what"
- Connect related work to your approach

## Humanizer

Use `humanizer-zh` skill to remove AI writing patterns:
- Avoid exaggerated significance
- Reduce mechanical transition phrases
- Vary sentence structure
- Remove formulaic expressions

## Scripts

- `bibliography-formatter.py`: Format BibTeX entries
- `section-templates.md`: Section outlines by paper type

## Tips

- Write methods first (most concrete)
- Save abstract for last
- Read papers in your target venue for style
- Get feedback early from co-authors
