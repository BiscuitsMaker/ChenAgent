# Agent问答系统

基于LangChain的智能问答系统，支持RAG检索、工具调用和对话记忆。

## 功能特性

- **RAG检索**: 基于ChromaDB的向量检索
- **工具集成**: 支持博查搜索、Tavily搜索、Python计算
- **对话记忆**: 支持对话历史管理
- **多工具支持**: 可配置的工具组合

## 项目结构

```
食品安全抽检问答系统cursor/
├── agents/
│   ├── llm_agent.py          # 主Agent实现
│   ├── memory/
│   │   └── memory.py         # 记忆管理
│   ├── retriever/
│   │   ├── retriever.py      # RAG检索器
│   │   └── data/            # 知识库数据
│   └── tools/
│       └── tools.py          # 工具集合
├── config.py                # 配置文件
├── main.py                  # 主程序入口
└── requirements.txt         # 依赖包
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
# OpenAI配置
OPENAI_API_KEY=your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1

# 搜索工具配置
TAVILY_API_KEY=your-tavily-api-key
BOCHA_API_KEY=your-bocha-api-key
BOCHA_BASE_URL=your-bocha-base-url
```

### 3. 运行系统

```bash
python main.py
```

## 配置说明

在 `config.py` 中可以配置：

- **模型配置**: 模型名称、温度等
- **记忆配置**: 记忆类型和窗口大小
- **RAG配置**: 数据路径、分块大小等
- **工具配置**: 启用的工具列表

## 使用示例

启动后可以直接与Agent对话：

```
你：什么是食品安全？
Agent：[基于知识库的回答]

你：帮我搜索最新的食品安全新闻
Agent：[使用搜索工具获取信息]

你：计算一下 2^10 + 5*3
Agent：[使用Python计算工具]
```

## 工具说明

1. **博查搜索**: 使用博查AI进行网络搜索
2. **Tavily搜索**: 使用Tavily进行信息检索
3. **Python计算**: 执行数学计算和数据处理
4. **知识库检索**: 从本地向量数据库检索信息

## 故障排除

1. **API密钥错误**: 检查环境变量设置
2. **依赖安装失败**: 确保Python版本3.8+
3. **向量数据库错误**: 检查数据文件路径
