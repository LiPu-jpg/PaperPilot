#!/usr/bin/env python3
"""
Literature Review Generator

Generates literature review drafts from analyzed paper data,
identifies research gaps, and produces structured output for hypothesis generation.
"""

import argparse
import json
import sys
from typing import List, Dict, Any, Optional
from datetime import datetime


def synthesize_summary(papers: List[Dict[str, Any]]) -> str:
    """Synthesize a 2-3 paragraph summary from analyzed papers.

    Args:
        papers: List of paper dictionaries with title, summary, method, etc.

    Returns:
        Synthesized summary text
    """
    if not papers:
        return "No papers analyzed yet."

    themes = {}
    for paper in papers:
        method = paper.get("method", "").lower()
        if not method:
            method = paper.get("summary", "").split(" ")[0].lower()
        if method not in themes:
            themes[method] = []
        themes[method].append(paper)

    summary_parts = []

    if len(themes) > 0:
        method_names = ", ".join(themes.keys())
        summary_parts.append(
            f"This review analyzed {len(papers)} papers using methods "
            f"including {method_names}."
        )

    if len(papers) > 0:
        summary_parts.append(
            f"The most cited works focus on {papers[0].get('title', 'key work')}. "
            f"Recent advances include {papers[-1].get('title', 'latest approach')}."
        )

    if len(themes) > 1:
        summary_parts.append(
            f"There is a growing trend toward {list(themes.keys())[-1]} approaches, "
        )

    return " ".join(summary_parts)


def identify_research_gap(papers: List[Dict[str, Any]]) -> str:
    """Identify research gap by analyzing limitations and future work.

    Args:
        papers: List of analyzed paper dictionaries

    Returns:
        Articulated research gap
    """
    if not papers:
        return "Insufficient papers to identify research gap (need at least 3)."

    limitations = []
    for paper in papers:
        if "limitation" in paper:
            limitations.append(paper["limitation"])

    future_work = []
    for paper in papers:
        if "future_work" in paper:
            future_work.append(paper["future_work"])

    gap_parts = []

    if limitations:
        gap_parts.append(
            f"While current approaches {', '.join(limitations[:2])}, "
            f"these methods still face challenges in {', '.join(limitations[2:])}."
        )

    if future_work:
        gap_parts.append(
            f"Recent work identifies opportunities in {', '.join(future_work[:2])}, "
            f"but systematic exploration of {', '.join(future_work[2:])} remains limited."
        )

    gap_parts.append(
        "This research aims to address these limitations by "
        "developing novel approaches that combine the strengths of "
        "existing methods while mitigating their weaknesses."
    )

    return " ".join(gap_parts)


def generate_key_papers(papers: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
    """Select and format key papers from the full list.

    Args:
        papers: List of all analyzed papers
        top_n: Number of key papers to select (default 10)

    Returns:
        List of key papers with essential information
    """
    if not papers:
        return []

    sorted_papers = sorted(
        papers,
        key=lambda x: (x.get("year", 2025), -len(x.get("citations", []))),
        reverse=True
    )

    key_papers = sorted_papers[:top_n]

    formatted = []
    for i, paper in enumerate(key_papers, 1):
        formatted.append({
            "id": f"P{i}",
            "title": paper.get("title", "Unknown"),
            "year": paper.get("year", "Unknown"),
            "method": paper.get("method", "Unknown"),
            "limitation": paper.get("limitation", "Not specified"),
            "contribution": paper.get("summary", "").split(".")[0] + "." if paper.get("summary") else ""
        })

    return formatted


def generate_output(papers: List[Dict[str, Any]], query: str) -> Dict[str, Any]:
    """Generate complete literature review output.

    Args:
        papers: List of analyzed papers
        query: Original search query

    Returns:
        Dictionary with review results
    """
    research_gap = identify_research_gap(papers)
    summary = synthesize_summary(papers)
    key_papers_list = generate_key_papers(papers, top_n=10)

    methods = set()
    for paper in papers:
        if "method" in paper:
            methods.add(paper["method"].lower())

    recommended_directions = []
    if "attention" in " ".join(methods):
        recommended_directions.append(
            "Investigate attention mechanisms for long-range dependency modeling"
        )
    if "transformer" in " ".join(methods):
        recommended_directions.append(
            "Explore efficient transformer architectures for resource-constrained environments"
        )
    if len(methods) > 0:
        recommended_directions.append(
            f"Combine strengths of {', '.join(list(methods)[:3])} methods"
        )

    return {
        "query": query,
        "papers_analyzed": len(papers),
        "research_gap": research_gap,
        "summary": summary,
        "key_papers": key_papers_list,
        "recommended_directions": recommended_directions[:5]
    }


def load_papers_from_file(input_file: str) -> List[Dict[str, Any]]:
    """Load papers from JSON file.

    Args:
        input_file: Path to JSON file with paper data

    Returns:
        List of paper dictionaries

    Raises:
        FileNotFoundError: If input file doesn't exist
        json.JSONDecodeError: If file is invalid JSON
    """
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("papers", [])
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in input file: {e}")


def main():
    """CLI interface for review generator."""
    parser = argparse.ArgumentParser(
        description="Generate literature review from analyzed paper data"
    )
    parser.add_argument(
        "input",
        help="Input JSON file with paper data (output from arxiv-search.py)"
    )
    parser.add_argument(
        "--query",
        help="Original search query (for metadata)"
    )
    parser.add_argument(
        "--output",
        help="Output JSON file path (default: literature_review.json)",
        default="literature_review.json"
    )
    parser.add_argument(
        "--key-papers",
        type=int,
        help="Number of key papers to include (default: 10)",
        default=10
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print JSON output"
    )

    args = parser.parse_args()

    try:
        papers = load_papers_from_file(args.input)

        if not papers:
            print("Warning: No papers found in input file", file=sys.stderr)
            print("Input file should contain: {\"papers\": [...]}", file=sys.stderr)
            sys.exit(1)

        output = generate_output(papers, args.query or "literature review")

        with open(args.output, "w", encoding="utf-8") as f:
            if args.pretty:
                json.dump(output, f, indent=2, ensure_ascii=False)
            else:
                json.dump(output, f, ensure_ascii=False)

        print(f"✓ Literature review generated: {args.output}")
        print(f"  Papers analyzed: {output['papers_analyzed']}")
        print(f"  Key papers: {len(output['key_papers'])}")
        print(f"  Research gap identified: {len(output['research_gap'])} chars")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
