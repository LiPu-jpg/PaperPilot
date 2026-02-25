#!/usr/bin/env python3
"""
Semantic Scholar API Search

Search academic papers using Semantic Scholar API with citation network analysis.

Usage:
    python semantic-scholar.py "transformer attention" --max-results 10

API Key (optional):
    Set SEMANTIC_SCHOLAR_API_KEY environment variable for higher rate limits.
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.parse
from typing import Dict, List, Optional


# Semantic Scholar API base URL
SEMANTIC_SCHOLAR_URL = "https://api.semanticscholar.org/graph/v1"


class SemanticScholarClient:
    """Client for Semantic Scholar API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        self.base_url = SEMANTIC_SCHOLAR_URL

    def _make_request(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
    ) -> Dict:
        """Make API request with proper headers."""

        headers = {
            "Accept": "application/json",
        }

        if self.api_key:
            headers["x-api-key"] = self.api_key

        url = f"{self.base_url}/{endpoint}"

        if params:
            url += f"?{urllib.parse.urlencode(params)}"

        request = urllib.request.Request(url, headers=headers)

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:
                raise RuntimeError("Rate limit exceeded. Consider using an API key.")
            raise RuntimeError(f"HTTP Error {e.code}: {e.reason}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"Connection Error: {e.reason}")

    def search_papers(
        self,
        query: str,
        max_results: int = 10,
        fields: Optional[str] = None,
    ) -> List[Dict]:
        """Search for papers."""

        if fields is None:
            fields = "title,authors,abstract,year,venue,citationCount,referenceCount,doi,fieldsOfStudy"

        params = {
            "query": query,
            "limit": min(max_results, 100),
            "fields": fields,
            "offset": 0,
        }

        result = self._make_request("paper/search", params)
        return result.get("data", [])

    def get_paper(self, paper_id: str, fields: Optional[str] = None) -> Optional[Dict]:
        """Get paper details by ID (DOI, arXiv ID, or Semantic Scholar ID)."""

        if fields is None:
            fields = "title,authors,abstract,year,venue,citationCount,references,citations,fieldsOfStudy"

        params = {"fields": fields}

        try:
            return self._make_request(f"paper/{paper_id}", params)
        except RuntimeError:
            return None

    def get_citations(self, paper_id: str, max_results: int = 10) -> List[Dict]:
        """Get papers citing the given paper."""

        params = {
            "limit": min(max_results, 1000),
            "fields": "title,authors,year,venue,citationCount",
        }

        result = self._make_request(f"paper/{paper_id}/citations", params)
        return result.get("data", [])

    def get_references(self, paper_id: str, max_results: int = 10) -> List[Dict]:
        """Get papers referenced by the given paper."""

        params = {
            "limit": min(max_results, 1000),
            "fields": "title,authors,year,venue,referenceCount",
        }

        result = self._make_request(f"paper/{paper_id}/references", params)
        return result.get("data", [])

    def get_citation_network(
        self,
        paper_id: str,
        depth: int = 1,
    ) -> Dict:
        """Get citation network for a paper."""

        paper = self.get_paper(paper_id)

        if not paper:
            return {"error": "Paper not found"}

        network = {
            "paper": {
                "paperId": paper.get("paperId"),
                "title": paper.get("title"),
                "year": paper.get("year"),
            },
            "citations": [],
            "references": [],
        }

        if depth >= 1:
            network["citations"] = self.get_citations(paper_id, max_results=20)
            network["references"] = self.get_references(paper_id, max_results=20)

        return network


def format_paper(paper: Dict, include_abstract: bool = False) -> str:
    """Format paper for console output."""

    lines = []
    lines.append(f"Title: {paper.get('title', 'N/A')}")

    authors = paper.get("authors", [])
    if authors:
        author_names = [a.get("name", "") for a in authors[:3]]
        lines.append(f"Authors: {', '.join(author_names)}")

    if paper.get("year"):
        lines.append(f"Year: {paper.get('year')}")

    if paper.get("venue"):
        lines.append(f"Venue: {paper.get('venue')}")

    lines.append(f"Citations: {paper.get('citationCount', 0)}")

    if paper.get("doi"):
        lines.append(f"DOI: {paper.get('doi')}")

    if include_abstract and paper.get("abstract"):
        abstract = paper["abstract"][:500]
        if len(paper["abstract"]) > 500:
            abstract += "..."
        lines.append(f"\nAbstract: {abstract}")

    return "\n    ".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Search Semantic Scholar API for academic papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python semantic-scholar.py "transformer attention"
    python semantic-scholar.py "BERT" -n 20 --output results.json
    python semantic-scholar.py --paper-id <id> --citations
    python semantic-scholar.py --paper-id <id> --references

Environment Variables:
    SEMANTIC_SCHOLAR_API_KEY  - Optional API key for higher rate limits
        """,
    )

    parser.add_argument(
        "query",
        nargs="?",
        help="Search query",
    )
    parser.add_argument(
        "--max-results",
        "-n",
        type=int,
        default=10,
        help="Maximum number of results (default: 10)",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output JSON file (default: print to console)",
    )
    parser.add_argument(
        "--api-key",
        help="Semantic Scholar API key (or set SEMANTIC_SCHOLAR_API_KEY)",
    )
    parser.add_argument(
        "--paper-id",
        help="Get paper by ID (DOI, arXiv ID, or Semantic Scholar ID)",
    )
    parser.add_argument(
        "--citations",
        action="store_true",
        help="Show papers citing the paper (requires --paper-id)",
    )
    parser.add_argument(
        "--references",
        action="store_true",
        help="Show papers referenced by the paper (requires --paper-id)",
    )
    parser.add_argument(
        "--abstract",
        action="store_true",
        help="Include abstract in output",
    )

    args = parser.parse_args()

    # Check if we have valid arguments
    if not args.query and not args.paper_id:
        parser.error("Either provide a search query or use --paper-id")

    if args.citations or args.references:
        if not args.paper_id:
            parser.error("--citations and --references require --paper-id")

    # Create client
    client = SemanticScholarClient(api_key=args.api_key)

    try:
        if args.paper_id:
            # Get specific paper or citation network
            if args.citations or args.references:
                network = client.get_citation_network(args.paper_id)

                if "error" in network:
                    print(f"Error: {network['error']}")
                    sys.exit(1)

                output = network
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(output, f, indent=2)
                    print(f"Citation network saved to: {args.output}")
                else:
                    print(f"\nPaper: {network['paper']['title']}")
                    if args.citations:
                        print(f"\nCiting Papers ({len(network['citations'])}):")
                        for i, c in enumerate(network["citations"], 1):
                            print(f"  [{i}] {c.get('title', 'N/A')}")
                    if args.references:
                        print(f"\nReferences ({len(network['references'])}):")
                        for i, r in enumerate(network["references"], 1):
                            print(f"  [{i}] {r.get('title', 'N/A')}")
            else:
                # Just get paper details
                paper = client.get_paper(args.paper_id)

                if not paper:
                    print("Paper not found")
                    sys.exit(1)

                output = paper
                if args.output:
                    with open(args.output, "w", encoding="utf-8") as f:
                        json.dump(output, f, indent=2)
                    print(f"Paper details saved to: {args.output}")
                else:
                    print(format_paper(paper, include_abstract=args.abstract))
        else:
            # Search papers
            papers = client.search_papers(args.query, max_results=args.max_results)

            if not papers:
                print("No results found.")
                return

            output = papers

            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2)
                print(f"Results saved to: {args.output}")
            else:
                for i, paper in enumerate(papers, 1):
                    print(
                        f"\n[{i}] {format_paper(paper, include_abstract=args.abstract)}"
                    )

    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
