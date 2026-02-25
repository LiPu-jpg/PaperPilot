#!/usr/bin/env python3
"""
Statistical Tester

Perform statistical tests on experiment results including t-tests, ANOVA,
Wilcoxon, and multiple comparison corrections.

Usage:
    python stat-tester.py --test ttest --group1 a.csv --group2 b.csv
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
from scipy import stats


def load_values(file_path: str) -> List[float]:
    """Load numeric values from CSV or JSON file."""
    
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    if suffix == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                if data and isinstance(data[0], dict):
                    values = []
                    for item in data:
                        for v in item.values():
                            if isinstance(v, (int, float)):
                                values.append(float(v))
                                break
                    return values
                return [float(x) for x in data if isinstance(x, (int, float))]
            return []
    elif suffix == ".csv":
        try:
            import pandas as pd
            df = pd.read_csv(file_path)
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    return df[col].dropna().tolist()
            return []
        except ImportError:
            print("Error: pandas required for CSV support")
            sys.exit(1)
    else:
        raise ValueError(f"Unsupported file format: {suffix}")


def cohens_d(group1: List[float], group2: List[float]) -> float:
    """Calculate Cohen's d effect size."""
    
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    if pooled_std == 0:
        return 0.0
    
    return (np.mean(group1) - np.mean(group2)) / pooled_std


def interpret_effect_size(d: float) -> str:
    """Interpret Cohen's d effect size."""
    
    d = abs(d)
    if d < 0.2:
        return "negligible"
    elif d < 0.5:
        return "small"
    elif d < 0.8:
        return "medium"
    else:
        return "large"


def t_test(
    group1: List[float],
    group2: List[float],
    paired: bool = False,
    alternative: str = "two-sided",
) -> Dict[str, Any]:
    """Perform independent or paired t-test."""
    
    if paired and len(group1) != len(group2):
        raise ValueError("Paired test requires equal group sizes")
    
    if paired:
        statistic, pvalue = stats.ttest_rel(group1, group2, alternative=alternative)
    else:
        statistic, pvalue = stats.ttest_ind(group1, group2, alternative=alternative)
    
    return {
        "test": "paired t-test" if paired else "independent t-test",
        "statistic": float(statistic),
        "p_value": float(pvalue),
        "effect_size": cohens_d(group1, group2),
        "effect_interpretation": interpret_effect_size(cohens_d(group1, group2)),
        "mean_group1": float(np.mean(group1)),
        "mean_group2": float(np.mean(group2)),
        "std_group1": float(np.std(group1, ddof=1)),
        "std_group2": float(np.std(group2, ddof=1)),
    }


def mann_whitney_test(
    group1: List[float],
    group2: List[float],
    alternative: str = "two-sided",
) -> Dict[str, Any]:
    """Perform Mann-Whitney U test (non-parametric)."""
    
    statistic, pvalue = stats.mannwhitneyu(group1, group2, alternative=alternative)
    
    n1, n2 = len(group1), len(group2)
    r = 1 - (2 * statistic) / (n1 * n2)
    
    return {
        "test": "Mann-Whitney U",
        "statistic": float(statistic),
        "p_value": float(pvalue),
        "effect_size": abs(r),
        "effect_interpretation": interpret_effect_size(abs(r)),
    }


def wilcoxon_test(
    group1: List[float],
    group2: List[float],
    alternative: str = "two-sided",
) -> Dict[str, Any]:
    """Perform Wilcoxon signed-rank test (paired non-parametric)."""
    
    if len(group1) != len(group2):
        raise ValueError("Wilcoxon test requires equal group sizes")
    
    statistic, pvalue = stats.wilcoxon(group1, group2, alternative=alternative)
    
    return {
        "test": "Wilcoxon signed-rank",
        "statistic": float(statistic),
        "p_value": float(pvalue),
    }


def anova_test(*groups: List[float]) -> Dict[str, Any]:
    """Perform one-way ANOVA."""
    
    statistic, pvalue = stats.f_oneway(*groups)
    
    group_means = [np.mean(g) for g in groups]
    grand_mean = np.mean([x for g in groups for x in g])
    
    ss_between = sum(len(g) * (m - grand_mean) ** 2 for g, m in zip(groups, group_means))
    ss_total = sum((x - grand_mean) ** 2 for g in groups for x in g)
    
    eta_squared = ss_between / ss_total if ss_total > 0 else 0
    
    return {
        "test": "One-way ANOVA",
        "statistic": float(statistic),
        "p_value": float(pvalue),
        "effect_size": eta_squared,
        "effect_interpretation": "large" if eta_squared > 0.14 else ("medium" if eta_squared > 0.06 else "small"),
        "num_groups": len(groups),
    }


def kruskal_test(*groups: List[float]) -> Dict[str, Any]:
    """Perform Kruskal-Wallis H test (non-parametric ANOVA)."""
    
    statistic, pvalue = stats.kruskal(*groups)
    
    return {
        "test": "Kruskal-Wallis H",
        "statistic": float(statistic),
        "p_value": float(pvalue),
        "num_groups": len(groups),
    }


def bonferroni_correction(pvalues: List[float], alpha: float = 0.05) -> List[Dict]:
    """Apply Bonferroni correction for multiple comparisons."""
    
    n = len(pvalues)
    corrected_alpha = alpha / n
    
    results = []
    for i, p in enumerate(pvalues):
        results.append({
            "comparison": i + 1,
            "original_p": p,
            "corrected_p": min(p * n, 1.0),
            "significant": p < corrected_alpha,
        })
    
    return results


def holm_bonferroni_correction(pvalues: List[float], alpha: float = 0.05) -> List[Dict]:
    """Apply Holm-Bonferroni correction for multiple comparisons."""
    
    n = len(pvalues)
    sorted_indices = np.argsort(pvalues)
    sorted_p = [pvalues[i] for i in sorted_indices]
    
    results = []
    for rank, (orig_idx, p) in enumerate(zip(sorted_indices, sorted_p), 1):
        corrected_alpha = alpha / (n - rank + 1)
        results.append({
            "comparison": orig_idx + 1,
            "original_p": p,
            "corrected_p": p * (n - rank + 1),
            "threshold": corrected_alpha,
            "significant": p < corrected_alpha,
        })
    
    results.sort(key=lambda x: x["comparison"])
    
    any_significant = False
    for r in results:
        if not any_significant:
            if r["significant"]:
                r["still_significant"] = True
            else:
                any_significant = True
                r["still_significant"] = False
        else:
            r["still_significant"] = False
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="Perform statistical tests on experiment results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument("--test", "-t", required=True,
                        choices=["ttest", "mannwhitney", "wilcoxon", "anova", "kruskal"],
                        help="Statistical test to perform")
    parser.add_argument("--group1", help="First group (CSV or JSON file)")
    parser.add_argument("--group2", help="Second group (CSV or JSON file)")
    parser.add_argument("--groups", nargs="+", help="Multiple groups for ANOVA")
    parser.add_argument("--paired", action="store_true", help="Use paired version of test")
    parser.add_argument("--alternative", choices=["two-sided", "greater", "less"],
                        default="two-sided", help="Alternative hypothesis")
    parser.add_argument("--alpha", type=float, default=0.05,
                        help="Significance level (default: 0.05)")
    parser.add_argument("--compare-more", nargs=2, action="append",
                        metavar=("GROUP1", "GROUP2"), help="Additional pairwise comparisons")
    parser.add_argument("--correction", choices=["bonferroni", "holm"],
                        help="Multiple comparison correction method")
    parser.add_argument("--output", "-o", help="Output JSON file")
    
    args = parser.parse_args()
    
    # Validate
    if args.test in ["ttest", "mannwhitney", "wilcoxon"]:
        if not args.group1 or not args.group2:
            parser.error(f"--test {args.test} requires --group1 and --group2")
    elif args.test in ["anova", "kruskal"]:
        if not args.groups or len(args.groups) < 2:
            parser.error(f"--test {args.test} requires at least 2 --groups")
    
    try:
        if args.test in ["ttest", "mannwhitney", "wilcoxon"]:
            group1 = load_values(args.group1)
            group2 = load_values(args.group2)
            
            if not group1 or not group2:
                print("Error: Failed to load values from files")
                sys.exit(1)
            
            if args.test == "ttest":
                result = t_test(group1, group2, paired=args.paired, alternative=args.alternative)
            elif args.test == "mannwhitney":
                result = mann_whitney_test(group1, group2, alternative=args.alternative)
            elif args.test == "wilcoxon":
                result = wilcoxon_test(group1, group2, alternative=args.alternative)
            
            results = {"main_test": result, "comparisons": []}
            
            if args.compare_more and args.correction:
                additional_pvalues = []
                comparison_results = []
                
                for g1_file, g2_file in args.compare_more:
                    g1 = load_values(g1_file)
                    g2 = load_values(g2_file)
                    
                    if args.test == "ttest":
                        comp_result = t_test(g1, g2, paired=args.paired)
                    else:
                        comp_result = mann_whitney_test(g1, g2)
                    
                    additional_pvalues.append(comp_result["p_value"])
                    comparison_results.append({
                        "group1": g1_file,
                        "group2": g2_file,
                        "p_value": comp_result["p_value"],
                    })
                
                if args.correction == "bonferroni":
                    corrections = bonferroni_correction(additional_pvalues, args.alpha)
                else:
                    corrections = holm_bonferroni_correction(additional_pvalues, args.alpha)
                
                for i, corr in enumerate(corrections):
                    comparison_results[i].update(corr)
                
                results["comparisons"] = comparison_results
        
        elif args.test in ["anova", "kruskal"]:
            groups = [load_values(g) for g in args.groups]
            
            if not all(groups):
                print("Error: Failed to load values from files")
                sys.exit(1)
            
            if args.test == "anova":
                result = anova_test(*groups)
            else:
                result = kruskal_test(*groups)
            
            results = {"main_test": result}
        
        main_p = results["main_test"]["p_value"]
        results["significant"] = main_p < args.alpha
        
        output_json = json.dumps(results, indent=2)
        
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(output_json)
            print(f"Results saved to: {args.output}")
        else:
            print(output_json)
        
        print(f"\n{'='*50}")
        print(f"Test: {results['main_test']['test']}")
        print(f"p-value: {main_p:.6f}")
        print(f"Significant at alpha={args.alpha}: {'Yes' if results['significant'] else 'No'}")
        
        if "effect_size" in results["main_test"]:
            es = results["main_test"]["effect_size"]
            ei = results["main_test"].get("effect_interpretation", "N/A")
            print(f"Effect size: {es:.4f} ({ei})")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
