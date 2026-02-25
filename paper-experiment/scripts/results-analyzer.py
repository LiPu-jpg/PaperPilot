#!/usr/bin/env python3
"""
Results Analyzer

Analyze experiment results from CSV/JSON files and generate summary statistics,
tables, and visualizations for academic papers.

Usage:
    python results-analyzer.py --input results.csv --output analysis/
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np


def load_data(file_path: str) -> List[Dict]:
    """Load experiment results from CSV or JSON file."""

    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return [data]
    elif suffix == ".csv":
        try:
            import pandas as pd

            df = pd.read_csv(file_path)
            return df.to_dict("records")
        except ImportError:
            print(
                "Error: pandas required for CSV support. Install with: pip install pandas"
            )
            sys.exit(1)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def calculate_statistics(values: List[float]) -> Dict[str, float]:
    """Calculate summary statistics for a list of values."""

    if not values:
        return {}

    arr = np.array(values)

    return {
        "count": len(values),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr, ddof=1)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "median": float(np.median(arr)),
        "q25": float(np.percentile(arr, 25)),
        "q75": float(np.percentile(arr, 75)),
    }


def calculate_confidence_interval(
    values: List[float],
    confidence: float = 0.95,
) -> Dict[str, float]:
    """Calculate confidence interval for mean."""

    if len(values) < 2:
        return {"mean": np.mean(values), "ci_lower": values[0], "ci_upper": values[0]}

    arr = np.array(values)
    mean = np.mean(arr)
    se = np.std(arr, ddof=1) / np.sqrt(len(arr))

    # t-distribution approximation (using 1.96 for 95% CI)
    from scipy import stats

    t_val = stats.t.ppf((1 + confidence) / 2, len(arr) - 1)

    return {
        "mean": float(mean),
        "ci_lower": float(mean - t_val * se),
        "ci_upper": float(mean + t_val * se),
    }


def generate_latex_table(
    results: Dict[str, Dict[str, float]],
    metric_name: str = "Value",
    caption: str = "Experiment Results",
    label: str = "tab:results",
) -> str:
    """Generate LaTeX table from results."""

    lines = []
    lines.append("\\begin{table}[htbp]")
    lines.append("\\centering")
    lines.append(f"\\caption{{{caption}}}")
    lines.append(f"\\label{{{label}}}")
    lines.append("\\begin{tabular}{lrrr}")
    lines.append("\\hline")
    lines.append("Method & Mean & Std Dev & 95\\% CI \\\\")
    lines.append("\\hline")

    for method, stats in results.items():
        mean = stats.get("mean", 0)
        std = stats.get("std", 0)
        ci_lower = stats.get("ci_lower", mean - std)
        ci_upper = stats.get("ci_upper", mean + std)

        lines.append(
            f"{method} & {mean:.4f} & {std:.4f} & [{ci_lower:.4f}, {ci_upper:.4f}] \\\\"
        )

    lines.append("\\hline")
    lines.append("\\end{tabular}")
    lines.append("\\end{table}")

    return "\n".join(lines)


def analyze_by_column(
    data: List[Dict],
    group_column: str,
    value_column: str,
) -> Dict[str, Dict[str, float]]:
    """Analyze results grouped by a column."""

    groups: Dict[str, List[float]] = {}

    for row in data:
        group = str(row.get(group_column, "unknown"))
        try:
            value = float(row.get(value_column, 0))
            if group not in groups:
                groups[group] = []
            groups[group].append(value)
        except (ValueError, TypeError):
            continue

    results = {}
    for group, values in groups.items():
        stats = calculate_statistics(values)
        ci = calculate_confidence_interval(values)
        stats.update(ci)
        results[group] = stats

    return results


def analyze_all_columns(
    data: List[Dict],
    value_columns: Optional[List[str]] = None,
) -> Dict[str, Dict[str, float]]:
    """Analyze all numeric columns in the data."""

    if not data:
        return {}

    # Find numeric columns
    if value_columns is None:
        value_columns = []
        for key, value in data[0].items():
            if isinstance(value, (int, float)):
                value_columns.append(key)

    results = {}
    for col in value_columns:
        values = []
        for row in data:
            try:
                values.append(float(row.get(col, 0)))
            except (ValueError, TypeError):
                continue

        if values:
            stats = calculate_statistics(values)
            ci = calculate_confidence_interval(values)
            stats.update(ci)
            results[col] = stats

    return results


def create_comparison_chart(
    results: Dict[str, Dict[str, float]],
    output_path: str,
) -> None:
    """Create comparison bar chart with error bars."""

    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("Warning: matplotlib not installed. Skipping chart creation.")
        return

    methods = list(results.keys())
    means = [results[m].get("mean", 0) for m in methods]
    stds = [results[m].get("std", 0) for m in methods]

    plt.figure(figsize=(10, 6))
    plt.bar(methods, means, yerr=stds, capsize=5, alpha=0.7)
    plt.ylabel("Score")
    plt.title("Experiment Results Comparison")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()

    print(f"Chart saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze experiment results and generate tables for papers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python results-analyzer.py --input results.csv --output analysis/
    python results-analyzer.py --input results.json --group-by model --value accuracy
    python results-analyzer.py --input results.csv --latex --output table.tex
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input CSV or JSON file with experiment results",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Output directory or file",
    )
    parser.add_argument(
        "--group-by",
        help="Column to group results by (for comparison tables)",
    )
    parser.add_argument(
        "--value",
        help="Value column to analyze (required with --group-by)",
    )
    parser.add_argument(
        "--columns",
        nargs="+",
        help="Specific columns to analyze (analyzes all numeric if not specified)",
    )
    parser.add_argument(
        "--latex",
        action="store_true",
        help="Generate LaTeX table output",
    )
    parser.add_argument(
        "--chart",
        action="store_true",
        help="Generate comparison chart (requires matplotlib)",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.95,
        help="Confidence level (default: 0.95)",
    )
    parser.add_argument(
        "--format",
        choices=["json", "text"],
        default="json",
        help="Output format (default: json)",
    )

    args = parser.parse_args()

    try:
        # Load data
        data = load_data(args.input)

        if not data:
            print("Error: No data found in input file")
            sys.exit(1)

        print(f"Loaded {len(data)} records from {args.input}")

        # Analyze data
        if args.group_by and args.value:
            results = analyze_by_column(data, args.group_by, args.value)
        else:
            results = analyze_all_columns(data, args.columns)

        if not results:
            print("Error: No numeric columns found for analysis")
            sys.exit(1)

        # Output results
        output_path = args.output or "analysis"

        if args.latex:
            latex = generate_latex_table(results)

            if output_path:
                output_file = (
                    f"{output_path}.tex"
                    if not output_path.endswith(".tex")
                    else output_path
                )
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(latex)
                print(f"LaTeX table saved to: {output_file}")
            else:
                print("\n" + latex)
        else:
            if args.format == "json":
                output_data = json.dumps(results, indent=2)

                if output_path:
                    output_file = (
                        f"{output_path}.json"
                        if not output_path.endswith(".json")
                        else output_path
                    )
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(output_data)
                    print(f"Results saved to: {output_file}")
                else:
                    print(output_data)
            else:
                # Text format
                print("\nSummary Statistics:")
                print("=" * 60)

                for metric, stats in results.items():
                    print(f"\n{metric}:")
                    print(f"  Mean: {stats.get('mean', 0):.4f}")
                    print(f"  Std:  {stats.get('std', 0):.4f}")
                    print(
                        f"  95% CI: [{stats.get('ci_lower', 0):.4f}, {stats.get('ci_upper', 0):.4f}]"
                    )

        # Generate chart if requested
        if args.chart:
            chart_path = f"{output_path}_chart.png" if output_path else "comparison.png"
            create_comparison_chart(results, chart_path)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
