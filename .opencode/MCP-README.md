# MCP配置说明

本项目配置了多个MCP（Model Context Protocol）服务，用于增强论文研究和下载能力。

## 已配置的MCP服务

### 1. Scientific Papers MCP (FutureLab)
**包名**: `@futurelab-studio/latest-science-mcp`

**功能**:
- 搜索arXiv、OpenAlex、PubMed、bioRxiv等学术数据库
- 获取论文元数据和摘要
- 下载PDF文件
- 提取PDF文本内容

**使用方式**:
```bash
# 搜索论文
npx -y @futurelab-studio/latest-science-mcp search-papers \
  --source=arxiv --query="machine learning" --count=5

# 获取最新论文
npx -y @futurelab-studio/latest-science-mcp fetch-latest \
  --source=arxiv --category=cs.AI --count=10

# 获取高引用论文
npx -y @futurelab-studio/latest-science-mcp fetch-top-cited \
  --concept="machine learning" --since=2024-01-01 --count=20

# 获取论文详情
npx -y @futurelab-studio/latest-science-mcp fetch-content \
  --source=arxiv --id=2301.12345
```

**数据源支持**:
| 数据源 | 说明 |
|--------|------|
| arxiv | arXiv预印本论文库 |
| openalex | OpenAlex学术图谱 |
| pmc | PubMed Central |
| europepmc | 欧洲PMC |
| biorxiv | 生物预印本 |
| core | CORE聚合学术资源 |

### 2. Semantic Scholar MCP (AIRA)
**包名**: `@hamid-vakilzadeh/mcpsemanticscholar` (通过Smithery运行)

**功能**:
- 深度引用网络分析
- 作者学术背景调查
- 多维度论文搜索
- 领域特定研究浏览
- Wiley全文访问（需要TDM Token）

**使用方式**:
```bash
# 通过Smithery运行
npx -y @smithery/cli@latest run @hamid-vakilzadeh/mcpsemanticscholar
```

**注意**: 此MCP需要通过Smithery CLI运行，因为其未直接发布到npm。

## OpenCode集成

在OpenCode中，这些MCP服务会自动可用。你可以直接对话：

```
# 搜索论文
"帮我搜索关于transformer架构的最新arXiv论文"

# 下载论文
"下载arXiv论文2301.12345到./papers目录"

# 分析引用
"分析这篇论文的引用网络"
```

## 配置文件

MCP配置文件位于: `.opencode/mcp.json`

```json
{
  "mcpServers": {
    "scientific-papers": {
      "type": "local",
      "command": ["npx", "-y", "@futurelab-studio/latest-science-mcp@latest"],
      "env": {
        "PAPER_DOWNLOAD_PATH": "./papers"
      }
    },
    "semantic-scholar": {
      "type": "local",
      "command": ["npx", "-y", "@smithery/cli@latest"],
      "args": ["run", "@hamid-vakilzadeh/mcpsemanticscholar"]
    }
  }
}
```

## 下载路径

默认下载路径: `./papers/`

你可以在环境变量中修改：
```json
{
  "env": {
    "PAPER_DOWNLOAD_PATH": "/path/to/your/papers"
  }
}
```

## 故障排除

### 1. 命令未找到
确保Node.js和npm已正确安装：
```bash
node --version
npm --version
```

### 2. 下载失败
检查网络连接和arXiv可访问性：
```bash
curl -I https://arxiv.org/abs/2301.12345
```

### 3. Smithery运行失败
如果Semantic Scholar MCP无法通过Smithery运行，可以手动克隆并构建：
```bash
git clone https://github.com/hamid-vakilzadeh/AIRA-SemanticScholar.git
cd AIRA-SemanticScholar
npm install
npm run build
# 然后使用 build/index.js 作为command
```

## 相关资源

- [Scientific Papers MCP GitHub](https://github.com/benedict2310/Scientific-Papers-MCP)
- [AIRA Semantic Scholar GitHub](https://github.com/hamid-vakilzadeh/AIRA-SemanticScholar)
- [Smithery MCP Registry](https://smithery.ai/)
