#!/usr/bin/env python3
"""
Discipline Configuration Manager for Paper Assistant

Provides discipline-specific configurations for different academic fields,
including search APIs, code templates, experiment patterns, and writing styles.
"""

from typing import Dict, List, Optional, Any
import sys


class DisciplineConfig:
    """Manages discipline-specific configurations for paper writing.

    Different disciplines require different tools, templates, and conventions.
    This class provides centralized configuration management for all supported disciplines.
    """

    DISCIPLINES = {
        "cs": {
            "name": "Computer Science",
            "search_apis": ["arxiv", "semantic_scholar"],
            "code_template": "ml-template.py",
            "experiment_pattern": "ml_comparison",
            "writing_template": "cs_paper.md",
            "citation_style": "IEEE",
            "default_metrics": ["accuracy", "f1", "precision", "recall"],
        },
        "ml": {
            "name": "Machine Learning",
            "search_apis": ["arxiv", "semantic_scholar"],
            "code_template": "pytorch-template.py",
            "experiment_pattern": "hyperparameter_search",
            "writing_template": "ml_paper.md",
            "citation_style": "IEEE",
            "default_metrics": ["accuracy", "f1", "auc", "bleu", "rouge"],
        },
        "bio": {
            "name": "Biomedical",
            "search_apis": ["pubmed", "web_of_science"],
            "code_template": "r-analysis.R",
            "experiment_pattern": "clinical_trial",
            "writing_template": "bio_paper.md",
            "citation_style": "Vancouver",
            "default_metrics": ["p_value", "confidence_interval", "effect_size"],
        },
        "psych": {
            "name": "Psychology",
            "search_apis": ["psycinfo", "google_scholar"],
            "code_template": "survey-analysis.R",
            "experiment_pattern": "questionnaire",
            "writing_template": "psych_paper.md",
            "citation_style": "APA",
            "default_metrics": ["mean", "std", "correlation", "anova"],
        },
        "soc": {
            "name": "Sociology",
            "search_apis": ["google_scholar", "jstor"],
            "code_template": "qualitative-analysis.py",
            "experiment_pattern": "field_study",
            "writing_template": "soc_paper.md",
            "citation_style": "APA",
            "default_metrics": ["frequencies", "themes", "saturation"],
        },
        "econ": {
            "name": "Economics",
            "search_apis": ["jstor", "nber", "repec"],
            "code_template": "econometric-model.R",
            "experiment_pattern": "econometric_analysis",
            "writing_template": "econ_paper.md",
            "citation_style": "Chicago",
            "default_metrics": ["r_squared", "t_stat", "f_stat", "durbin_watson"],
        },
        "humanities": {
            "name": "Humanities & Social Sciences",
            "search_apis": ["google_scholar", "jstor"],
            "code_template": None,
            "experiment_pattern": None,
            "writing_template": "humanities_paper.md",
            "citation_style": "Chicago",
            "default_metrics": [],
        },
        "general": {
            "name": "General / Interdisciplinary",
            "search_apis": ["google_scholar", "semantic_scholar"],
            "code_template": "generic-template.py",
            "experiment_pattern": "generic",
            "writing_template": "generic_paper.md",
            "citation_style": "IEEE",
            "default_metrics": ["accuracy", "f1"],
        },
    }

    METHODOLOGIES = {
        "quantitative": {
            "name": "Quantitative",
            "description": "Statistical analysis with numerical data",
            "supported_disciplines": ["cs", "ml", "bio", "psych", "econ"],
        },
        "qualitative": {
            "name": "Qualitative",
            "description": "Thematic analysis of non-numerical data",
            "supported_disciplines": ["soc", "humanities"],
        },
        "mixed": {
            "name": "Mixed Methods",
            "description": "Combination of quantitative and qualitative",
            "supported_disciplines": ["psych", "soc", "humanities"],
        },
    }

    CITATION_STYLES = {
        "IEEE": {
            "name": "IEEE",
            "format": "Numbered citations [1], [2]",
            "fields": "number, title, author, year",
        },
        "APA": {
            "name": "APA",
            "format": "Author (Year) format",
            "fields": "author, year, title, source",
        },
        "MLA": {
            "name": "MLA",
            "format": "Author Page format",
            "fields": "author, page, title",
        },
        "Chicago": {
            "name": "Chicago",
            "format": "Footnote or author-date",
            "fields": "author, date, title",
        },
        "Vancouver": {
            "name": "Vancouver",
            "format": "Numbered in bibliography",
            "fields": "number, author, title, journal",
        },
    }

    def __init__(self, discipline: str):
        """Initialize discipline configuration.

        Args:
            discipline: Discipline code (cs, ml, bio, psych, soc, econ, humanities, general)

        Raises:
            ValueError: If discipline is not supported
        """
        self.discipline = discipline.lower()

        if self.discipline not in self.DISCIPLINES:
            supported = ", ".join(self.DISCIPLINES.keys())
            raise ValueError(
                f"Unsupported discipline: {discipline}. "
                f"Supported disciplines: {supported}"
            )

    def get_config(self) -> Dict[str, Any]:
        """Get full configuration for current discipline.

        Returns:
            Dictionary containing all discipline-specific settings
        """
        return self.DISCIPLINES[self.discipline].copy()

    def get_name(self) -> str:
        """Get human-readable discipline name.

        Returns:
            Discipline name as string
        """
        return self.get_config()["name"]

    def get_search_apis(self) -> List[str]:
        """Get list of search APIs for this discipline.

        Returns:
            List of API names
        """
        return self.get_config()["search_apis"]

    def get_code_template(self) -> Optional[str]:
        """Get default code template for this discipline.

        Returns:
            Template filename or None if not applicable
        """
        return self.get_config()["code_template"]

    def get_experiment_pattern(self) -> Optional[str]:
        """Get experiment pattern for this discipline.

        Returns:
            Pattern name or None if not applicable
        """
        return self.get_config()["experiment_pattern"]

    def get_writing_template(self) -> str:
        """Get writing template for this discipline.

        Returns:
            Template filename
        """
        return self.get_config()["writing_template"]

    def get_citation_style(self) -> str:
        """Get default citation style for this discipline.

        Returns:
            Citation style code (IEEE, APA, etc.)
        """
        return self.get_config()["citation_style"]

    def get_default_metrics(self) -> List[str]:
        """Get default evaluation metrics for this discipline.

        Returns:
            List of metric names
        """
        return self.get_config()["default_metrics"]

    def supports_methodology(self, methodology: str) -> bool:
        """Check if discipline supports a specific methodology.

        Args:
            methodology: Methodology code (quantitative, qualitative, mixed)

        Returns:
            True if methodology is supported, False otherwise
        """
        if methodology not in self.METHODOLOGIES:
            return False

        meth_config = self.METHODOLOGIES[methodology]
        return self.discipline in meth_config.get("supported_disciplines", [])

    @classmethod
    def list_disciplines(cls) -> Dict[str, str]:
        """List all supported disciplines.

        Returns:
            Dictionary mapping discipline codes to human-readable names
        """
        return {code: config["name"] for code, config in cls.DISCIPLINES.items()}

    @classmethod
    def list_methodologies(cls) -> Dict[str, str]:
        """List all supported methodologies.

        Returns:
            Dictionary mapping methodology codes to names
        """
        return {code: config["name"] for code, config in cls.METHODOLOGIES.items()}

    @classmethod
    def get_citation_style_info(cls, style: str) -> Optional[Dict[str, str]]:
        """Get information about a citation style.

        Args:
            style: Citation style code

        Returns:
            Dictionary with style info or None if not found
        """
        return cls.CITATION_STYLES.get(style.upper())

    def validate_preferences(self, preferences: Dict[str, str]) -> List[str]:
        """Validate user preferences against discipline capabilities.

        Args:
            preferences: User preference dictionary

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        discipline = preferences.get("discipline", self.discipline)
        if discipline not in self.DISCIPLINES:
            errors.append(f"Discipline {discipline} is not supported")

        methodology = preferences.get("methodology", "")
        if methodology and not self.supports_methodology(methodology):
            errors.append(
                f"Methodology {methodology} not supported by discipline {discipline}"
            )

        citation_style = preferences.get("citation_style", "")
        if citation_style and citation_style not in self.CITATION_STYLES:
            errors.append(f"Citation style {citation_style} is not supported")

        language = preferences.get("language", "")
        if language not in ["zh", "en", "mixed"]:
            errors.append(f"Language {language} must be zh, en, or mixed")

        return errors


def main():
    """CLI interface for discipline configuration."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description="Manage discipline-specific configurations for paper writing"
    )
    parser.add_argument(
        "command", choices=["list", "info", "validate"], help="Command to execute"
    )
    parser.add_argument(
        "--discipline", help="Discipline code (for info and validate commands)"
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    try:
        if args.command == "list":
            disciplines = DisciplineConfig.list_disciplines()

            if args.json:
                print(json.dumps(disciplines, indent=2))
            else:
                print("\nSupported Disciplines:")
                print("=" * 50)
                for code, name in disciplines.items():
                    print(f"  {code:12s} - {name}")

            print("\nSupported Methodologies:")
            print("-" * 50)
            methodologies = DisciplineConfig.list_methodologies()
            for code, name in methodologies.items():
                print(f"  {code:12s} - {name}")

        elif args.command == "info":
            if not args.discipline:
                parser.error("--discipline is required for info command")

            config = DisciplineConfig(args.discipline)

            info = {
                "name": config.get_name(),
                "search_apis": config.get_search_apis(),
                "code_template": config.get_code_template(),
                "experiment_pattern": config.get_experiment_pattern(),
                "writing_template": config.get_writing_template(),
                "citation_style": config.get_citation_style(),
                "default_metrics": config.get_default_metrics(),
            }

            if args.json:
                print(json.dumps(info, indent=2))
            else:
                print(f"\nDiscipline: {args.discipline}")
                print("=" * 50)
                for key, value in info.items():
                    if value is None:
                        continue
                    if isinstance(value, list):
                        value_str = ", ".join(value)
                    else:
                        value_str = str(value)
                    print(f"  {key:20s}: {value_str}")

        elif args.command == "validate":
            if not args.discipline:
                parser.error("--discipline is required for validate command")

            config = DisciplineConfig(args.discipline)

            sample_preferences = {
                "discipline": args.discipline,
                "methodology": "quantitative",
                "language": "zh",
                "citation_style": "IEEE",
            }

            errors = config.validate_preferences(sample_preferences)

            if errors:
                print(
                    f"Validation failed with {len(errors)} error(s):", file=sys.stderr
                )
                for error in errors:
                    print(f"  - {error}", file=sys.stderr)
                sys.exit(1)
            else:
                print("✓ Validation passed")

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
