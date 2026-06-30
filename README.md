# 🌿 省域绿色算力承载能力评估与资源布局决策支持系统

> Green Computing Resource Carrying Capacity Assessment & Layout Decision Support System

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-15-black.svg)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB.svg)](https://react.dev/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791.svg)](https://www.postgresql.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6-3178C6.svg)](https://www.typescriptlang.org/)
[![ECharts](https://img.shields.io/badge/ECharts-5.5-AA344D.svg)](https://echarts.apache.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-06B6D4.svg)](https://tailwindcss.com/)

---

## ⚠️ 重要说明：隐私与安全

本项目涉及以下敏感配置信息，**出于安全考虑，已从代码仓库中移除，不予公开**：

| 敏感信息 | 说明 |
|----------|------|
| **PostgreSQL 数据库密码** | 用于连接生产环境数据库，包含 42 张业务表的读写权限 |
| **DeepSeek API Key** | 用于智能问答模块的大语言模型调用，涉及 API 额度与计费 |

> 📧 **如需部署或运行本项目，请联系作者获取数据库密码及 API Key。**
>
> 联系时请说明使用场景（学术研究 / 教学演示 / 其他），作者将根据情况提供相应的访问凭据。

项目中的 `.env.example` 为配置模板文件，仅包含字段名和格式说明，**不含真实密码**。部署时请将其复制为 `.env` 并填入从作者处获取的真实凭据。

---

## 📖 目录

- [隐私与安全](#️-重要说明隐私与安全)
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

系统面向四类用户提供全链条决策支持服务：

| 用户类型 | 核心需求 |
|----------|----------|
| 🏛️ 政府部门 | 掌握各省绿色算力发展水平，制定区域差异化政策 |
| 🏢 数据中心企业 | 评估算力基础设施布局选址适宜度与投资优先级 |
| ⚡ 能源规划机构 | 分析能源供给结构与碳排放约束对算力布局的影响 |
| 🎓 研究人员 | 查询模型计算结果、对比分析方法差异、复现研究结论 |

---

## 核心功能

### 📊 数据驾驶舱（10 个功能页面）

- **首页总览** — 全国宏观概览、Top 排名、四大区域分布统计
- **综合评价** — TOPSIS 综合得分排名、南丁格尔玫瑰图
- **区域差异** — Dagum 基尼系数分解（区域内 + 区域间 + 超变密度贡献率）
- **空间聚焦** — 中国地图 Choropleth + Moran's I 全局自相关 + LISA 局部聚集分析
- **动态演化** — Markov 转移概率矩阵 + 传统/空间 Markov 对比 + 核密度估计
- **省域诊断** — 障碍度诊断（首要/次要障碍维度、短板类型识别）
- **类型识别** — LPA 潜在剖面分析（4 类发展类型 + 动态转移轨迹）
- **SHAP 解释** — 全局特征重要性 + 局部瀑布图 + 年度维度贡献分解
- **布局决策** — 省域布局推荐（优势指数、功能定位、优化策略、风险预警）
- **智能问答** — 自然语言查询，RAG + DeepSeek 大模型

### 🤖 智能问答

- **RAG 检索增强生成**：TF-IDF 向量化 + 10 篇专业知识文档
- **问题自动分类**：6 类路由（排名查询、省份诊断、布局建议、趋势预测、模型说明、知识问答）
- **10 个数据库工具**：自动调用数据库查询获取实时数据，确保回答准确可追溯
- **离线降级策略**：LLM 不可用时自动切换离线模式，保障服务可用性

### 📈 可视化能力

支持 **10 余种** ECharts 高级图表类型，统一采用深色科技风主题：

| 图表 | 用途 |
|------|------|
| 🗺️ 中国地图 Choropleth | 省级得分空间分布可视化 |
| 🌹 南丁格尔玫瑰图 | 指标雷达对比分析 |
| 🍩 环形饼图 | 四大区域占比分析 |
| 📊 横向排名条 | 31 省得分直观排序 |
| 📈 折线图 / 面积图 | 时间序列趋势变化 |
| 📉 堆叠柱状图 | 维度分解与结构分析 |
| 🌊 SHAP 瀑布图 | 特征贡献方向与大小解释 |
| 🔥 热力矩阵 | 状态转移概率可视化 |

---

## 技术栈

### 后端

| 技术 | 版本 | 用途 |
|------|------|------|
| [Python](https://www.python.org/) | 3.10+ | 后端编程语言 |
| [FastAPI](https://fastapi.tiangolo.com/) | ≥ 0.110 | 异步 Web 框架，自动生成 Swagger / ReDoc 交互式文档 |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ≥ 2.0 | ORM 数据库访问层，连接池管理 |
| [PostgreSQL](https://www.postgresql.org/) | 18 | 关系型数据库，存储全部 42 张业务表 |
| [Pydantic](https://docs.pydantic.dev/) | ≥ 2.0 | 请求参数校验与响应数据序列化 |
| [Uvicorn](https://www.uvicorn.org/) | ≥ 0.27 | ASGI 高性能服务器 |
| [scikit-learn](https://scikit-learn.org/) | ≥ 1.3 | TF-IDF 文本向量化（RAG 检索模块） |
| [pandas](https://pandas.pydata.org/) | ≥ 2.0 | 数据处理与 Excel 读取 |
| [openpyxl](https://openpyxl.readthedocs.io/) | ≥ 3.1 | Excel 文件解析引擎 |
| [DeepSeek Chat API](https://platform.deepseek.com/) | — | 大语言模型（智能问答） |

### 前端

| 技术 | 版本 | 用途 |
|------|------|------|
| [Next.js](https://nextjs.org/) | ^15.0 | React 全栈框架，App Router 路由模式 |
| [React](https://react.dev/) | ^19.0 | UI 组件库 |
| [TypeScript](https://www.typescriptlang.org/) | ^5.6 | 类型安全开发 |
| [Tailwind CSS](https://tailwindcss.com/) | ^3.4 | 实用优先 CSS 框架，深色科技风响应式主题 |
| [ECharts](https://echarts.apache.org/) | ^5.5 | 数据可视化图表库 |
| [echarts-for-react](https://github.com/hustcc/echarts-for-react) | ^3.0 | React 环境下的 ECharts 封装 |

---

## 系统架构

```
                            ┌──────────────────────────┐
                            │       用户浏览器            │
                            │  http://your-domain.com   │
                            └───────────┬──────────────┘
                                        │
                                        ▼
                            ┌──────────────────────────┐
                            │     Nginx（反向代理）       │
                            │  / → :3000   /api/* → :8000│
                            └─────────┬──────────┬─────┘
                                      │          │
                         ┌────────────┘          └────────────┐
                         ▼                                    ▼
              ┌──────────────────┐              ┌──────────────────────────┐
              │  Next.js 前端     │              │   FastAPI 后端 (:8000)    │
              │  (端口 3000)      │              │                          │
              │                  │              │  API Routes (14 端点)     │
              │  • 10 个页面      │              │  Service Layer (11 模块)  │
              │  • ECharts 图表   │              │  SQLAlchemy ORM (23 模型) │
              │  • Dark Theme     │              │  Agent / RAG 智能问答     │
              └──────────────────┘              └────────────┬─────────────┘
                                                             │
                                                             ▼
                                              ┌──────────────────────────┐
                                              │   PostgreSQL 数据库       │
                                              │   42 张表 · 8 大类别     │
                                              │   31 省 × 9 年 × 34 指标  │
                                              └──────────────────────────┘
```

系统遵循"**数据资源层 → 数据存储层 → 后端服务层 → 前端展示层 → 应用交互层**"五层架构设计，各层通过标准化 RESTful API 和 Pydantic 数据模型实现松耦合协作。

---

## 项目结构

```
green-compute-system/
│
├── backend/                        # FastAPI 后端源码
│   ├── app/                        # 应用核心
│   │   ├── main.py                 #   入口：FastAPI 实例化、CORS、路由注册
│   │   ├── database.py             #   SQLAlchemy 引擎 + 连接池（pool_size=5）
│   │   ├── models.py               #   23 个 ORM 数据模型
│   │   ├── schemas.py              #   30 个 Pydantic 响应模型
│   │   ├── api/
│   │   │   └── routes.py           #   14 个 RESTful API 端点
│   │   └── services/               #   11 个业务服务模块
│   │       ├── province.py         #     省份基础信息服务
│   │       ├── score.py            #     TOPSIS 综合得分服务
│   │       ├── overview.py         #     首页聚合数据服务
│   │       ├── obstacle.py         #     障碍度诊断服务
│   │       ├── lpa.py              #     LPA 类型分析服务
│   │       ├── shap.py             #     SHAP 可解释性服务
│   │       ├── layout.py           #     布局决策服务
│   │       ├── indicator.py        #     指标体系查询服务
│   │       ├── dagum.py            #     Dagum 基尼系数分解服务
│   │       ├── moran.py            #     Moran's I 空间自相关服务
│   │       └── markov.py           #     Markov 转移矩阵服务
│   │
│   ├── agent/                      # 🤖 智能问答模块
│   │   ├── router.py               #   POST /api/chat 端点
│   │   ├── chat_service.py         #   对话编排（分类 → 检索 → 工具调用 → 生成）
│   │   ├── tools.py                #   10 个数据库查询工具函数
│   │   ├── prompts.py              #   LLM 系统提示词模板库
│   │   └── rate_limit.py           #   频率限制中间件
│   │
│   ├── db/
│   │   ├── database.py             # 导入器专用数据库连接
│   │   └── schema.sql              # 42 张表完整建表语句（可直接执行）
│   │
│   ├── importers/
│   │   ├── import_excel_to_db.py   # Excel → PostgreSQL 数据导入管道
│   │   ├── inspect_excel_files.py  # Excel 文件结构扫描工具
│   │   └── data_import_config.yaml # 10 个 Excel → 42 张表的字段映射配置
│   │
│   └── rag/
│       ├── build_index.py          # TF-IDF 向量索引构建脚本
│       ├── retriever.py            # 知识库文档检索器
│       └── rag_docs/               # 10 篇 RAG 专业知识文档
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
├── frontend/                       # Next.js 15 前端源码
│   ├── public/
│   │   └── china.json              # 中国省级行政区划 GeoJSON 数据
│   ├── src/
│   │   ├── app/                    # App Router 路由页面
│   │   │   ├── page.tsx            #   / → 自动重定向到 /dashboard
│   │   │   ├── layout.tsx          #   全局布局：侧边栏 + 顶栏 + 内容区
│   │   │   ├── dashboard/          #   🏠 首页总览
│   │   │   ├── evaluation/         #   📊 综合评价（TOPSIS 排名）
│   │   │   ├── regional-difference/#   🔀 区域差异（Dagum 分解）
│   │   │   ├── spatial-cluster/    #   🗺️ 空间聚焦（Moran + LISA）
│   │   │   ├── dynamic-evolution/  #   🔄 动态演化（Markov 转移）
│   │   │   ├── province-diagnosis/ #   🔍 省域诊断（障碍度）
│   │   │   ├── type-identification/#   🏷️ 类型识别（LPA 分类）
│   │   │   ├── shap/               #   💡 SHAP 解释（特征重要性）
│   │   │   ├── layout-decision/    #   📋 布局决策（优化建议）
│   │   │   └── chat/               #   💬 智能问答（RAG + LLM）
│   │   ├── components/
│   │   │   ├── charts/             # 10 个可复用 ECharts 图表组件
│   │   │   │   ├── ChinaMap.tsx     #     中国地图 Choropleth
│   │   │   │   ├── DonutChart.tsx   #     环形饼图
│   │   │   │   ├── RoseChart.tsx    #     南丁格尔玫瑰图
│   │   │   │   ├── RankingBar.tsx   #     横向排名条
│   │   │   │   ├── LineChart.tsx    #     折线图
│   │   │   │   ├── AreaChart.tsx    #     面积图
│   │   │   │   ├── StackedBar.tsx   #     堆叠柱状图
│   │   │   │   ├── BarChart.tsx     #     柱状图
│   │   │   │   ├── ShapWaterfall.tsx#     SHAP 瀑布图
│   │   │   │   └── RegionChart.tsx  #     区域柱状图
│   │   │   ├── chat/               # 聊天 UI 组件
│   │   │   ├── Sidebar.tsx         # 224px 导航侧边栏（四级分组）
│   │   │   ├── Header.tsx          # 56px 顶部状态栏
│   │   │   └── ...
│   │   └── lib/
│   │       └── api.ts              # 类型化 API 客户端（12 数据 + 1 聊天）
│   ├── next.config.js              # standalone 输出 + API 代理 rewrite
│   ├── tailwind.config.js          # 深色科技风主题色板
│   ├── tsconfig.json
│   └── package.json
│
├── data/                           # 数据文件
│   ├── raw/                        # 11 个 Excel 源数据文件
│   │   ├── clean_data.xlsx         #   清洗后面板数据（31省×9年×34指标）
│   │   ├── 表2-1_指标体系.xlsx      #   34 个二级指标定义
│   │   ├── 表3-1_标准化数据.xlsx    #   极差标准化结果
│   │   ├── 表3-2_组合权重结果.xlsx  #   熵权法 + CRITIC 组合权重
│   │   ├── 表3-3_绿色算力综合得分(1).xlsx  # TOPSIS 综合得分
│   │   ├── 第1章_数据治理报告(1).xlsx
│   │   ├── 第4章_LPA结果表(1).xlsx
│   │   ├── 第5章_空间演化分析结果表(1).xlsx
│   │   ├── 第6章_障碍度模型结果表(1).xlsx
│   │   ├── 第7章_SHAP解释分析结果表(1).xlsx
│   │   └── 第8章_布局决策结果表.xlsx
│   ├── metadata/
│   │   └── data_dictionary.xlsx    # 数据字典（字段说明）
│   └── vector_store/               # 持久化 TF-IDF 向量索引
│
├── deploy/                         # 🚀 部署配置
│   ├── setup.sh                    #   服务器一键部署脚本
│   └── nginx.conf                  #   Nginx 反向代理配置模板
│
├── docs/                           # 文档
│   ├── 第九章_系统设计与实现.md      #   系统设计技术文档（~500 行）
│   └── chapter9_figures/           #   系统架构 SVG 图
│
├── .env.example                    # 环境变量模板（不含真实密码）
├── requirements.txt                # Python 依赖清单
├── start_public.sh                 # 一键公网启动脚本（本地 ngrok 隧道）
└── README.md                       # 本文件
```

---

## 功能页面

### 1. 🏠 首页总览 `/dashboard`

全国绿色算力发展水平宏观概览。展示年度最高/最低/均分统计卡片、Top 10 省份横向排名条、四大区域得分环形饼图，支持年份切换（2016—2024）。

### 2. 📊 综合评价 `/evaluation`

31 省份 TOPSIS 综合得分完整排名。采用南丁格尔玫瑰图按区域分组着色展示，辅以得分排序表格，支持按年份独立查看。

### 3. 🔀 区域差异 `/regional-difference`

Dagum 基尼系数四维分解。包含总体基尼系数趋势折线图、四大区域内差异堆叠柱状图、区域间差异对比和贡献率分解（区域内 / 区域间 / 超变密度）。

### 4. 🗺️ 空间聚焦 `/spatial-cluster`

空间自相关与局部聚集模式分析。中国地图按综合得分四级着色，Moran's I 逐年趋势折线图，LISA 聚集类型（HH / HL / LH / LL）环形图。支持点击省份查看该省空间邻接状态。

### 5. 🔄 动态演化 `/dynamic-evolution`

Markov 链动态转移分析。传统 Markov 与空间 Markov 转移概率矩阵热力图对比，核密度估计（KDE）分布面积图，状态阈值定义及空间滞后状态说明。

### 6. 🔍 省域诊断 `/province-diagnosis`

单省份障碍度深度诊断。省份选择器 + 首要/次要障碍维度及其障碍度 + 短板诊断类型标签 + 障碍指标排名条 + 历年障碍度演化趋势折线图。

### 7. 🏷️ 类型识别 `/type-identification`

LPA 潜在剖面分析结果展示。4 类发展类型概要卡片（含省份数、核心特征描述），各省份 LPA 类型归属排名条，类型特征详情表，类型间转移轨迹图。

### 8. 💡 SHAP 解释 `/shap`

机器学习模型可解释性分析。省份 + 年份联合选择器，全局特征重要性排名条，局部 SHAP 瀑布图（Top 8 特征，红蓝区分正负贡献方向），年度维度贡献堆叠图，模型性能指标（R² / MAE / RMSE）。

### 9. 📋 布局决策 `/layout-decision`

省域算力资源布局智能推荐。包括布局适宜度进度条卡片（优势指数）、推荐布局类型 + 功能定位 + 优化策略 + 风险预警，支持省份切换查询。

### 10. 💬 智能问答 `/chat`

基于 RAG 的自然语言智能问答。对话界面带建议问题快捷按钮，系统自动进行问题分类、知识库检索、数据库工具调用和 LLM 生成回答，回答附带数据来源追溯标签。

---

## API 接口

### 数据查询（13 个 GET 端点）

| 端点 | 参数 | 说明 |
|------|------|------|
| `GET /health` | — | 服务健康检查，返回 `{"status":"ok"}` |
| `GET /api/provinces` | — | 全部 31 省基础信息（含区域、枢纽状态、邻接关系） |
| `GET /api/scores` | `year`（默认 2024） | 某年度 TOPSIS 综合得分与排名（升序） |
| `GET /api/province/{province}/profile` | `year` | 省份综合画像：得分 + LPA 类型 + 障碍诊断 + 布局建议 |
| `GET /api/obstacles` | `province`（必填） | 省份障碍度完整诊断报告 |
| `GET /api/lpa` | — | 全部省份 LPA 发展类型分类 |
| `GET /api/shap` | `province`, `year` | 局部 SHAP 特征贡献值 Top 8 |
| `GET /api/layout` | `province` | 省份布局决策推荐详情 |
| `GET /api/overview` | `year` | 首页总览聚合数据（均分、极值、排名） |
| `GET /api/indicators` | — | 34 个二级指标完整定义 |
| `GET /api/dagum` | — | Dagum 基尼系数分解（总体 + 区域内 + 区域间） |
| `GET /api/moran` | — | Moran's I 全局自相关 + LISA 局部聚集结果 |
| `GET /api/markov` | — | Markov 转移概率矩阵（传统 + 空间） |

### 智能问答（1 个 POST 端点）

| 端点 | 请求体 | 说明 |
|------|--------|------|
| `POST /api/chat` | `{"question": "上海2024年的绿色算力得分排名是多少？"}` | RAG + DeepSeek LLM 智能问答 |

### 交互式 API 文档

启动后端后，浏览器访问：

- **Swagger UI**（可交互调试）：`http://localhost:8000/docs`
- **ReDoc**（结构化文档）：`http://localhost:8000/redoc`

---

## 智能问答模块

系统集成的智能问答模块采用 **RAG（Retrieval-Augmented Generation，检索增强生成）** 架构，确保回答既具备大语言模型的语义理解能力，又能准确引用数据库中存储的实际分析结果。

### 处理流程

```
用户提问："上海2024年的绿色算力得分排名？"
    │
    ▼
┌─────────────────┐
│  关键词匹配       │  ← 77 个关键词库（31 省份名 + 46 领域术语）
│  问题分类         │  ← 排名查询 / 省份诊断 / 布局建议 / 趋势预测 / 模型说明 / 知识问答
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  RAG 知识库检索   │  ← TF-IDF 向量相似度匹配 Top 3 专业知识文档
│  (10 篇 Markdown) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  数据库工具调用   │  ← 自动判定需要哪些工具并执行（得分查询 / 排名 / 障碍 / SHAP 等）
│  (10 个工具函数)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DeepSeek LLM   │  ← 系统提示词 + 检索文档片段 + 数据库查询结果
│  生成结构回答    │  → 返回：得分数据 + 排名 + 趋势分析 + 数据来源标注
└─────────────────┘
```

### 内置工具函数

`get_latest_scores` · `get_province_score` · `get_province_trend` · `get_top_rankings` · `get_lpa_result` · `get_obstacle_result` · `get_shap_top_features` · `get_layout_recommendation` · `compare_provinces` · `get_future_potential_ranking`（基于 6 因子加权预测模型）

### 安全与容错

- **全链路异常捕获**：永不向用户暴露原始错误信息
- **LLM 离线降级**：API 不可用时自动切换为规则匹配模式
- **越界问题引导**：对超出系统能力范围的问题，礼貌引导至可用功能
- **速率限制**：防止 API 滥用和过度消耗

---

## 本地开发

### 前置条件

| 软件 | 最低版本 | 检查命令 |
|------|----------|----------|
| Python | 3.10+ | `python3 --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| PostgreSQL | 16+ | `psql --version` |

### 1. 获取凭据

> 📧 **联系作者获取数据库密码与 API Key**，这是运行项目的必要前提。

### 2. 克隆项目

```bash
git clone <your-repo-url>
cd green-compute-system
```

### 3. 配置环境变量

```bash
cp .env.example .env
```

编辑 `.env`，填入从作者处获取的凭据：

```ini
DATABASE_URL=postgresql+psycopg2://postgres:从作者获取的密码@localhost:5432/green_compute
DEEPSEEK_API_KEY=从作者获取的API_Key
```

### 4. 初始化数据库

```bash
# 创建数据库
createdb green_compute

# 导入 42 张表的建表语句
psql -U postgres -d green_compute -f backend/db/schema.sql

# 安装 Python 依赖
pip install -r requirements.txt

# 将 Excel 数据导入 PostgreSQL
python3 backend/importers/import_excel_to_db.py
```

### 5. 构建 RAG 索引（智能问答功能需要）

```bash
python3 backend/rag/build_index.py
```

完成后确认 `data/vector_store/` 目录下存在索引文件。

### 6. 启动后端

```bash
python3 -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

访问 `http://localhost:8000/docs` 验证 Swagger 文档正常加载，尝试调用 `/api/scores?year=2024` 确认有数据返回。

### 7. 启动前端

```bash
cd frontend
npm install
npm run dev
```

访问 `http://localhost:3000`，首页应自动跳转至 `/dashboard` 并加载数据。

### 8. 公网临时分享（可选）

如果你需要将本地服务临时暴露到公网供他人预览：

```bash
bash start_public.sh
```

此脚本会自动启动后端（崩溃重启守护）、构建前端生产版本、启动 Next.js 生产服务器，并通过 ngrok 创建公网隧道，终端将打印可访问的公网 URL。

---

## 服务器部署

### 后端（FastAPI）— systemd 守护

创建 `/etc/systemd/system/green-compute-api.service`：

```ini
[Unit]
Description=Green Compute System API
After=network.target postgresql.service

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
sudo systemctl daemon-reload
sudo systemctl enable --now green-compute-api
```

### 前端（Next.js Standalone）— systemd 守护

创建 `/etc/systemd/system/green-compute-web.service`：

```ini
[Unit]
Description=Green Compute System Web
After=network.target green-compute-api.service

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

```bash
sudo systemctl enable --now green-compute-web
```

### Nginx 反向代理

参考 `deploy/nginx.conf` 模板，核心规则：
- `/` → `http://127.0.0.1:3000`（前端页面）
- `/api/*` → `http://127.0.0.1:8000/api/*`（后端 API）
- `/_next/static/*` → `http://127.0.0.1:3000` + 30 天强缓存

---

## 宝塔面板部署

如果你使用**宝塔面板**管理服务器，完整操作流程如下：

### 第 1 步：上传文件

将 `green-compute-system/` 整个目录上传至服务器（例如 `/www/wwwroot/green-compute-system/`）。

### 第 2 步：配置环境变量

```bash
cd /www/wwwroot/green-compute-system
cp .env.example .env
nano .env  # 填入从作者处获取的数据库密码和 API Key
```

### 第 3 步：创建数据库

宝塔面板 → **数据库** → **添加数据库**：

- 数据库名：`green_compute`
- 用户名：`postgres`（或自定义）
- 密码：与 `.env` 中一致

### 第 4 步：运行一键部署脚本

在宝塔终端中执行：

```bash
cd /www/wwwroot/green-compute-system
bash deploy/setup.sh
```

脚本自动完成：环境检查 → 表结构创建 → 数据导入 → Python 依赖安装 → 前端构建。

### 第 5 步：添加进程守护

**Python 后端** — 宝塔 → 网站 → Python 项目 → 添加项目：

| 配置项 | 值 |
|--------|-----|
| 启动命令 | `python3 -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` |
| 项目目录 | `/www/wwwroot/green-compute-system` |
| 端口 | `8000` |

**Node 前端** — 宝塔 → 网站 → Node.js 项目 → 添加项目：

| 配置项 | 值 |
|--------|-----|
| 启动命令 | `node .next/standalone/server.js` |
| 项目目录 | `/www/wwwroot/green-compute-system/frontend` |
| 端口 | `3000` |

### 第 6 步：配置 Nginx

宝塔 → 网站 → 你的站点 → **配置文件**，将 `deploy/nginx.conf` 的内容粘贴替换（记得修改 `server_name` 为你的实际域名或 IP）。

### 第 7 步：验证部署

在浏览器访问你的域名或 IP，确认：

1. 首页自动跳转到 `/dashboard` 且数据正常加载
2. 导航侧边栏的 10 个页面均能正常访问
3. API 文档页 `/docs` 可以打开

---

## 数据库设计

系统数据库共包含 **42 张业务表**，按业务领域分为 8 大类别，所有表通过"省份名称 + 年份"字段关联。

### 表分类总览

| 类别 | 表数量 | 核心表举例 |
|------|--------|-----------|
| 基础信息 | 3 | `province_basic`（省份信息）, `adjacency_matrix`（邻接矩阵）, `indicator_system`（34 个指标定义） |
| 核心数据 | 4 | `indicator_values`（原始值）, `indicator_values_normalized`（标准化值）, `indicator_weights`（组合权重）, `topsis_scores`（综合得分） |
| LPA 分析 | 4 | `lpa_province_assignment`（省份类型归属）, `lpa_type_summary`（类型概要）, `lpa_model_fit`（模型拟合指标）, `lpa_type_trajectory`（类型转移轨迹） |
| 空间演化 | 10 | `dagum_decomposition`, `dagum_intra_region`, `dagum_inter_region`, `moran_results`, `lisa_results`, `markov_probability`, `markov_frequency`, `spatial_markov`, `state_thresholds`, `spatial_lag_state`, `kde_statistics` |
| 障碍度诊断 | 7 | `obstacle_national`, `obstacle_regional`, `obstacle_lpa`, `obstacle_province`, `obstacle_indicator`, `obstacle_annual_evolution`, `obstacle_province_indicator_detail` |
| SHAP 解释 | 7 | `shap_model_metrics`, `shap_predictions`, `shap_importance`, `shap_annual_dimension_contribution`, `shap_lpa_dimension_contribution`, `shap_province_summary`, `shap_local_top8` |
| 布局决策 | 7 | `layout_province_decision`, `layout_type_summary`, `layout_type_features`, `layout_lpa_matrix`, `layout_strategy_library`, `layout_strategy_priority` |

### 数据流向

```
data/raw/*.xlsx                    ← 11 个 Excel 源数据文件
       │
       ▼
backend/importers/import_excel_to_db.py
       │  字段映射 · 类型转换 · 省份名标准化 · 区域自动补充 · 完整性校验
       ▼
PostgreSQL (green_compute)         ← 42 张结构化业务表
       │
       ▼
SQLAlchemy ORM (23 个模型)         ← 对象关系映射
       │
       ▼
Service Layer (11 个服务模块)       ← 业务逻辑封装
       │
       ▼
API Routes (14 个端点)             ← RESTful JSON 响应
```

### 指标体系概要

| 一级维度 | 指标数 | 示例指标 |
|----------|--------|----------|
| 算力需求基础 | 4 | GDP（亿元）、常住人口（万人）、能源消费总量、CO₂排放量 |
| 能源供给能力 | 3 | 每万人发电装机容量、可再生能源消纳比重、全社会用电量 |
| 数字基础设施 | 5 | 每万人光缆线路长度、每万人5G基站数、每万人接入端口数、移动电话普及率、互联网宽带用户数 |
| 绿色低碳约束 | 3 | 单位GDP能耗、碳排放强度、工业固废综合利用率 |
| 创新与人才支撑 | 5 | R&D经费投入强度、万人发明专利数、IT从业人员占比、劳动生产率、科技支出占比 |
| 气候与自然条件 | 3 | 年平均气温、人均水资源量 |
| 区域协同能力 | 3 | IT服务业增加值占比、电信业务强度、高技术产业投资强度 |
| 算力产出效益 | 8 | 移动互联网普及率、每万人互联网宽带用户数等 |

> 完整指标体系（含编码、权重、方向、单位）参见 `data/raw/表2-1_指标体系.xlsx`

---

## 常见问题

<details>
<summary><b>Q: 打开网页显示 404？</b></summary>

三步排查法：
1. `curl http://127.0.0.1:8000/health` — 确认后端运行，返回 `{"status":"ok"}`
2. `curl -o /dev/null -w "%{http_code}" http://127.0.0.1:3000` — 确认前端运行，返回 `200`
3. 检查 Nginx 配置中 `proxy_pass` 端口是否与上述一致

常见原因是只启动了前端而忘记启动后端，Nginx 把 `/api/*` 代理到 8000 端口时连接被拒，页面 JS 加载后 API 请求全部失败导致显示空白或错误。
</details>

<details>
<summary><b>Q: 页面能打开，但数据为空或一直显示 Loading？</b></summary>

1. 数据库是否已导入数据：`psql -U postgres -d green_compute -c "SELECT count(*) FROM topsis_scores;"`
2. `.env` 中 `DATABASE_URL` 密码是否正确
3. 后端终端日志是否有数据库连接错误（如 `Connection refused`）
4. PostgreSQL 服务是否运行：`pg_isready`
</details>

<details>
<summary><b>Q: 智能问答功能不可用？</b></summary>

需满足三个条件：
1. `.env` 中已配置有效的 `DEEPSEEK_API_KEY`
2. 已构建 RAG 索引（`python3 backend/rag/build_index.py`）
3. `data/vector_store/` 目录存在且包含 `.pkl` 索引文件
</details>

<details>
<summary><b>Q: 如何在新服务器上重建数据库？</b></summary>

```bash
# 1. 建库 + 建表
createdb green_compute
psql -U postgres -d green_compute -f backend/db/schema.sql

# 2. 导入数据
pip install -r requirements.txt
python3 backend/importers/import_excel_to_db.py

# 3. 重建 RAG 索引
python3 backend/rag/build_index.py
```
</details>

<details>
<summary><b>Q: npm install 失败或 npm run build 报错？</b></summary>

```bash
# 清除缓存
rm -rf node_modules package-lock.json .next
npm cache clean --force

# 重新安装
npm install
npm run build
```
</details>

<details>
<summary><b>Q: 如何更新分析数据？</b></summary>

1. 将新的 Excel 结果文件放入 `data/raw/`
2. 更新 `backend/importers/data_import_config.yaml` 中的字段映射（如有变化）
3. 清空旧数据并重新导入：
   ```bash
   psql -U postgres -d green_compute -f backend/db/schema.sql  # 会重建所有表
   python3 backend/importers/import_excel_to_db.py
   ```
4. 如果知识文档有更新，重建 RAG 索引：`python3 backend/rag/build_index.py`
</details>

---

## 致谢

本项目的数据来源包括国家统计局、中国能源统计年鉴、中国科技统计年鉴、中国信息产业年鉴和各省统计年鉴等公开统计资料，在此一并致谢

---

<p align="center">
  <sub>Built with ❤️ using FastAPI · Next.js · PostgreSQL · ECharts · DeepSeek · Tailwind CSS</sub>
</p>
