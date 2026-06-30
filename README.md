# 🌿 省域绿色算力承载能力评估与资源布局决策支持系统

> Green Computing Resource Carrying Capacity Assessment & Layout Decision Support System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791.svg)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6.svg)](https://www.typescriptlang.org/)

---

## 📖 目录

- [项目简介](#项目简介)
- [核心功能](#核心功能)
- [技术栈](#技术栈)
- [系统架构](#系统架构)
- [项目结构](#项目结构)
- [功能页面](#功能页面)
- [API 接口](#api-接口)
- [智能问答模块](#智能问答模块)
- [本地开发](#本地开发)
- [服务器部署](#服务器部署)
- [宝塔面板部署](#宝塔面板部署)
- [数据库设计](#数据库设计)
- [常见问题](#常见问题)

---

## 项目简介

随着国家"东数西算"工程的深入推进和"双碳"目标的加速落地，省域绿色算力承载能力已成为衡量区域数字经济发展潜力的核心指标之一。本系统以 **2016—2024 年中国 31 个省级行政区**的多源面板数据为基础，通过 TOPSIS 综合评价、Dagum 区域差异分解、Moran's I 空间自相关、Markov 动态演化模型、LPA 潜在剖面分析、SHAP 可解释性分析和障碍度诊断等方法，构建了从"**数据汇聚 → 模型评价 → 空间诊断 → 类型识别 → 布局决策 → 智能问答**"的完整应用闭环。

系统面向四类用户提供全链条决策支持：

| 用户类型 | 核心需求 |
|----------|----------|
| 🏛️ 政府部门 | 掌握各省绿色算力发展水平，制定区域政策 |
| 🏢 数据中心企业 | 评估算力基础设施布局选址适宜度 |
| ⚡ 能源规划机构 | 分析能源供给与碳排放约束对算力布局的影响 |
| 🎓 研究人员 | 查询模型结果、对比分析方法差异 |

---

## 核心功能

### 📊 数据驾驶舱（10 个功能页面）

- **首页总览** — 全国宏观概览、Top 排名、区域分布统计
- **综合评价** — TOPSIS 综合得分排名、南丁格尔玫瑰图
- **区域差异** — Dagum 基尼系数分解（区域内 + 区域间 + 超变密度）
- **空间聚焦** — 中国地图 Choropleth + Moran's I + LISA 聚集分析
- **动态演化** — Markov 转移概率矩阵 + 传统/空间 Markov 对比
- **省域诊断** — 障碍度诊断（首要/次要障碍维度、短板类型识别）
- **类型识别** — LPA 潜在剖面分析（4 类发展类型 + 动态轨迹）
- **SHAP 解释** — 特征重要性 + 局部瀑布图 + 年度贡献分解
- **布局决策** — 省域布局推荐（优势指数、功能定位、优化策略、风险预警）
- **智能问答** — 自然语言查询，RAG + DeepSeek 大模型

### 🤖 智能问答

- **RAG 检索增强生成**：TF-IDF 向量化 + 10 篇专业知识文档
- **问题自动分类**：6 类问题路由（排名查询、省份诊断、布局建议、趋势预测、模型说明、知识问答）
- **10 个数据库工具**：自动调用数据库查询获取实时数据
- **离线降级**：LLM 不可用时自动切换离线模式

### 📈 可视化能力

支持 **10+ 种** ECharts 高级图表类型：

| 图表 | 用途 |
|------|------|
| 🗺️ 中国地图 Choropleth | 空间分布可视化 |
| 🌹 南丁格尔玫瑰图 | 指标雷达对比 |
| 🍩 环形饼图 | 区域占比分析 |
| 📊 横向排名条 | 31 省排名对比 |
| 📈 折线图 / 面积图 | 时间序列趋势 |
| 📉 堆叠柱状图 | 维度分解 |
| 🌊 SHAP 瀑布图 | 特征贡献解释 |
| 🔥 热力矩阵 | 转移概率可视化 |

---

## 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| [FastAPI](https://fastapi.tiangolo.com/) | ≥ 0.110 | 异步 Web 框架，自动生成 Swagger/ReDoc 文档 |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ≥ 2.0 | ORM 数据库访问，连接池管理 |
| [PostgreSQL](https://www.postgresql.org/) | 18 | 关系型数据库，42 张业务表 |
| [Pydantic](https://docs.pydantic.dev/) | ≥ 2.0 | 数据校验与序列化 |
| [Uvicorn](https://www.uvicorn.org/) | ≥ 0.27 | ASGI 服务器 |
| [scikit-learn](https://scikit-learn.org/) | ≥ 1.3 | TF-IDF 向量化（RAG 模块） |
| [pandas](https://pandas.pydata.org/) / [openpyxl](https://openpyxl.readthedocs.io/) | ≥ 2.0 / ≥ 3.1 | Excel 数据导入管道 |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| [Next.js](https://nextjs.org/) | ^15.0 | React 全栈框架（App Router） |
| [React](https://react.dev/) | ^19.0 | UI 组件库 |
| [TypeScript](https://www.typescriptlang.org/) | ^5.6 | 类型安全 |
| [Tailwind CSS](https://tailwindcss.com/) | ^3.4 | 深色科技风响应式样式 |
| [ECharts](https://echarts.apache.org/) | ^5.5 | 数据可视化（10+ 种图表） |
| [echarts-for-react](https://github.com/hustcc/echarts-for-react) | ^3.0 | React ECharts 封装 |

### AI / LLM

| 组件 | 说明 |
|------|------|
| DeepSeek Chat API | 智能问答大语言模型 |
| TF-IDF 向量化 | 知识库文档检索（Chroma 可选） |
| RAG 管道 | 检索增强生成：检索 → 上下文拼接 → LLM 生成 |

---

## 系统架构

```
┌─────────────────────────────────────────────────┐
│                    用户浏览器                      │
│               http://your-domain.com              │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              Nginx (反向代理)                      │
│          / → 3000    /api/* → 8000               │
└────────┬───────────────────────┬────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐   ┌─────────────────────────┐
│  Next.js 前端    │   │   FastAPI 后端 (8000)    │
│  (端口 3000)     │   │                         │
│                 │   │  ┌───────────────────┐  │
│  • 10 页面      │   │  │  API Routes       │  │
│  • ECharts 图表  │   │  │  /api/provinces   │  │
│  • Tailwind CSS │   │  │  /api/scores      │  │
│  • Dark Theme   │   │  │  /api/obstacles   │  │
│                 │   │  │  ... (14 端点)     │  │
└─────────────────┘   │  ├───────────────────┤  │
                       │  │  Service Layer    │  │
                       │  │  11 业务服务模块   │  │
                       │  ├───────────────────┤  │
                       │  │  SQLAlchemy ORM   │  │
                       │  │  23 数据模型       │  │
                       │  ├───────────────────┤  │
                       │  │  Agent / RAG      │  │
                       │  │  智能问答模块       │  │
                       │  └───────────────────┘  │
                       └───────────┬─────────────┘
                                   │
                                   ▼
                       ┌─────────────────────────┐
                       │   PostgreSQL 数据库       │
                       │   42 张表 · 8 大业务类别   │
                       └─────────────────────────┘
```

**五层架构**：数据资源层 → 数据存储层 → 后端服务层 → 前端展示层 → 应用交互层

---

## 项目结构

```
green-compute-system/
│
├── backend/                        # FastAPI 后端
│   ├── app/                        # 应用核心
│   │   ├── main.py                 # FastAPI 入口（CORS、路由注册、健康检查）
│   │   ├── database.py             # SQLAlchemy 引擎 + 连接池配置
│   │   ├── models.py               # 23 个 ORM 数据模型
│   │   ├── schemas.py              # 30 个 Pydantic 响应模型
│   │   ├── api/
│   │   │   └── routes.py           # 14 个 RESTful API 端点
│   │   └── services/               # 11 个业务服务模块
│   │       ├── province.py         # 省份信息服务
│   │       ├── score.py            # TOPSIS 得分服务
│   │       ├── overview.py         # 首页总览聚合
│   │       ├── obstacle.py         # 障碍度诊断服务
│   │       ├── lpa.py              # LPA 类型分析服务
│   │       ├── shap.py             # SHAP 解释服务
│   │       ├── layout.py           # 布局决策服务
│   │       ├── indicator.py        # 指标体系服务
│   │       ├── dagum.py            # Dagum 分解服务
│   │       ├── moran.py            # Moran's I 空间分析服务
│   │       └── markov.py           # Markov 转移矩阵服务
│   │
│   ├── agent/                      # 🤖 智能问答模块
│   │   ├── router.py               # POST /api/chat 端点
│   │   ├── chat_service.py         # 对话编排（分类 → 检索 → 工具调用 → 生成）
│   │   ├── tools.py                # 10 个数据库查询工具函数
│   │   ├── prompts.py              # LLM 系统提示词模板
│   │   └── rate_limit.py           # 频率限制
│   │
│   ├── db/
│   │   ├── database.py             # 导入器数据库连接
│   │   └── schema.sql              # 42 张表的完整建表语句
│   │
│   ├── importers/
│   │   ├── import_excel_to_db.py   # Excel → PostgreSQL 数据导入管道
│   │   ├── inspect_excel_files.py  # Excel 文件扫描工具
│   │   └── data_import_config.yaml # 字段映射配置（10 个 Excel → 42 张表）
│   │
│   └── rag/
│       ├── build_index.py          # TF-IDF 向量索引构建
│       ├── retriever.py            # 知识库检索器
│       └── rag_docs/               # 10 篇 RAG 知识库文档
│           ├── 01_system_overview.md
│           ├── 02_topsis_model.md
│           ├── 03_lpa_model.md
│           ├── 04_spatial_evolution.md
│           ├── 05_obstacle_model.md
│           ├── 06_shap_model.md
│           ├── 07_layout_rules.md
│           ├── 08_future_prediction_rules.md
│           ├── 09_indicators.md
│           └── 10_faq.md
│
├── frontend/                       # Next.js 15 前端
│   ├── public/
│   │   └── china.json              # 中国省级 GeoJSON 地图数据
│   ├── src/
│   │   ├── app/                    # App Router 页面（10 个页面）
│   │   │   ├── page.tsx            # / → 自动跳转 /dashboard
│   │   │   ├── layout.tsx          # 全局布局（侧边栏 + 顶栏 + 内容区）
│   │   │   ├── dashboard/          # 首页总览
│   │   │   ├── evaluation/         # 综合评价
│   │   │   ├── regional-difference/# 区域差异
│   │   │   ├── spatial-cluster/    # 空间聚焦
│   │   │   ├── dynamic-evolution/  # 动态演化
│   │   │   ├── province-diagnosis/ # 省域诊断
│   │   │   ├── type-identification/# 类型识别
│   │   │   ├── shap/               # SHAP 解释
│   │   │   ├── layout-decision/    # 布局决策
│   │   │   └── chat/               # 智能问答
│   │   ├── components/
│   │   │   ├── charts/             # 10 个可复用 ECharts 图表组件
│   │   │   │   ├── ChinaMap.tsx
│   │   │   │   ├── DonutChart.tsx
│   │   │   │   ├── RoseChart.tsx
│   │   │   │   ├── RankingBar.tsx
│   │   │   │   ├── LineChart.tsx
│   │   │   │   ├── AreaChart.tsx
│   │   │   │   ├── StackedBar.tsx
│   │   │   │   ├── BarChart.tsx
│   │   │   │   ├── ShapWaterfall.tsx
│   │   │   │   └── RegionChart.tsx
│   │   │   ├── chat/               # 聊天 UI 组件
│   │   │   ├── Sidebar.tsx         # 导航侧边栏
│   │   │   ├── Header.tsx          # 顶部状态栏
│   │   │   └── ...
│   │   └── lib/
│   │       └── api.ts              # 类型化 API 客户端（12 数据 + 1 聊天）
│   ├── next.config.js              # standalone 输出 + API 代理重写
│   ├── tailwind.config.js          # 深色科技风主题
│   ├── tsconfig.json
│   └── package.json
│
├── data/                           # 数据文件
│   ├── raw/                        # 11 个 Excel 源数据文件
│   │   ├── clean_data.xlsx         # 清洗后的面板数据
│   │   ├── 表2-1_指标体系.xlsx
│   │   ├── 表3-1_标准化数据.xlsx
│   │   ├── 表3-2_组合权重结果.xlsx
│   │   ├── 表3-3_绿色算力综合得分(1).xlsx
│   │   ├── 第1章_数据治理报告(1).xlsx
│   │   ├── 第4章_LPA结果表(1).xlsx
│   │   ├── 第5章_空间演化分析结果表(1).xlsx
│   │   ├── 第6章_障碍度模型结果表(1).xlsx
│   │   ├── 第7章_SHAP解释分析结果表(1).xlsx
│   │   └── 第8章_布局决策结果表.xlsx
│   ├── metadata/
│   │   └── data_dictionary.xlsx    # 数据字典
│   └── vector_store/               # 持久化的 TF-IDF 向量索引
│
├── deploy/                         # 🚀 部署配置文件
│   ├── setup.sh                    # 服务器一键部署脚本
│   └── nginx.conf                  # Nginx 反向代理配置模板
│
├── docs/                           # 文档
│   ├── 第九章_系统设计与实现.md      # 系统设计完整文档（488 行）
│   └── chapter9_figures/           # 架构图（SVG）
│
├── .env.example                    # 环境变量模板
├── requirements.txt                # Python 依赖
├── start_public.sh                 # 一键公网启动脚本（本地开发用）
└── README.md                       # 本文件
```

---

## 功能页面

### 1. 🏠 首页总览 `/dashboard`

- 年度绿色算力综合得分全国概览
- 最高分 / 最低分 / 全国均分统计卡片
- Top 10 省份横向排名条
- 四大区域环形饼图
- 年份选择器（2016—2024）

### 2. 📊 综合评价 `/evaluation`

- 31 省 TOPSIS 综合得分排名表
- 南丁格尔玫瑰图（按区域着色）
- 支持按年份切换

### 3. 🔀 区域差异 `/regional-difference`

- Dagum 基尼系数总体趋势折线图
- 区域内基尼系数堆叠柱状图
- 区域间基尼系数对比柱状图
- 贡献率分解条形图

### 4. 🗺️ 空间聚焦 `/spatial-cluster`

- 中国地图 Choropleth（按得分分级着色）
- Moran's I 全局自相关趋势折线图
- LISA 聚集类型环形饼图（HH / HL / LH / LL）
- 支持点击省份下钻

### 5. 🔄 动态演化 `/dynamic-evolution`

- 传统 Markov 转移概率矩阵（热力矩阵）
- 空间 Markov 转移概率矩阵
- 核密度估计（KDE）分布面积图
- 状态阈值定义表

### 6. 🔍 省域诊断 `/province-diagnosis`

- 省份选择器（默认上海）
- 首要 + 次要障碍维度及障碍度
- 短板诊断类型
- 省级障碍指标排名条
- 历年障碍度演化趋势

### 7. 🏷️ 类型识别 `/type-identification`

- 4 类 LPA 发展类型概要卡片
- 各省份类型归属排名条
- 类型特征详情表
- 类型转移轨迹图

### 8. 💡 SHAP 解释 `/shap`

- 省份 + 年份选择器
- 全局特征重要性排名
- 局部 SHAP 瀑布图（Top 8 特征）
- 年度维度贡献堆叠图
- 模型性能指标（R²、MAE、RMSE）

### 9. 📋 布局决策 `/layout-decision`

- 省域布局适宜度进度条卡片
- 推荐布局类型 + 功能定位
- 优化策略 + 风险预警
- 适用省份选择器

### 10. 💬 智能问答 `/chat`

- 自然语言对话界面（类 ChatGPT）
- 建议问题快捷按钮
- 数据源追溯标签
- 支持问题类型：排名查询、省份诊断、布局建议、趋势预测、模型说明、知识问答

---

## API 接口

### 数据查询接口（13 个 GET 端点）

| 端点 | 参数 | 说明 |
|------|------|------|
| `GET /health` | — | 健康检查 |
| `GET /api/provinces` | — | 所有省份基础信息（含邻接矩阵） |
| `GET /api/scores` | `year` (默认 2024) | 某年 TOPSIS 综合得分 + 排名 |
| `GET /api/province/{province}/profile` | `year` | 省份综合画像（得分 + LPA + 障碍 + 布局） |
| `GET /api/obstacles` | `province` (必填) | 省份障碍度诊断 |
| `GET /api/lpa` | — | LPA 类型分类结果 |
| `GET /api/shap` | `province`, `year` | SHAP 局部解释 Top 8 |
| `GET /api/layout` | `province` | 布局决策推荐 |
| `GET /api/overview` | `year` | 首页总览聚合数据 |
| `GET /api/indicators` | — | 指标体系定义（34 指标） |
| `GET /api/dagum` | — | Dagum 基尼系数分解 |
| `GET /api/moran` | — | Moran's I + LISA 结果 |
| `GET /api/markov` | — | Markov 转移概率矩阵 |

### 智能问答接口（1 个 POST 端点）

| 端点 | 请求体 | 说明 |
|------|--------|------|
| `POST /api/chat` | `{"question": "..."}` | RAG + LLM 智能问答 |

### API 文档

启动后端后访问：
- **Swagger UI**：`http://localhost:8000/docs`
- **ReDoc**：`http://localhost:8000/redoc`

---

## 智能问答模块

智能问答模块是系统的核心亮点之一，采用 **RAG（检索增强生成）** 架构：

```
用户提问
    │
    ▼
┌──────────────┐
│  关键词匹配    │  ← 77 个关键词（31 省份 + 46 领域术语）
│  问题分类      │  ← 6 类：排名 / 诊断 / 布局 / 趋势 / 模型 / 知识
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  RAG 检索     │  ← TF-IDF 向量相似度搜索 10 篇知识文档
│  (Top 3 文档) │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  工具调用     │  ← 10 个数据库查询工具（自动按需调用）
│  (可选)       │     查询得分、排名、障碍、LPA、SHAP、布局等
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  DeepSeek LLM │  ← 系统提示词 + 检索文档 + 工具结果 → 生成回答
│  生成回答     │
└──────────────┘
```

### 10 个数据库工具

`get_latest_scores` · `get_province_score` · `get_province_trend` · `get_top_rankings` · `get_lpa_result` · `get_obstacle_result` · `get_shap_top_features` · `get_layout_recommendation` · `compare_provinces` · `get_future_potential_ranking`（6 因子加权预测）

### 安全策略

- 永不抛出异常（全链路 try-catch，优雅降级）
- LLM 不可用时自动切换离线模式
- 越界问题礼貌引导至系统能力范围
- 速率限制保护

---

## 本地开发

### 前置条件

| 软件 | 最低版本 | 说明 |
|------|----------|------|
| Python | 3.10+ | 后端运行环境 |
| Node.js | 18+ | 前端构建和运行 |
| npm | 9+ | 包管理器 |
| PostgreSQL | 16+ | 数据库（可用本地已有实例） |

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd green-compute-system
```

### 2. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入你的数据库连接信息：

```ini
DATABASE_URL=postgresql+psycopg2://postgres:你的密码@localhost:5432/green_compute
DEEPSEEK_API_KEY=你的DeepSeek_API_Key
```

### 3. 创建数据库并导入数据

```bash
# 创建数据库
createdb green_compute

# 导入表结构
psql -U postgres -d green_compute -f backend/db/schema.sql

# 安装 Python 依赖
pip install -r requirements.txt

# 导入 Excel 数据到 PostgreSQL
python3 backend/importers/import_excel_to_db.py
```

### 4. 构建 RAG 索引（可选，智能问答功能需要）

```bash
python3 backend/rag/build_index.py
```

### 5. 启动后端

```bash
python3 -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

验证：访问 `http://localhost:8000/docs` 查看 Swagger API 文档

### 6. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:3000`

> **提示**：开发模式下，Next.js 会自动将 `/api/*` 请求代理到后端 `http://127.0.0.1:8000`，无需额外配置。

### 7. 一键公网启动（可选，用于临时分享）

```bash
bash start_public.sh
```

此脚本会自动启动后端、构建前端生产版本、启动 Next.js 生产服务器，并通过 ngrok 暴露公网隧道地址。

---

## 服务器部署

### 方式一：手动部署

#### 后端（FastAPI）

```bash
# 使用 systemd 或 supervisor 守护进程
python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

**systemd 示例**（`/etc/systemd/system/green-compute-api.service`）：

```ini
[Unit]
Description=Green Compute System API
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/green-compute-system
ExecStart=/usr/bin/python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now green-compute-api
```

#### 前端（Next.js Standalone）

```bash
cd frontend
npm install
npm run build
# 生产模式启动，使用 standalone 输出
node .next/standalone/server.js
```

**systemd 示例**（`/etc/systemd/system/green-compute-web.service`）：

```ini
[Unit]
Description=Green Compute System Web
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/green-compute-system/frontend
ExecStart=/usr/bin/node .next/standalone/server.js
Environment=PORT=3000
Environment=HOSTNAME=127.0.0.1
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

#### Nginx 反向代理

参考 `deploy/nginx.conf`，将域名指向 3000 端口，API 路径透传至 8000 端口。

### 方式二：Docker 部署（推荐）

待补充。

---

## 宝塔面板部署

如果你使用**宝塔面板**管理服务器，请按以下步骤操作：

### 第 1 步：上传文件

将 `green-compute-system/` 整个目录上传到服务器（例如 `/www/wwwroot/green-compute-system/`）。

### 第 2 步：配置环境变量

```bash
cd /www/wwwroot/green-compute-system
cp .env.example .env
nano .env  # 修改数据库密码和 API Key
```

### 第 3 步：创建数据库

宝塔面板 → **数据库** → **添加数据库**：
- 数据库名：`green_compute`
- 用户名：`postgres`（或自定义）
- 密码：与 `.env` 中一致

### 第 4 步：运行部署脚本

在宝塔终端中执行：

```bash
cd /www/wwwroot/green-compute-system
bash deploy/setup.sh
```

此脚本自动完成：检查配置 → 创建表结构 → 导入数据 → 安装依赖 → 构建前端。

### 第 5 步：添加进程守护

**后端** — 宝塔 → 网站 → Python 项目 → 添加：

| 配置项 | 值 |
|--------|-----|
| 启动命令 | `python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` |
| 项目目录 | `/www/wwwroot/green-compute-system` |
| 端口 | `8000` |

**前端** — 宝塔 → 网站 → Node.js 项目 → 添加：

| 配置项 | 值 |
|--------|-----|
| 启动命令 | `node .next/standalone/server.js` |
| 项目目录 | `/www/wwwroot/green-compute-system/frontend` |
| 端口 | `3000` |

### 第 6 步：配置 Nginx

宝塔 → 网站 → 你的站点 → 配置文件，将 `deploy/nginx.conf` 的内容粘贴进去，修改 `server_name` 为你的域名或 IP。

### 第 7 步：验证

访问 `http://你的域名`，确认页面正常加载，API 数据正常返回。

---

## 数据库设计

系统数据库共包含 **42 张表**，按业务领域分为 8 个类别：

| 类别 | 表数量 | 核心表 |
|------|--------|--------|
| 基础信息 | 3 | `province_basic`, `adjacency_matrix`, `indicator_system` |
| 核心数据 | 4 | `indicator_values`, `indicator_values_normalized`, `indicator_weights`, `topsis_scores` |
| LPA 分析 | 4 | `lpa_province_assignment`, `lpa_type_summary`, `lpa_model_fit`, `lpa_type_trajectory` |
| 空间演化 | 10 | `dagum_decomposition`, `dagum_intra_region`, `dagum_inter_region`, `moran_results`, `lisa_results`, `markov_probability`, `markov_frequency`, `spatial_markov`, `state_thresholds`, `spatial_lag_state`, `kde_statistics` |
| 障碍度诊断 | 7 | `obstacle_national`, `obstacle_regional`, `obstacle_lpa`, `obstacle_province`, `obstacle_indicator`, `obstacle_annual_evolution`, `obstacle_province_indicator_detail` |
| SHAP 解释 | 7 | `shap_model_metrics`, `shap_predictions`, `shap_importance`, `shap_annual_dimension_contribution`, `shap_lpa_dimension_contribution`, `shap_province_summary`, `shap_local_top8` |
| 布局决策 | 7 | `layout_province_decision`, `layout_type_summary`, `layout_type_features`, `layout_lpa_matrix`, `layout_strategy_library`, `layout_strategy_priority` |
| 指标体系 | 1 | `indicator_system`（34 个二级指标 × 8 个一级维度） |

### 数据流向

```
Excel 文件 (data/raw/*.xlsx)
    │
    ▼
import_excel_to_db.py
（字段映射 · 类型转换 · 省份标准化 · 完整性校验）
    │
    ▼
PostgreSQL 42 张表
    │
    ▼
SQLAlchemy ORM → Service Layer → API Routes → JSON Response
```

### 指标体系概要

| 一级维度 | 二级指标数 | 示例指标 |
|----------|-----------|----------|
| 算力需求基础 | 4 | GDP、常住人口、能源消费总量、CO₂排放量 |
| 能源供给能力 | 3 | 发电装机容量、可再生能源消纳比重、全社会用电量 |
| 数字基础设施 | 5 | 光缆线路长度、5G基站数、接入端口数、移动电话普及率 |
| 绿色低碳约束 | 3 | 单位GDP能耗、碳排放强度、工业固废综合利用率 |
| 创新与人才支撑 | 5 | R&D经费强度、发明专利数、IT从业人员占比、劳动生产率 |
| 气候与自然条件 | 3 | 年平均气温、人均水资源量 |
| 区域协同能力 | 3 | IT服务业增加值占比、电信业务强度、高技术产业投资强度 |
| 算力产出效益 | 8 | 互联网宽带用户数、移动互联网普及率等 |

> 完整指标体系及权重参见 `data/raw/表2-1_指标体系.xlsx`

---

## 常见问题

<details>
<summary><b>Q: 网页打开显示 404？</b></summary>

检查三点：
1. **后端是否启动**：`curl http://127.0.0.1:8000/health` 应返回 `{"status":"ok"}`
2. **前端是否启动**：`curl http://127.0.0.1:3000` 应返回 HTML
3. **Nginx 配置是否正确**：检查反向代理规则是否将 `/` 指向 3000 端口，`/api/` 指向 8000 端口
</details>

<details>
<summary><b>Q: 页面加载但数据为空？</b></summary>

1. 确认数据库已导入：连接数据库，执行 `SELECT count(*) FROM topsis_scores;` 应有数据
2. 确认 `.env` 中 `DATABASE_URL` 配置正确
3. 查看后端日志：`uvicorn` 终端输出中是否有数据库连接错误
</details>

<details>
<summary><b>Q: 智能问答不可用？</b></summary>

需要：
1. `.env` 中配置有效的 `DEEPSEEK_API_KEY`
2. RAG 索引已构建：`python3 backend/rag/build_index.py`
3. 确保 `data/vector_store/` 目录存在且包含索引文件
</details>

<details>
<summary><b>Q: PostgreSQL 连接不上？</b></summary>

```bash
# 检查 PostgreSQL 是否运行
pg_isready

# 检查端口
netstat -tlnp | grep 5432

# 测试连接
psql -U postgres -h 127.0.0.1 -d green_compute -c "SELECT 1"
```
</details>

<details>
<summary><b>Q: npm install 失败？</b></summary>

```bash
# 清除缓存重试
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```
</details>

<details>
<summary><b>Q: 如何更新数据？</b></summary>

1. 将新的 Excel 文件放入 `data/raw/`
2. 更新 `backend/importers/data_import_config.yaml` 中的字段映射
3. 重新运行导入：`python3 backend/importers/import_excel_to_db.py`
4. 重新构建 RAG 索引（如果知识文档有变化）
</details>

---

## License

本项目仅用于学术研究和教育目的。数据来源包括国家统计局、中国能源统计年鉴、中国科技统计年鉴和中国信息产业年鉴等公开统计资料。

---

<p align="center">
  <sub>Built with ❤️ using FastAPI · Next.js · PostgreSQL · ECharts · DeepSeek</sub>
</p>
