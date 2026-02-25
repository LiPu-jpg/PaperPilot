"""
arXiv API Search

Usage:
    python arxiv-search.py "transformer attention" --max-results 10
"""

import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from typing import List, Dict


def search_arxiv(query: str, max_results: int = 10) -> List[Dict]:
    """Search arXiv API and return results."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }

    url = f"{base_url}?{urllib.parse.urlencode(params)}"

    with urllib.request.urlopen(url) as response:
        data = response.read()

    root = ET.fromstring(data)
    results = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        result = {
            "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip(),
            "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
            "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
            "authors": [
                a.find("{http://www.w3.org/2005/Atom}name").text
                for a in entry.findall("{http://www.w3.org/2005/Atom}author")
            ],
            "pdf_url": entry.find(
                "{http://www.w3.org/2005/Atom}link[@title='pdf']"
            ).attrib["href"],
        }
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Search arXiv")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--max-results", type=int, default=10)
    args = parser.parse_args()

    results = search_arxiv(args.query, args.max_results)

    for i, r in enumerate(results, 1):
        print(f"\n[{i}] {r['title']}")
        print(f"    Published: {r['published'][:10]}")
        print(f"    Authors: {', '.join(r['authors'][:3])}")
        print(f"    PDF: {r['pdf_url']}")


if __name__ == "__main__":
    main()
