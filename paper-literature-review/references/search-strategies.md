# Search Strategies for Literature Review

## Multi-Database Strategy

### Primary Databases
- **arXiv**: Physics, mathematics, CS, AI preprints
- **Semantic Scholar**: Comprehensive academic search with citation analysis
- **PubMed**: Biomedical and life sciences literature
- **CrossRef**: DOI metadata and citation lookup

### Search Flow
1. Start with broad keywords
2. Refine based on initial results
3. Use Boolean operators to combine concepts
4. Apply date filters (last 2-5 years for recent work)
5. Deduplicate results across databases

## Keyword Optimization

### Boolean Operators
- `AND`: `transformer AND attention` - both terms must appear
- `OR`: `(attention OR mechanism)` - at least one must appear
- `NOT`: `transformer NOT recurrent` - exclude term
- Quotation marks: `"self-attention mechanism"` - exact phrase

### Query Refinement Techniques

**Expand with synonyms:**
- Core term: `attention mechanism`
- Synonyms: `self-attention`, `dot-product attention`, `cross-attention`

**Add domain-specific terms:**
- For ML: `machine learning`, `neural networks`, `deep learning`
- For NLP: `natural language processing`, `transformers`, `language models`

**Limit by time period:**
- Recent: `publishedDate:[2024-01-01 TO *]`
- Last 5 years: `publishedDate:[2019-01-01 TO *]`

## Citation Network Exploration

### Start with Seed Papers
- Identify 3-5 highly cited papers in your area
- Use their citation lists to find related work

### Forward Citation Tracing
- Find papers that cite your seed papers
- Build citation graph to understand influence
- Look for citation bursts (clusters of related work)

### Backward Citation Tracing
- Examine references in promising papers
- Find common foundations and classical approaches
- Understand historical development of the field

## Quality Assessment

### Relevance Filters
- Title relevance: Keywords in title?
- Abstract relevance: Keywords in abstract?
- Publication venue: Top conferences/journals?
- Citation count: Minimum threshold (e.g., >10 for recent work)

### Paper Screening Criteria
- Exclude: Preprints without peer review (unless appropriate)
- Exclude: Non-English papers (if working in English)
- Exclude: Duplicate papers across databases
- Minimum: Full-text availability or at least detailed abstract

## Systematic Review Approach

### PRISMA Framework
1. **P**lanning - Define search strategy and inclusion criteria
2. **R**ecruitment - Execute searches across databases
3. **S**election - Apply screening criteria
4. **A**ppraisal - Evaluate quality of selected papers
5. **S**ynthesis - Extract findings and identify gaps

### Evidence Mapping
- Create matrix of methods vs. applications
- Document strengths and limitations of each approach
- Map methodological trends over time

## Best Practices

### API Rate Limits
- arXiv: No strict limit, but be respectful
- Semantic Scholar: 5000 requests/day for free tier
- PubMed: 3 requests/second (NCBI E-utilities)

### Caching Strategy
- Store search results locally to avoid repeated API calls
- Implement incremental updates (cache first, then fetch new)
- Use cache expiration (e.g., 7 days for arXiv)

### Error Handling
- Handle API timeouts gracefully
- Implement retry logic with exponential backoff
- Log failed searches for debugging
- Provide partial results on complete failure
