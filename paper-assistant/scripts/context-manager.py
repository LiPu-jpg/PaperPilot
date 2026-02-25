#!/usr/bin/env python3
"""
Context Manager for Paper Assistant

Manages .paper_context.json file for state persistence,
stage transitions, and context propagation across the paper writing workflow.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ContextManager:
    """Manages paper project context and state persistence."""

    STAGES_ORDER = ["literature_review", "hypothesis", "code", "experiment", "writing"]

    def __init__(self, project_path: str):
        """Initialize context manager for a project.

        Args:
            project_path: Root directory of the paper project

        Raises:
            ValueError: If project_path does not exist
        """
        self.project_path = Path(project_path).resolve()
        if not self.project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        self.context_file = self.project_path / ".paper_context.json"
        self.context: Dict[str, Any] = {}

    def load_context(self) -> Dict[str, Any]:
        """Load context from .paper_context.json file.

        Returns:
            Context dictionary with project metadata, stages, and preferences

        Raises:
            FileNotFoundError: If context file doesn't exist
            json.JSONDecodeError: If context file is invalid JSON
        """
        if not self.context_file.exists():
            raise FileNotFoundError(
                f"Context file not found: {self.context_file}. "
                "Use init_project() to create a new project."
            )

        try:
            with open(self.context_file, "r", encoding="utf-8") as f:
                self.context = json.load(f)
            return self.context.copy()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in context file: {e}")

    def save_context(self, context: Optional[Dict[str, Any]] = None) -> None:
        """Save context to .paper_context.json file.

        Args:
            context: Context dictionary to save. If None, saves current context.

        Raises:
            ValueError: If context is invalid
            IOError: If unable to write file
        """
        if context is not None:
            self._validate_context(context)
            self.context = context
        else:
            self._validate_context(self.context)

        if "project" not in self.context:
            self.context["project"] = {}
        self.context["project"]["last_updated"] = datetime.now().isoformat()

        try:
            with open(self.context_file, "w", encoding="utf-8") as f:
                json.dump(self.context, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise IOError(f"Failed to save context: {e}")

    def update_stage(self, stage: str, data: Dict[str, Any]) -> None:
        """Update a specific stage with new data.

        Args:
            stage: Stage name (literature_review, hypothesis, code, experiment, writing)
            data: Dictionary containing stage-specific data

        Raises:
            ValueError: If stage name is invalid or data is invalid
        """
        if stage not in self.STAGES_ORDER:
            raise ValueError(
                f"Invalid stage: {stage}. Valid stages: {', '.join(self.STAGES_ORDER)}"
            )

        if not isinstance(data, dict):
            raise ValueError("Stage data must be a dictionary")

        if "stages" not in self.context:
            self.context["stages"] = {}

        if stage not in self.context["stages"]:
            self.context["stages"][stage] = {}

        self.context["stages"][stage].update(data)

        if "status" not in data:
            self.context["stages"][stage]["status"] = "in_progress"

        self.context["current_stage"] = stage

    def rollback_to_stage(self, target_stage: str) -> None:
        """Rollback project to a previous stage.

        Resets all stages after target_stage to 'pending' status.
        Sets target_stage as current stage with 'in_progress' status.

        Args:
            target_stage: Stage to rollback to

        Raises:
            ValueError: If target_stage is not a valid stage name
        """
        if target_stage not in self.STAGES_ORDER:
            raise ValueError(f"Invalid target stage: {target_stage}")

        target_idx = self.STAGES_ORDER.index(target_stage)

        for stage in self.STAGES_ORDER[target_idx + 1 :]:
            if stage in self.context.get("stages", {}):
                self.context["stages"][stage]["status"] = "pending"

                stage_data = self.context["stages"][stage]
                stage_keys_to_keep = {"status"}
                for key in list(stage_data.keys()):
                    if key not in stage_keys_to_keep:
                        del stage_data[key]

        self.context["current_stage"] = target_stage
        self.context["stages"][target_stage]["status"] = "in_progress"

    def get_stage_output(self, stage: str) -> Dict[str, Any]:
        """Get output data for a specific stage.

        Args:
            stage: Stage name

        Returns:
            Dictionary containing stage output data

        Raises:
            ValueError: If stage is invalid or not found
        """
        if stage not in self.STAGES_ORDER:
            raise ValueError(f"Invalid stage: {stage}")

        if "stages" not in self.context or stage not in self.context["stages"]:
            raise ValueError(f"Stage data not found: {stage}")

        return self.context["stages"][stage].copy()

    def get_current_stage(self) -> str:
        """Get the current active stage.

        Returns:
            Current stage name

        Raises:
            ValueError: If no context is loaded
        """
        if not self.context or "current_stage" not in self.context:
            raise ValueError("No context loaded. Call load_context() first.")

        return self.context["current_stage"]

    def is_stage_complete(self, stage: str) -> bool:
        """Check if a stage is completed.

        Args:
            stage: Stage name

        Returns:
            True if stage status is 'completed', False otherwise
        """
        try:
            stage_data = self.get_stage_output(stage)
            return stage_data.get("status") == "completed"
        except ValueError:
            return False

    def set_stage_status(self, stage: str, status: str) -> None:
        """Set the status of a specific stage.

        Args:
            stage: Stage name
            status: New status (pending, in_progress, completed, failed)

        Raises:
            ValueError: If stage or status is invalid
        """
        valid_statuses = ["pending", "in_progress", "completed", "failed"]
        if status not in valid_statuses:
            raise ValueError(
                f"Invalid status: {status}. Valid statuses: {', '.join(valid_statuses)}"
            )

        if stage not in self.STAGES_ORDER:
            raise ValueError(f"Invalid stage: {stage}")

        if "stages" not in self.context:
            self.context["stages"] = {}

        if stage not in self.context["stages"]:
            self.context["stages"][stage] = {}

        self.context["stages"][stage]["status"] = status

    def get_user_preferences(self) -> Dict[str, Any]:
        """Get user preferences from context.

        Returns:
            Dictionary of user preferences (discipline, methodology, language, etc.)
        """
        return self.context.get("user_preferences", {})

    def set_user_preferences(self, preferences: Dict[str, Any]) -> None:
        """Update user preferences in context.

        Args:
            preferences: Dictionary of preference key-value pairs
        """
        if "user_preferences" not in self.context:
            self.context["user_preferences"] = {}

        self.context["user_preferences"].update(preferences)

    def _validate_context(self, context: Dict[str, Any]) -> None:
        """Validate context structure and required fields.

        Args:
            context: Context dictionary to validate

        Raises:
            ValueError: If context is invalid
        """
        if not isinstance(context, dict):
            raise ValueError("Context must be a dictionary")

        required_fields = ["project", "current_stage", "user_preferences"]
        for field in required_fields:
            if field not in context:
                raise ValueError(f"Missing required field: {field}")

        if "stages" not in context:
            raise ValueError("Missing 'stages' field in context")

    @classmethod
    def init_project(cls, project_path: str, **kwargs) -> "ContextManager":
        """Initialize a new paper project with default context.

        Args:
            project_path: Root directory for the project
            **kwargs: Additional configuration options

        Returns:
            ContextManager instance with initialized context
        """
        project_path_str = str(project_path)
        project_dir = Path(project_path_str).resolve()

        project_dir.mkdir(parents=True, exist_ok=True)

        manager = cls(project_path_str)

        default_context = {
            "project": {
                "name": kwargs.get("project_name", "my-paper"),
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
            },
            "current_stage": "literature_review",
            "stages": {
                "literature_review": {"status": "pending"},
                "hypothesis": {"status": "pending"},
                "code": {"status": "pending"},
                "experiment": {"status": "pending"},
                "writing": {"status": "pending"},
            },
            "user_preferences": {
                "discipline": kwargs.get("discipline", "cs"),
                "methodology": kwargs.get("methodology", "quantitative"),
                "language": kwargs.get("language", "zh"),
                "citation_style": kwargs.get("citation_style", "IEEE"),
            },
        }

        manager.context = default_context
        manager.save_context()

        return manager


def main():
    """CLI interface for context manager."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Manage paper project context and state"
    )
    parser.add_argument(
        "command",
        choices=["init", "load", "status", "rollback"],
        help="Command to execute",
    )
    parser.add_argument(
        "--project",
        default=".",
        help="Project root directory (default: current directory)",
    )
    parser.add_argument(
        "--stage",
        help="Target stage (for rollback command)"
    )

    # Init command options
    parser.add_argument(
        "--project-name",
        help="Project name (for init command)"
    )
    parser.add_argument(
        "--discipline",
        choices=["cs", "ml", "bio", "psych", "soc", "econ", "humanities", "general"],
        help="Discipline code (for init command)"
    )
    parser.add_argument(
        "--methodology",
        choices=["quantitative", "qualitative", "mixed"],
        help="Research methodology (for init command)"
    )
    parser.add_argument(
        "--language",
        choices=["zh", "en", "mixed"],
        help="Language preference (for init command)"
    )
    parser.add_argument(
        "--citation-style",
        choices=["IEEE", "APA", "MLA", "Chicago", "Vancouver"],
        help="Citation style (for init command)"
    )

    args = parser.parse_args()

    try:
        if args.command == "init":
            init_kwargs = {"project_path": args.project}
            if args.project_name:
                init_kwargs["project_name"] = args.project_name
            if args.discipline:
                init_kwargs["discipline"] = args.discipline
            if args.methodology:
                init_kwargs["methodology"] = args.methodology
            if args.language:
                init_kwargs["language"] = args.language
            if args.citation_style:
                init_kwargs["citation_style"] = args.citation_style

            manager = ContextManager.init_project(**init_kwargs)
            print(f"✓ Initialized paper project at {args.project}")
            print(f"  Context file: {manager.context_file}")
            manager = ContextManager.init_project(args.project)
            print(f"✓ Initialized paper project at {args.project}")
            print(f"  Context file: {manager.context_file}")

        elif args.command == "load":
            manager = ContextManager(args.project)
            context = manager.load_context()
            current_stage = context.get("current_stage", "unknown")
            print(f"Current stage: {current_stage}")
            print(f"Project: {context.get('project', {}).get('name', 'unknown')}")

        elif args.command == "status":
            manager = ContextManager(args.project)
            context = manager.load_context()

            print("\nProject Status:")
            print("=" * 50)

            for stage in ContextManager.STAGES_ORDER:
                stage_data = context.get("stages", {}).get(stage, {})
                status = stage_data.get("status", "pending")
                marker = "✓" if status == "completed" else "○"
                print(f"  {marker} {stage:20s} [{status}]")

            print("\nUser Preferences:")
            print("-" * 50)
            prefs = context.get("user_preferences", {})
            for key, value in prefs.items():
                print(f"  {key:20s}: {value}")

        elif args.command == "rollback":
            if not args.stage:
                parser.error("--stage is required for rollback command")

            manager = ContextManager(args.project)
            manager.load_context()
            manager.rollback_to_stage(args.stage)
            manager.save_context()

            print(f"✓ Rolled back to stage: {args.stage}")
            print(f"  Current stage: {manager.get_current_stage()}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
