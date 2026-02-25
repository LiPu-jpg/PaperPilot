"""
Code Scaffold Generator

Generate project templates for common experiment types.
"""

import argparse
import os
from pathlib import Path


TEMPLATES = {
    "classification": {
        "description": "Image/text classification experiment",
        "files": {
            "train.py": "Training script",
            "model.py": "Model definition",
            "dataset.py": "Data loading",
            "config.yaml": "Hyperparameters",
        },
    },
    "generation": {
        "description": "Text generation experiment",
        "files": {
            "train.py": "Training script",
            "model.py": "Model definition",
            "Tokenizer.py": "Tokenizer",
            "config.yaml": "Hyperparameters",
        },
    },
    "rl": {
        "description": "Reinforcement learning experiment",
        "files": {
            "train.py": "Training script",
            "env.py": "Environment",
            "agent.py": "Agent implementation",
            "config.yaml": "Hyperparameters",
        },
    },
    "baseline": {
        "description": "Baseline implementation template",
        "files": {
            "main.py": "Entry point",
            "model.py": "Model",
            "utils.py": "Utilities",
            "config.yaml": "Config",
        },
    },
}


def create_template(template_name: str, output_dir: str):
    """Create a project scaffold from template."""
    if template_name not in TEMPLATES:
        print(f"Available templates: {', '.join(TEMPLATES.keys())}")
        return

    template = TEMPLATES[template_name]
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for filename, description in template["files"].items():
        filepath = output_path / filename
        if not filepath.exists():
            filepath.write_text(f"# {description}\n# TODO: Implement\n")
            print(f"Created: {filepath}")

    print(f"\nTemplate '{template_name}' created in {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Generate code scaffold")
    parser.add_argument(
        "template", choices=list(TEMPLATES.keys()), help="Template type"
    )
    parser.add_argument("--output", "-o", default=".", help="Output directory")
    args = parser.parse_args()

    create_template(args.template, args.output)


if __name__ == "__main__":
    main()
