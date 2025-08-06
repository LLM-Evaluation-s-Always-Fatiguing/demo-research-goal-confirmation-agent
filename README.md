# 研究目标澄清智能体

这个项目通过实现一个简单的研究目标澄清智能体，来展示上下文管理的一种动态上下文控制的范式。

# 快速开始

## 安装依赖

使用以下命令同步项目依赖：

```shell
uv sync
```

如果还未安装 `uv`，请参考[这里](https://docs.astral.sh/uv/getting-started/installation/)的说明先完成安装。

## 配置环境变量

将 `.env.example` 复制为 `.env`，并填充上所要求的各环境变量的真实值。

## 配置 `ag`

使用以下命令来配置 `ag` 以正常使用 `playground`:

```shell
uv run --no-project -- ag setup
```

## 启动 Playground

使用以下命令启动 playground 并体验 agent：

```shell
uv run --no-project -- python run_demo.py
```
