# PaperPilot

AI-powered Paper Writing Skills - From topic selection to publication, all-in-one solution.

## ✨ Features

- **Complete Workflow**: Literature Review → Hypothesis Generation → Code Experiment → Paper Writing
- **Modular**: Each phase is independent and reusable
- **Context Management**: Auto-track research progress
- **Multi-disciplinary**: Templates for CS, ML, Biology, Psychology and more

## 📦 Installation

### Method 1: npm (Recommended)

```bash
# Install to OpenCode (default)
npm install paperpilot

# Or install to Claude Code
npm install paperpilot && npm run install:claude

# Or install to Codex
npm install paperpilot && npm run install:codex
```

### Method 2: Manual

```bash
# Clone project
git clone https://github.com/LiPu-jpg/PaperPilot.git
cd PaperPilot

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

Use directly in OpenCode/Claude Code/Codex:

```
Help me write a paper about [topic]
Search for literature related to [keywords]
Generate research hypotheses
Analyze experimental results
```

## 📁 Modules

| Module | Function | Use Case |
|--------|----------|----------|
| `paper-assistant` | Core Coordinator | Project init, workflow management |
| `paper-literature-review` | Literature Review | Search papers, generate review |
| `paper-hypothesis` | Hypothesis Generation | Design experiments, verify feasibility |
| `paper-code` | Code Generation | Scaffold, code review |
| `paper-experiment` | Experiment Execution | Run analysis, statistical tests |
| `paper-writing` | Paper Writing | Polishing, formatting, citations |

## 🔧 Using Scripts Manually

```bash
# Literature search
python paper-literature-review/scripts/arxiv-search.py "keywords" --max-results 10

# Hypothesis generation
python paper-hypothesis/scripts/hypothesis-generator.py --context-file .paper_context.json

# Code scaffold
python paper-code/scripts/code-scaffold.py classification --output ./my-project

# Run experiment
python paper-experiment/scripts/experiment-runner.py --config config.json

# Results analysis
python paper-experiment/scripts/results-analyzer.py results.json

# Bibliography formatting
python paper-writing/scripts/bibliography-formatter.py refs.bib --style IEEE
```

## 📋 Project Structure

```
PaperPilot/
├── paper-assistant/          # Core coordinator
├── paper-literature-review/  # Literature review
├── paper-hypothesis/         # Hypothesis generation
├── paper-code/              # Code writing
├── paper-experiment/        # Experiment execution
├── paper-writing/           # Paper writing
├── scripts/                 # Installation scripts
├── package.json
└── README.md
```

## 📄 License

MIT License

---

**Made with ❤️ for researchers**
