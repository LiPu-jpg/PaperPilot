#!/usr/bin/env python3
"""Bibliography Formatter - Format and validate BibTeX entries."""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


class BibTeXFormatter:
    """Format and normalize BibTeX entries."""

    # Field ordering for clean output
    FIELD_ORDER = [
        "author",
        "title",
        "booktitle",
        "journal",
        "year",
        "volume",
        "number",
        "pages",
        "publisher",
        "doi",
        "url",
        "abstract",
        "keywords",
        "editor",
        "edition",
        "series",
        "address",
        "month",
        "note",
        "crossref",
    ]

    def __init__(self, style: str = "IEEE"):
        self.style = style
        self.entries: Dict[str, Dict] = {}

    def parse_file(self, filepath: str) -> None:
        """Parse BibTeX file."""
        content = Path(filepath).read_text()
        self.entries = self._parse_bibtex(content)

    def _parse_bibtex(self, content: str) -> Dict[str, Dict]:
        """Parse BibTeX content into dictionary."""
        entries = {}
        # Match @type{citation_key, ...}
        entry_pattern = r"@(\w+)\s*\{\s*([^,]+),"

        for match in re.finditer(entry_pattern, content):
            entry_type = match.group(1)
            citation_key = match.group(2).strip()

            # Find the matching closing brace
            start = match.end()
            depth = 1
            end = start
            for i, char in enumerate(content[start:], start):
                if char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1
                if depth == 0:
                    end = i
                    break

            entry_content = content[start:end]
            fields = self._parse_fields(entry_content)
            entries[citation_key] = {"type": entry_type, **fields}

        return entries

    def _parse_fields(self, content: str) -> Dict[str, str]:
        """Parse fields from entry content."""
        fields = {}
        # Match field = value
        field_pattern = r"(\w+)\s*=\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}"

        for match in re.finditer(field_pattern, content):
            field_name = match.group(1).lower()
            field_value = match.group(2).strip()
            fields[field_name] = field_value

        return fields

    def format_entry(self, citation_key: str) -> str:
        """Format a single entry."""
        if citation_key not in self.entries:
            return f"Error: Citation key '{citation_key}' not found"

        entry = self.entries[citation_key]
        entry_type = entry.pop("type")

        lines = [f"@{entry_type}{{{citation_key},"]

        # Order fields
        for field in self.FIELD_ORDER:
            if field in entry:
                lines.append(f"  {field} = {{{entry[field]}}},")

        # Add any remaining fields
        for field, value in entry.items():
            if field not in self.FIELD_ORDER:
                lines.append(f"  {field} = {{{value}}},")

        lines.append("}")
        return "\n".join(lines)

    def format_all(self) -> str:
        """Format all entries."""
        return "\n\n".join(
            self.format_entry(key) for key in sorted(self.entries.keys())
        )

    def sort_by_author(self) -> Dict[str, Dict]:
        """Sort entries by first author name."""

        def get_first_author(entry):
            authors = entry.get("author", "").split(" and ")
            if authors:
                # Get last name of first author
                first = authors[0].strip().split()[-1]
                return first.lower()
            return "zzz"

        return dict(sorted(self.entries.items(), key=lambda x: get_first_author(x[1])))

    def validate(self, citation_key: Optional[str] = None) -> List[str]:
        """Validate entries for common issues."""
        errors = []

        def check_entry(key: str, entry: Dict):
            # Check required fields
            entry_type = entry.get("type", "").lower()
            if entry_type in ["article"]:
                required = ["author", "title", "journal", "year"]
            elif entry_type in ["inproceedings", "conference"]:
                required = ["author", "title", "booktitle", "year"]
            elif entry_type in ["book"]:
                required = ["author", "title", "publisher", "year"]
            else:
                required = ["author", "title", "year"]

            for field in required:
                if field not in entry:
                    errors.append(f"{key}: Missing required field '{field}'")

            # Check year format
            if "year" in entry:
                if not re.match(r"^\d{4}$", entry["year"]):
                    errors.append(f"{key}: Invalid year format '{entry['year']}'")

        if citation_key:
            if citation_key in self.entries:
                check_entry(citation_key, self.entries[citation_key])
            else:
                errors.append(f"Citation key '{citation_key}' not found")
        else:
            for key, entry in self.entries.items():
                check_entry(key, entry)

        return errors

    def convert_style(self, target_style: str) -> str:
        """Convert citations to different style."""
        # This is a simplified version
        lines = []

        for key, entry in self.entries.items():
            if target_style == "APA":
                authors = entry.get("author", "").split(" and ")
                if len(authors) == 1:
                    author_str = self._format_author_apa(authors[0])
                elif len(authors) == 2:
                    author_str = f"{self._format_author_apa(authors[0])} & {self._format_author_apa(authors[1])}"
                else:
                    author_str = f"{self._format_author_apa(authors[0])} et al."

                title = entry.get("title", "")
                journal = entry.get("journal", entry.get("booktitle", ""))
                year = entry.get("year", "")
                volume = entry.get("volume", "")
                pages = entry.get("pages", "")

                citation = f"{author_str} ({year}). {title}. "
                if journal:
                    citation += f"*{journal}*"
                    if volume:
                        citation += f", {volume}"
                    if pages:
                        citation += f", {pages}"
                citation += "."
                lines.append(f"[{key}] {citation}")

        return "\n".join(lines)

    def _format_author_apa(self, author: str) -> str:
        """Format author name for APA style."""
        parts = author.strip().split()
        if len(parts) >= 2:
            last = parts[-1]
            initials = " ".join(p[0] + "." for p in parts[:-1])
            return f"{last}, {initials}"
        return author


def main():
    parser = argparse.ArgumentParser(description="Format and validate BibTeX entries")
    parser.add_argument("input", help="Input BibTeX file")
    parser.add_argument("-o", "--output", help="Output file (default: stdout)")
    parser.add_argument(
        "-s", "--style", choices=["IEEE", "APA"], default="IEEE", help="Output style"
    )
    parser.add_argument("-k", "--key", help="Process only this citation key")
    parser.add_argument("--validate", action="store_true", help="Validate entries")
    parser.add_argument("--sort", action="store_true", help="Sort by first author")
    parser.add_argument("--convert", choices=["APA"], help="Convert to another style")

    args = parser.parse_args()

    formatter = BibTeXFormatter(style=args.style)

    try:
        formatter.parse_file(args.input)
    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    # Validation
    if args.validate:
        errors = formatter.validate(args.key)
        if errors:
            print("Validation errors:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
        else:
            print("Validation passed!")
            sys.exit(0)

    # Sorting
    if args.sort:
        formatter.entries = formatter.sort_by_author()

    # Output
    if args.convert:
        output = formatter.convert_style(args.convert)
    else:
        if args.key:
            output = formatter.format_entry(args.key)
        else:
            output = formatter.format_all()

    if args.output:
        Path(args.output).write_text(output)
        print(f"Output written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
