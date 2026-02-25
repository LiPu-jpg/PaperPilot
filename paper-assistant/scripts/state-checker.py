#!/usr/bin/env python3
"""
Stage Validator for Paper Assistant

Validates that each stage meets completion criteria before
transitioning to the next stage in the paper writing workflow.
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
import sys


@dataclass
class ValidationResult:
    """Result of stage validation."""

    valid: bool
    missing_fields: List[str]
    errors: List[str]


class StageValidator:
    """Validates stage completion status and data integrity.

    Each stage must meet specific criteria before the workflow
    can proceed to the next stage. The validator checks:
    - Required fields exist
    - Data formats are correct
    - Minimum quantity requirements
    - Stage-specific validation rules
    """

    LITERATURE_REVIEW_REQUIRED = ["research_gap", "key_papers", "summary"]

    HYPOTHESIS_REQUIRED = ["hypotheses", "experiment_designs", "feasibility"]

    CODE_REQUIRED = ["repo_url", "config"]

    EXPERIMENT_REQUIRED = ["results", "tables", "analysis"]

    WRITING_REQUIRED = ["sections", "drafts"]

    def validate_literature_review(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate literature review stage completion.

        Required:
            - research_gap: String articulating the identified gap
            - key_papers: List of analyzed papers (min 5)
            - summary: Synthesis of findings

        Args:
            context: Context dictionary with literature_review data

        Returns:
            ValidationResult with validation status and any issues
        """
        stage_data = context.get("stages", {}).get("literature_review", {})
        missing = []
        errors = []

        for field in self.LITERATURE_REVIEW_REQUIRED:
            if field not in stage_data or not stage_data[field]:
                missing.append(field)

        key_papers = stage_data.get("key_papers", [])
        if not isinstance(key_papers, list):
            errors.append("key_papers must be a list")
        elif len(key_papers) < 5:
            errors.append("At least 5 key papers required for literature review")

        research_gap = stage_data.get("research_gap", "")
        if not isinstance(research_gap, str) or len(research_gap) < 50:
            errors.append("research_gap must be a string with at least 50 characters")

        return ValidationResult(
            valid=len(missing) == 0 and len(errors) == 0,
            missing_fields=missing,
            errors=errors,
        )

    def validate_hypothesis(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate hypothesis generation stage completion.

        Required:
            - hypotheses: List of hypothesis statements (min 1)
            - experiment_designs: List of experiment designs
            - feasibility: Dict with data/method availability

        Args:
            context: Context dictionary with hypothesis data

        Returns:
            ValidationResult with validation status and any issues
        """
        stage_data = context.get("stages", {}).get("hypothesis", {})
        missing = []
        errors = []

        for field in self.HYPOTHESIS_REQUIRED:
            if field not in stage_data or not stage_data[field]:
                missing.append(field)

        hypotheses = stage_data.get("hypotheses", [])
        if not isinstance(hypotheses, list):
            errors.append("hypotheses must be a list")
        elif len(hypotheses) == 0:
            errors.append("At least one hypothesis required")

        feasibility = stage_data.get("feasibility", {})
        if not isinstance(feasibility, dict):
            errors.append("feasibility must be a dictionary")
        else:
            if "data" not in feasibility:
                errors.append("feasibility must specify data availability")
            if "method" not in feasibility:
                errors.append("feasibility must specify method feasibility")

        experiment_designs = stage_data.get("experiment_designs", [])
        if not isinstance(experiment_designs, list):
            errors.append("experiment_designs must be a list")
        elif len(experiment_designs) == 0:
            errors.append("At least one experiment design required")

        return ValidationResult(
            valid=len(missing) == 0 and len(errors) == 0,
            missing_fields=missing,
            errors=errors,
        )

    def validate_code(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate code implementation stage completion.

        Required:
            - repo_url: Path or URL to code repository
            - config: Configuration file path or dict

        Optional but recommended:
            - test_results: Test execution results
            - coverage: Test coverage metrics

        Args:
            context: Context dictionary with code data

        Returns:
            ValidationResult with validation status and any issues
        """
        stage_data = context.get("stages", {}).get("code", {})
        missing = []
        errors = []

        for field in self.CODE_REQUIRED:
            if field not in stage_data or not stage_data[field]:
                missing.append(field)

        repo_url = stage_data.get("repo_url", "")
        if not isinstance(repo_url, (str, type(None))):
            errors.append("repo_url must be a string")

        config = stage_data.get("config", "")
        if config is None or (not isinstance(config, (str, dict)) and config != ""):
            errors.append("config must be a string (path) or dictionary")

        return ValidationResult(
            valid=len(missing) == 0 and len(errors) == 0,
            missing_fields=missing,
            errors=errors,
        )

    def validate_experiment(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate experiment execution stage completion.

        Required:
            - results: Raw experiment results data
            - tables: Formatted result tables
            - analysis: Statistical analysis and significance tests

        Args:
            context: Context dictionary with experiment data

        Returns:
            ValidationResult with validation status and any issues
        """
        stage_data = context.get("stages", {}).get("experiment", {})
        missing = []
        errors = []

        for field in self.EXPERIMENT_REQUIRED:
            if field not in stage_data or not stage_data[field]:
                missing.append(field)

        results = stage_data.get("results", {})
        if not isinstance(results, dict):
            errors.append("results must be a dictionary")

        tables = stage_data.get("tables", [])
        if not isinstance(tables, list):
            errors.append("tables must be a list")
        elif len(tables) == 0:
            errors.append("At least one result table required")

        analysis = stage_data.get("analysis", "")
        if not analysis:
            errors.append("Statistical analysis required")

        return ValidationResult(
            valid=len(missing) == 0 and len(errors) == 0,
            missing_fields=missing,
            errors=errors,
        )

    def validate_writing(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate paper writing stage completion.

        Required:
            - sections: Dictionary of completed manuscript sections
            - drafts: List of draft files or content

        Optional but recommended:
            - abstract: Paper abstract
            - references: Formatted bibliography

        Args:
            context: Context dictionary with writing data

        Returns:
            ValidationResult with validation status and any issues
        """
        stage_data = context.get("stages", {}).get("writing", {})
        missing = []
        errors = []

        for field in self.WRITING_REQUIRED:
            if field not in stage_data or not stage_data[field]:
                missing.append(field)

        sections = stage_data.get("sections", {})
        if not isinstance(sections, dict):
            errors.append("sections must be a dictionary")

        drafts = stage_data.get("drafts", [])
        if not isinstance(drafts, list):
            errors.append("drafts must be a list")

        required_sections = [
            "abstract",
            "introduction",
            "method",
            "experiments",
            "conclusion",
        ]
        for section in required_sections:
            if section not in sections or not sections[section]:
                missing.append(f"section.{section}")

        return ValidationResult(
            valid=len(missing) == 0 and len(errors) == 0,
            missing_fields=missing,
            errors=errors,
        )

    def validate_transition(
        self, context: Dict[str, Any], from_stage: str, to_stage: str
    ) -> ValidationResult:
        """Validate that a stage transition is allowed.

        Checks:
        - Source stage is completed
        - Destination stage exists
        - Destination stage prerequisites are met

        Args:
            context: Full context dictionary
            from_stage: Current stage name
            to_stage: Next stage name

        Returns:
            ValidationResult indicating if transition is valid
        """
        errors = []
        stages_order = [
            "literature_review",
            "hypothesis",
            "code",
            "experiment",
            "writing",
        ]

        if from_stage not in stages_order:
            errors.append(f"Invalid source stage: {from_stage}")

        if to_stage not in stages_order:
            errors.append(f"Invalid destination stage: {to_stage}")

        if from_stage in stages_order and to_stage in stages_order:
            from_idx = stages_order.index(from_stage)
            to_idx = stages_order.index(to_stage)

            if to_idx <= from_idx:
                errors.append(
                    f"Cannot transition backward from {from_stage} to {to_stage}"
                )

            if to_idx > from_idx + 1:
                errors.append(f"Cannot skip stages from {from_stage} to {to_stage}")

        from_idx = stages_order.index(from_stage)
        source_valid = self.is_stage_complete(context, from_stage)

        if not source_valid:
            errors.append(f"Source stage {from_stage} is not completed")

        return ValidationResult(
            valid=len(errors) == 0, missing_fields=[], errors=errors
        )

    def is_stage_complete(self, context: Dict[str, Any], stage: str) -> bool:
        """Check if a specific stage is marked as completed.

        Args:
            context: Full context dictionary
            stage: Stage name to check

        Returns:
            True if stage status is 'completed', False otherwise
        """
        stages_order = [
            "literature_review",
            "hypothesis",
            "code",
            "experiment",
            "writing",
        ]
        if stage not in stages_order:
            return False

        stage_data = context.get("stages", {}).get(stage, {})
        return stage_data.get("status") == "completed"

    def validate_all(self, context: Dict[str, Any]) -> Dict[str, ValidationResult]:
        """Validate all stages in the workflow.

        Args:
            context: Full context dictionary

        Returns:
            Dictionary mapping stage names to ValidationResult
        """
        results = {
            "literature_review": self.validate_literature_review(context),
            "hypothesis": self.validate_hypothesis(context),
            "code": self.validate_code(context),
            "experiment": self.validate_experiment(context),
            "writing": self.validate_writing(context),
        }
        return results


def main():
    """CLI interface for stage validator."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate paper project stage completion status"
    )
    parser.add_argument(
        "stage",
        choices=[
            "literature_review",
            "hypothesis",
            "code",
            "experiment",
            "writing",
            "all",
        ],
        help="Stage to validate",
    )
    parser.add_argument(
        "--context-file", default=".paper_context.json", help="Path to context file"
    )
    parser.add_argument(
        "--json", action="store_true", help="Output validation results as JSON"
    )

    args = parser.parse_args()

    try:
        import json

        with open(args.context_file, "r", encoding="utf-8") as f:
            context = json.load(f)

        validator = StageValidator()

        if args.stage == "all":
            results = validator.validate_all(context)

            if args.json:
                json_results = {
                    stage: {
                        "valid": result.valid,
                        "missing": result.missing_fields,
                        "errors": result.errors,
                    }
                    for stage, result in results.items()
                }
                print(json.dumps(json_results, indent=2))
            else:
                print("\nValidation Results:")
                print("=" * 60)

                for stage, result in results.items():
                    status = "✓ PASS" if result.valid else "✗ FAIL"
                    print(f"\n{status}: {stage}")
                    if result.missing_fields:
                        print(f"  Missing: {', '.join(result.missing_fields)}")
                    if result.errors:
                        for error in result.errors:
                            print(f"  Error: {error}")

        else:
            validation_method = getattr(validator, f"validate_{args.stage}")
            result = validation_method(context)

            if args.json:
                json_result = {
                    "valid": result.valid,
                    "missing": result.missing_fields,
                    "errors": result.errors,
                }
                print(json.dumps(json_result, indent=2))
            else:
                status = "✓ PASS" if result.valid else "✗ FAIL"
                print(f"{status}: {args.stage}")

                if result.missing_fields:
                    print(f"  Missing: {', '.join(result.missing_fields)}")

                if result.errors:
                    for error in result.errors:
                        print(f"  Error: {error}")

    except FileNotFoundError:
        print(f"Error: Context file not found: {args.context_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in context file: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
