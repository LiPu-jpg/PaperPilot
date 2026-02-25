# OpenCode 配置总览

本文档汇总了当前项目配置的所有Skills和MCP服务。

## 📦 已安装的Skills

### 文档处理
| Skill | 用途 | 安装命令 |
|-------|------|----------|
| `pdf` | PDF文件处理 | `npx skills add davila7/claude-code-templates@pdf` ✅ 已安装 |
| `docx` | Word文档生成 | `npx skills add davila7/claude-code-templates@docx` ✅ 已安装 |
| `knowledge-graph-builder` | 知识图谱构建 | `npx skills add daffy0208/ai-dev-standards@Knowledge Graph Builder` ✅ 已安装 |

### 论文辅助Skills（本项目开发）
| Skill | 用途 | 路径 |
|-------|------|------|
| `paper-downloader` | 论文搜索与下载 | `.opencode/skills/paper-downloader/` |
| `paper-assistant` | 核心协调器 | `paper-assistant/SKILL.md` |
| `paper-literature-review` | 文献调研 | `paper-literature-review/SKILL.md` |
| `paper-hypothesis` | 假设生成 | `paper-hypothesis/SKILL.md` |
| `paper-code` | 代码编写 | `paper-code/SKILL.md` |
| `paper-experiment` | 实验执行 | `paper-experiment/SKILL.md` |
| `paper-writing` | 论文撰写 | `paper-writing/SKILL.md` |

## 🔌 已配置的MCP服务

### 1. Scientific Papers MCP

**包名**: `@futurelab-studio/latest-science-mcp`

**功能**:
- ✅ 搜索arXiv、OpenAlex、PubMed、bioRxiv
- ✅ 获取论文元数据和摘要
- ✅ 下载PDF文件
- ✅ 提取PDF文本内容

**配置** (`.opencode/mcp.json`):
```json
{
  "mcpServers": {
    "scientific-papers": {
      "type": "local",
      "command": ["npx", "-y", "@futurelab-studio/latest-science-mcp@latest"],
      "env": {
        "PAPER_DOWNLOAD_PATH": "./papers"
      }
    }
  }
}
```

**使用示例**:
```bash
# 搜索论文
npx -y @futurelab-studio/latest-science-mcp search-papers \
  --source=arxiv --query="machine learning" --count=5

# 获取最新论文
npx -y @futurelab-studio/latest-science-mcp fetch-latest \
  --source=arxiv --category=cs.AI --count=10
```

### 2. Semantic Scholar MCP (待配置)

**包名**: `@hamid-vakilzadeh/mcpsemanticscholar` (通过Smithery)

**功能**:
- 深度引用网络分析
- 作者学术背景调查
- 多维度论文搜索

**配置** (`.opencode/mcp.json`):
```json
{
  "mcpServers": {
    "semantic-scholar": {
      "type": "local",
      "command": ["npx", "-y", "@smithery/cli@latest"],
      "args": ["run", "@hamid-vakilzadeh/mcpsemanticscholar"]
    }
  }
}
```

**注意**: 此MCP需要通过Smithery运行。

## 📂 配置文件结构

```
.opencode/
├── mcp.json                          # MCP服务配置
├── MCP-README.md                     # MCP配置说明文档
└── skills/
    └── paper-downloader/
        └── SKILL.md                  # 论文下载Skill
```

## 🚀 快速使用指南

### 搜索论文

**方式1: 使用MCP命令**
```bash
npx -y @futurelab-studio/latest-science-mcp search-papers \
  --source=arxiv \
  --query="transformer architecture" \
  --count=10
```

**方式2: 在OpenCode对话中**
```
帮我搜索关于"transformer architecture"的arXiv论文
```

### 下载论文

**方式1: 直接下载**
```bash
mkdir -p ./papers
curl -L -o ./papers/2301.12345.pdf https://arxiv.org/pdf/2301.12345.pdf
```

**方式2: 使用MCP获取PDF链接后下载**
```bash
npx -y @futurelab-studio/latest-science-mcp fetch-content \
  --source=arxiv --id=2301.12345
# 从输出中提取PDF链接并下载
```

### 生成Word文档

使用已安装的docx skill:
```
创建一个Word文档，包含以下内容：
- 标题：研究计划
- 章节：1. 研究背景 2. 研究方法 3. 预期成果
```

### 处理PDF

使用已安装的pdf skill:
```
读取./papers/2301.12345.pdf的内容并总结
提取这篇PDF中的所有表格
```

### 构建知识图谱

使用已安装的knowledge-graph-builder skill:
```
基于这些论文构建一个知识图谱，显示研究主题之间的关系
```

## 🔧 故障排除

### MCP服务无法连接
1. 检查Node.js版本: `node --version`
2. 检查npm可访问性: `npm ping`
3. 测试MCP命令: `npx -y @futurelab-studio/latest-science-mcp --help`

### 下载失败
1. 检查网络连接: `curl -I https://arxiv.org`
2. 检查磁盘空间: `df -h`
3. 验证下载目录权限: `ls -la ./papers`

### Smithery运行失败
如果Semantic Scholar MCP无法运行:
```bash
# 手动安装并运行
git clone https://github.com/hamid-vakilzadeh/AIRA-SemanticScholar.git
cd AIRA-SemanticScholar
npm install
npm run build
# 然后修改mcp.json使用 build/index.js 作为command
```

## 📚 参考文档

- [MCP配置说明](./MCP-README.md) - 详细的MCP配置指南
- [paper-downloader Skill](./skills/paper-downloader/SKILL.md) - 论文下载Skill文档
- [项目README](../README.md) - 项目总览

## 🔄 更新检查

定期检查skills和MCP更新:

```bash
# 检查skills更新
npx skills check

# 更新所有skills
npx skills update

# 检查MCP更新（需手动检查GitHub/npm）
npm view @futurelab-studio/latest-science-mcp version
```

## 📝 待办事项

- [ ] 测试Semantic Scholar MCP通过Smithery运行
- [ ] 创建论文引用分析脚本
- [ ] 集成PDF文本提取到文献调研流程
- [ ] 添加更多学术数据库支持（IEEE, ACM等）
