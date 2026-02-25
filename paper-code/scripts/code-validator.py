#!/usr/bin/env python3
"""
Code Validator

Checks code quality for academic projects including linting,
type checking, import validation, and best practices.
"""

import subprocess
import sys
from typing import List, Dict, Any, Tuple
from pathlib import Path


class CodeValidator:
    """Validates code quality against academic standards."""

    CHECKERS = {
        "flake8": {
            "name": "flake8",
            "command": ["flake8", "flake8-python"],
            "install": "pip install flake8"
        },
        "black": {
            "name": "black",
            "command": ["black"],
            "install": "pip install black"
        },
        "mypy": {
            "name": "mypy",
            "command": ["mypy", "mypy"],
            "install": "pip install mypy"
        }
    }

    AVAILABLE_CHECKERS = ["flake8", "black", "mypy"]

    def __init__(self, project_path: str = "."):
        """Initialize code validator.

        Args:
            project_path: Root directory of project
        """
        self.project_path = Path(project_path).resolve()

        if not self.project_path.exists():
            raise FileNotFoundError(f"Project path does not exist: {project_path}")

    def check_linting(self, file_path: str) -> Dict[str, Any]:
        """Check code style with flake8.

        Args:
            file_path: Path to Python file or directory

        Returns:
            Validation result with errors and warnings
        """
        if "flake8" not in self.AVAILABLE_CHECKERS:
            return {
                "valid": True,
                "skipped": "flake8 not available",
                "errors": []
            }

        try:
            result = subprocess.run(
                ["flake8", file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                errors = []
                warnings = []

                for line in output.split('\n'):
                    if line.strip() and not line.startswith('  '):
                        errors.append(line.strip())
                    elif line.startswith('C90'):
                        errors.append(line.strip())
                    elif ': undefined' in line.lower() and 'import' in line.lower():
                        errors.append(line.strip())

                return {
                    "valid": len(errors) == 0,
                    "skipped": False,
                    "errors": errors,
                    "warnings": warnings
                }
            else:
                return {
                    "valid": False,
                    "skipped": True,
                    "errors": ["flake8 command failed"],
                    "warnings": []
                }

        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "skipped": True,
                "errors": ["flake8 timeout after 30 seconds"],
                "warnings": []
                }
        except Exception as e:
            return {
                "valid": False,
                "skipped": True,
                "errors": [f"Error: {e}"],
                "warnings": []
            }

    def check_black_formatting(self, file_path: str) -> Dict[str, Any]:
        """Check code formatting with black.

        Args:
            file_path: Path to Python file or directory

        Returns:
            Validation result with formatting issues
        """
        if "black" not in self.AVAILABLE_CHECKERS:
            return {
                "valid": True,
                "skipped": "black not available",
                "errors": [],
                "formatting_issues": []
            }

        try:
            result = subprocess.run(
                ["black", "--check", file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                formatting_issues = []

                for line in output.split('\n'):
                    if line.startswith('would reformat'):
                        formatting_issues.append(line.strip())

                return {
                    "valid": len(formatting_issues) == 0,
                    "skipped": False,
                    "errors": [],
                    "formatting_issues": formatting_issues
                }
            else:
                error_msg = result.stderr.strip() if result.stderr else ""
                return {
                    "valid": False,
                    "skipped": True,
                    "errors": [f"Black failed: {error_msg}"],
                    "formatting_issues": []
                }

        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "skipped": True,
                "errors": ["Black timeout after 30 seconds"],
                "formatting_issues": []
                }
        except Exception as e:
            return {
                "valid": False,
                "skipped": True,
                "errors": [f"Error: {e}"],
                "formatting_issues": []
            }

    def check_type_hints(self, file_path: str) -> Dict[str, Any]:
        """Check type hints with mypy.

        Args:
            file_path: Path to Python file

        Returns:
            Validation result with type issues
        """
        if "mypy" not in self.AVAILABLE_CHECKERS:
            return {
                "valid": True,
                "skipped": "mypy not available",
                "errors": []
            }

        try:
            result = subprocess.run(
                ["mypy", file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                output = result.stdout.strip()
                errors = []
                warnings = []

                for line in output.split('\n'):
                    if ': ' in line and 'note:' in line.lower():
                        errors.append(line.strip())
                    elif 'error:' in line.lower() or 'warning:' in line.lower():
                        errors.append(line.strip())

                return {
                    "valid": len(errors) == 0,
                    "skipped": False,
                    "errors": errors,
                    "warnings": warnings
                }
            else:
                error_msg = result.stderr.strip() if result.stderr else ""
                return {
                    "valid": False,
                    "skipped": True,
                    "errors": [f"Mypy failed: {error_msg}"],
                    "warnings": []
                }

        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "skipped": True,
                "errors": ["Mypy timeout after 30 seconds"],
                "warnings": []
            }
        except Exception as e:
            return {
                "valid": False,
                "skipped": True,
                "errors": [f"Error: {e}"],
                "warnings": []
            }

    def check_imports(self, file_path: str) -> Dict[str, Any]:
        """Check if all imports are available.

        Args:
            file_path: Path to Python file

        Returns:
            Validation result with missing imports
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            imports = []

            import ast
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.append(node.module)
                    for alias in node.names:
                        imports.append(f"{node.module}.{alias}")

            return {
                "valid": True,
                "skipped": False,
                "errors": [],
                "missing_imports": list(set(imports))
            }

        except SyntaxError as e:
            return {
                "valid": False,
                "skipped": False,
                "errors": [f"Syntax error: {e}"],
                "missing_imports": []
            }

    def validate_project(self, checkers: List[str] = None) -> Dict[str, Any]:
        """Run selected quality checks on the project.

        Args:
            checkers: List of checker names to run
                Options: ["flake8", "black", "mypy", "imports"]

        Returns:
            Complete validation report
        """
        if not self.project_path.exists():
            return {
                "valid": False,
                "skipped": True,
                "all_errors": [],
                "summary": "Project path does not exist"
            }

        results = {}

        if checkers is None:
            checkers = self.AVAILABLE_CHECKERS

        for checker in checkers:
            if checker == "flake8":
                results["flake8"] = self.check_linting(self.project_path)
            elif checker == "black":
                results["black"] = self.check_black_formatting(self.project_path)
            elif checker == "mypy":
                results["mypy"] = self.check_type_hints(self.project_path)
            elif checker == "imports":
                results["imports"] = self.check_imports(self.project_path)

        return results


def main():
    """CLI interface for code validator."""
    parser = argparse.ArgumentParser(
        description="Validate code quality for academic projects"
    )
    parser.add_argument(
        "project_path",
        default=".",
        help="Root directory of project"
    )
    parser.add_argument(
        "--checkers",
        nargs="+",
        choices=["flake8", "black", "mypy", "imports"],
        help="Checkers to run (default: all)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty print results"
    )

    args = parser.parse_args()

    validator = CodeValidator(args.project_path)

    if args.checkers is None:
        checkers = validator.AVAILABLE_CHECKERS

    results = validator.validate_project(args.checkers)

    if args.pretty:
        for checker, result in results.items():
            print(f"\n{checker.upper()}:")
            print("-" * 60)

            if not result["valid"]:
                print(f"  Status: {'FAILED'}")
                print(f"  Skipped: {result['skipped']}")

                for error in result.get("errors", []):
                    print(f"  ✗ {error}")
                for warning in result.get("warnings", []):
                    print(f"  ⚠ {warning}")
            else:
                print(f"  ✓ PASSED")

    print(f"\nSummary:")
    print(f"  Total checks: {len(results)}")
    failed_count = sum(1 for r in results.values() if not r["valid"])
    print(f"  Failed checks: {failed_count}")
    print(f"  Available checkers: {', '.join(validator.AVAILABLE_CHECKERS)}")


if __name__ == "__main__":
    main()
