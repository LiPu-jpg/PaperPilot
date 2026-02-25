#!/usr/bin/env python3
"""
PubMed API Search

Search biomedical literature using NCBI E-utilities API.

Usage:
    python pubmed-search.py "machine learning" --max-results 10
"""

import argparse
import json
import urllib.request
import urllib.parse
import urllib.error
from typing import Dict, List, Optional
from datetime import datetime


# NCBI E-utilities base URL
EUTILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(
    query: str,
    max_results: int = 10,
    db: str = "pubmed",
    retmode: str = "json",
) -> Dict:
    """Search PubMed using E-utilities ESearch."""

    params = {
        "db": db,
        "term": query,
        "retmode": retmode,
        "retmax": max_results,
        "sort": "relevance",
    }

    url = f"{EUTILS_URL}/esearch.fcgi?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("esearchresult", {})
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection Error: {e.reason}")
    except json.JSONDecodeError:
        raise RuntimeError("Failed to parse PubMed response")


def fetch_details(id_list: List[str], db: str = "pubmed") -> List[Dict]:
    """Fetch detailed information for PubMed IDs using ESummary."""

    if not id_list:
        return []

    params = {
        "db": db,
        "id": ",".join(id_list),
        "retmode": "json",
    }

    url = f"{EUTILS_URL}/esummary.fcgi?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))

        result_list = data.get("result", {})
        papers = []

        for pmid in id_list:
            if pmid in result_list:
                item = result_list[pmid]
                paper = {
                    "pmid": pmid,
                    "title": item.get("title", ""),
                    "authors": item.get("authors", []),
                    "source": item.get("source", ""),
                    "pubdate": item.get("pubdate", ""),
                    "doi": item.get("elocationid", "").replace("doi: ", ""),
                    "abstract": item.get(
                        "title", ""
                    ),  # Summary doesn't include abstract
                }
                papers.append(paper)

        return papers
    except Exception as e:
        raise RuntimeError(f"Failed to fetch details: {e}")


def search_pubmed_full(
    query: str,
    max_results: int = 10,
    include_details: bool = True,
) -> List[Dict]:
    """Complete PubMed search with details."""

    # Step 1: Search for IDs
    search_result = search_pubmed(query, max_results)
    id_list = search_result.get("IdList", [])

    if not id_list:
        return []

    # Step 2: Fetch details if requested
    if include_details:
        papers = fetch_details(id_list)
        return papers

    # Return minimal results with just IDs
    return [{"pmid": pmid} for pmid in id_list]


def output_results(papers: List[Dict], output_file: Optional[str] = None) -> None:
    """Output results to file or console."""

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=2, ensure_ascii=False)
        print(f"Results saved to: {output_file}")
    else:
        for i, paper in enumerate(papers, 1):
            print(f"\n[{i}] PMID: {paper.get('pmid', 'N/A')}")
            print(f"    Title: {paper.get('title', 'N/A')}")
            print(f"    Authors: {', '.join(paper.get('authors', [])[:3])}")
            print(f"    Source: {paper.get('source', 'N/A')}")
            print(f"    Date: {paper.get('pubdate', 'N/A')}")
            if paper.get("doi"):
                print(f"    DOI: {paper.get('doi')}")


def main():
    parser = argparse.ArgumentParser(
        description="Search PubMed using NCBI E-utilities API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python pubmed-search.py "CRISPR gene editing"
    python pubmed-search.py "deep learning" --max-results 20 --output results.json
        """,
    )

    parser.add_argument(
        "query",
        help="Search query (supports PubMed syntax)",
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
        "--ids-only",
        action="store_true",
        help="Only return PubMed IDs without details",
    )
    parser.add_argument(
        "--db",
        default="pubmed",
        choices=["pubmed", "medline"],
        help="Database to search (default: pubmed)",
    )

    args = parser.parse_args()

    try:
        papers = search_pubmed_full(
            args.query,
            max_results=args.max_results,
            include_details=not args.ids_only,
        )

        if not papers:
            print("No results found.")
            return

        output_results(papers, args.output)

    except RuntimeError as e:
        print(f"Error: {e}", file=__import__("sys").stderr)
        __import__("sys").exit(1)


if __name__ == "__main__":
    main()
