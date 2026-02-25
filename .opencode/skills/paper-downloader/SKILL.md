---
name: paper-downloader
description: Use when downloading academic papers from arXiv, searching for papers, or managing paper downloads
---

# Paper Downloader Skill

用于搜索和下载学术论文的Skill，支持arXiv、OpenAlex等多个学术数据库。

## 依赖

本Skill依赖以下MCP服务（已配置在`.opencode/mcp.json`）：
- `@futurelab-studio/latest-science-mcp` - 主要搜索和下载工具
- `@hamid-vakilzadeh/mcpsemanticscholar` - Semantic Scholar深度分析（可选）

## 功能

### 1. 搜索论文

在多个学术数据库中搜索相关论文。

**支持的数据源**:
- `arxiv` - arXiv预印本
- `openalex` - OpenAlex学术图谱
- `pmc` - PubMed Central
- `europepmc` - 欧洲PMC
- `biorxiv` - 生物预印本
- `core` - CORE聚合资源

**使用示例**:
```
搜索arXiv上关于"machine learning"的最新论文
搜索OpenAlex上引用数超过100的"transformer"论文
在PubMed上搜索"cancer immunotherapy"相关论文
```

### 2. 下载论文

通过arXiv ID或其他标识符下载PDF文件。

**下载规则**:
- 默认保存路径: `./papers/`
- 文件命名: `{arxiv-id}.pdf` 或 `{title}.pdf`
- 自动创建目录（如果不存在）
- 验证下载完整性

**使用示例**:
```
下载arXiv论文2301.12345
下载论文2301.12345到./my-papers目录
批量下载这些论文: 2301.12345, 2302.23456, 2303.34567
```

### 3. 获取论文详情

获取论文的完整元数据、摘要和引用信息。

**使用示例**:
```
获取论文2301.12345的详细信息
分析这篇论文的引用网络
获取作者John Doe的所有论文
```

## 工作流程

### 场景1: 文献调研

1. **用户请求**: "帮我找几篇关于Rust内存安全的最新论文"
2. **搜索**: 使用`search-papers`命令在arXiv搜索
3. **展示结果**: 显示标题、作者、日期、PDF链接
4. **用户选择**: 用户确认感兴趣的论文
5. **下载**: 使用curl下载PDF到./papers/
6. **验证**: 确认文件大小合理

### 场景2: 批量下载

1. **用户提供**: 一系列arXiv ID列表
2. **创建目录**: 确保./papers/存在
3. **批量下载**: 并行下载多个PDF
4. **错误处理**: 记录下载失败的ID
5. **结果报告**: 显示成功/失败统计

### 场景3: 引用分析

1. **用户请求**: "分析这篇论文的引用网络"
2. **获取详情**: 使用MCP获取论文元数据
3. **提取引用**: 分析引用和被引用关系
4. **可视化**: 生成引用图谱（可选）

## 命令参考

### Scientific Papers MCP

```bash
# 列出分类
npx -y @futurelab-studio/latest-science-mcp list-categories --source=arxiv

# 搜索论文
npx -y @futurelab-studio/latest-science-mcp search-papers \
  --source=arxiv \
  --query="your search query" \
  --count=10

# 获取最新论文
npx -y @futurelab-studio/latest-science-mcp fetch-latest \
  --source=arxiv \
  --category=cs.AI \
  --count=20

# 获取高引用论文
npx -y @futurelab-studio/latest-science-mcp fetch-top-cited \
  --concept="machine learning" \
  --since=2024-01-01 \
  --count=50

# 获取论文详情
npx -y @futurelab-studio/latest-science-mcp fetch-content \
  --source=arxiv \
  --id=2301.12345
```

### 直接下载

```bash
# 使用curl下载
mkdir -p ./papers
curl -L -o ./papers/2301.12345.pdf https://arxiv.org/pdf/2301.12345.pdf

# 使用wget下载
wget -P ./papers https://arxiv.org/pdf/2301.12345.pdf
```

## 集成MCP

如果 `latest-science-mcp` 可用，优先使用它：
- 提供更智能的搜索
- 支持OpenAlex数据库
- 自动解析PDF内容

## 示例工作流

1. 用户请求: "帮我找几篇关于Rust内存安全的论文"
2. 搜索arXiv: 使用MCP的`search-papers`命令
3. 展示结果: 显示标题、作者、摘要、PDF链接
4. 用户选择: 确认要下载的论文
5. 执行下载: 使用`curl`或MCP下载PDF
6. 验证结果: 确认文件大小正确

## 下载规则

1. **下载路径**: 默认保存到 `./papers/` 目录
2. **文件命名**: 使用 `{arxiv-id}.pdf` 格式
3. **链接构建**: `https://arxiv.org/pdf/{id}.pdf`
4. **错误处理**: 
   - 检查ID格式（通常是4位年份+月份+序号）
   - 检查网络连接
   - 验证PDF是否正确下载

## 错误处理

### 常见错误

1. **网络错误**
   - 检查网络连接
   - 验证arXiv可访问性

2. **ID格式错误**
   - arXiv ID格式: `YYMM.number` (如: 2301.12345)
   - 旧格式: `category/YYMMnumber` (如: hep-ex/0307015)

3. **下载失败**
   - 检查磁盘空间
   - 验证下载路径可写

4. **PDF损坏**
   - 验证文件大小(通常>10KB)
   - 重新下载

## 相关Skills

- `paper-literature-review` - 文献调研和综述生成
- `paper-hypothesis` - 基于文献生成研究假设
- `paper-code` - 实验代码编写
- `paper-experiment` - 实验执行和结果分析
- `paper-writing` - 论文撰写

## 参考

- [arXiv API文档](https://arxiv.org/help/api)
- [OpenAlex API文档](https://docs.openalex.org/)
- [Semantic Scholar API](https://api.semanticscholar.org/corpus/)
- [Scientific Papers MCP](https://github.com/benedict2310/Scientific-Papers-MCP)
