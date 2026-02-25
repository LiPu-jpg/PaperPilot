# PaperPilot

AI辅助论文写作全流程Skills - 从选题到发表,一条龙服务。

[English](README-en.md) | 中文

## ✨ 特性

- **完整工作流**: 文献调研 → 假设生成 → 代码实验 → 论文撰写
- **模块化**: 每个阶段独立可复用
- **上下文管理**: 自动追踪研究进度
- **多学科**: CS、ML、生物，心理等学科模板

## 📦 安装

### 方式一: npm (推荐)

```bash
# 安装到 OpenCode (默认)
npm install paperpilot

# 或安装到 Claude Code
npm install paperpilot && npm run install:claude

# 或安装到 Codex
npm install paperpilot && npm run install:codex
```

### 方式二: 手动

```bash
# 克隆项目
git clone https://github.com/LiPu-jpg/PaperPilot.git
cd PaperPilot

# 安装依赖
pip install -r requirements.txt
```

## 🚀 使用

在 OpenCode/Claude Code/Codex 中直接使用:

```
帮我写一篇关于[主题]的论文
帮我搜索[关键词]相关的文献
帮我生成研究假设
帮我分析实验结果
```

## 📁 模块

| 模块 | 功能 | 使用场景 |
|------|------|----------|
| `paper-assistant` | 核心协调器 | 项目初始化、流程管理 |
| `paper-literature-review` | 文献调研 | 搜索论文、综述 |
| `paper-hypothesis` | 假设生成 | 设计实验、验证可行性 |
| `paper-code` | 代码生成 | 脚手架、代码审查 |
| `paper-experiment` | 实验执行 | 运行分析、统计检验 |
| `paper-writing` | 论文撰写 | 润色、格式、引用 |

## 🔧 手动使用脚本

```bash
# 文献搜索
python paper-literature-review/scripts/arxiv-search.py "关键词" --max-results 10

# 假设生成
python paper-hypothesis/scripts/hypothesis-generator.py --context-file .paper_context.json

# 代码脚手架
python paper-code/scripts/code-scaffold.py classification --output ./my-project

# 实验运行
python paper-experiment/scripts/experiment-runner.py --config config.json

# 结果分析
python paper-experiment/scripts/results-analyzer.py results.json

# 参考文献格式化
python paper-writing/scripts/bibliography-formatter.py refs.bib --style IEEE
```

## 📋 项目结构

```
PaperPilot/
├── paper-assistant/          # 核心协调器
├── paper-literature-review/  # 文献调研
├── paper-hypothesis/         # 假设生成
├── paper-code/              # 代码编写
├── paper-experiment/        # 实验执行
├── paper-writing/           # 论文撰写
├── scripts/                 # 安装脚本
├── package.json
└── README.md
```

## 📄 许可证

MIT License

---

**Made with ❤️ for researchers**
