# Green Compute System - Data Import Module

## 概述

本模块负责将 `data/raw/` 目录下的 Excel 数据文件清洗并导入 PostgreSQL 数据库。

## 目录结构

```
backend/
├── db/
│   ├── database.py          # SQLAlchemy 数据库连接
│   └── schema.sql           # PostgreSQL 表结构定义
├── importers/
│   ├── data_import_config.yaml  # 导入配置文件（核心）
│   ├── inspect_excel_files.py   # Excel 文件扫描工具
│   ├── import_excel_to_db.py    # 数据导入主脚本
│   └── README.md               # 本文件
├── api/                     # FastAPI 接口（后续开发）
└── services/                # 业务逻辑层（后续开发）
```

## 前置条件

### 1. 安装 PostgreSQL

确保 PostgreSQL 已安装并运行。

### 2. 创建数据库

```bash
createdb -U postgres green_compute
```

或通过 psql：

```sql
CREATE DATABASE green_compute;
```

### 3. 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 4. 配置 .env 文件

```bash
cp .env.example .env
```

编辑 `.env`，填入实际的数据库密码：

```
DATABASE_URL=postgresql+psycopg2://postgres:你的密码@localhost:5432/green_compute
```

## 执行顺序

### 第一步：扫描 Excel 文件

```bash
python backend/importers/inspect_excel_files.py
```

这会生成 `data/excel_inspection_report.md`，包含每个 Excel 文件的：
- 文件名、Sheet 名
- 行数、列数
- 列名列表
- 前 5 行数据样本

**请仔细检查报告中的列名是否与 `data_import_config.yaml` 中的 column_mapping 匹配。**

### 第二步：检查并完善 data_import_config.yaml

根据第一步的扫描结果，必要时修改 `backend/importers/data_import_config.yaml`：

- 确认 `column_mapping` 中 Excel 列名与实际一致
- 确认 `required_fields` 和 `unique_keys` 正确
- 确认 `hub_provinces` 列表准确（国家算力枢纽节点省份）

### 第三步：创建数据库表

```bash
psql -U postgres -h localhost -d green_compute -f backend/db/schema.sql
```

如果使用远程数据库，请替换连接参数：

```bash
psql "$DATABASE_URL" -f backend/db/schema.sql
```

### 第四步：导入数据

```bash
python backend/importers/import_excel_to_db.py
```

导入完成后查看报告：`data/data_validation_report.md`

## 常见错误与处理

### 数据库连接失败

```
❌ Database connection failed
```

**原因：**
- PostgreSQL 未启动
- `.env` 中的密码错误
- 数据库 `green_compute` 不存在

**解决：**
```bash
# 检查 PostgreSQL 是否运行
pg_isready -h localhost

# 创建数据库
createdb -U postgres green_compute

# 验证 .env 配置
cat .env
```

### 表不存在

```
⚠️ Table 'xxx' does not exist
```

**原因：** 未执行 `schema.sql`

**解决：**
```bash
psql -U postgres -h localhost -d green_compute -f backend/db/schema.sql
```

### Excel 列名不匹配

```
⚠️ Required field 'province' not found in data
```

**原因：** Excel 文件中的列名与 `data_import_config.yaml` 中的 `column_mapping` 不一致。

**解决：**
1. 运行 `inspect_excel_files.py` 查看实际列名
2. 修改 `data_import_config.yaml` 中对应的 `column_mapping`

### 唯一键冲突

导入脚本默认使用 `append` 模式，已存在的数据会被跳过（不会报错退出）。跳过记录会在报告中列出。

如需全量替换，修改 `data_import_config.yaml` 中的 `import_mode` 为 `replace`（注意：replace 会清空表后重新导入）。

### 省份名称不统一

导入脚本会自动标准化省份名称：
- `内蒙古自治区` → `内蒙古`
- `广西壮族自治区` → `广西`
- 等等

如需添加更多映射，编辑 `data_import_config.yaml` 中的 `province_standardization` 部分。

### 其他错误

数据验证报告 `data/data_validation_report.md` 会记录所有警告和错误，请先查看该报告。

## 字段确认清单

以下字段需要人工确认（导入脚本无法自动判断）：

| 序号 | 字段 | 说明 | 如何确认 |
|------|------|------|----------|
| 1 | `hub_provinces` | 国家算力枢纽节点省份 | 对照国家政策文件确认 |
| 2 | `region_mapping` | 省份→区域映射 | 确认东部/中部/西部/东北划分正确 |
| 3 | `indicator_code` | 指标编码 X01-X34 | 对照 data_dictionary.xlsx |
| 4 | Markov `from_state` | 传统Markov首列列名 | 检查Excel中 "Unnamed: 0" 列的内容 |
| 5 | `is_hub` 字段 | 省份是否枢纽节点 | 基于 x34 字段值和政策文件 |

## 数据库表一览

| 类别 | 表名 | 来源 | 说明 |
|------|------|------|------|
| 基础 | `province_basic` | - | 省份基本信息 |
| 基础 | `indicator_system` | 表2-1 | 指标体系定义 |
| 核心 | `indicator_values` | clean_data | 原始指标值 |
| 核心 | `indicator_values_normalized` | 表3-1 | 标准化指标值 |
| 核心 | `indicator_weights` | 表3-2 | 组合权重 |
| 核心 | `topsis_scores` | 表3-3 | TOPSIS综合得分 |
| LPA | `lpa_model_fit` | 第4章 | 模型拟合 |
| LPA | `lpa_type_summary` | 第4章 | 类型汇总 |
| LPA | `lpa_province_assignment` | 第4章 | 省份归属 |
| LPA | `lpa_type_trajectory` | 第4章 | 类型轨迹 |
| 空间 | `kde_statistics` | 第5章 | KDE统计 |
| 空间 | `dagum_decomposition` | 第5章 | Dagum分解 |
| 空间 | `dagum_intra_region` | 第5章 | 区域内差异 |
| 空间 | `dagum_inter_region` | 第5章 | 区域间差异 |
| 空间 | `moran_results` | 第5章 | Moran's I |
| 空间 | `lisa_results` | 第5章 | LISA |
| 空间 | `markov_frequency` | 第5章 | Markov频数 |
| 空间 | `markov_probability` | 第5章 | Markov概率 |
| 空间 | `spatial_markov` | 第5章 | 空间Markov |
| 空间 | `spatial_lag_state` | 第5章 | 空间滞后状态 |
| 空间 | `state_thresholds` | 第5章 | 状态阈值 |
| 空间 | `adjacency_matrix` | 第5章 | 邻接矩阵 |
| 障碍度 | `obstacle_national` | 第6章 | 全国维度 |
| 障碍度 | `obstacle_regional` | 第6章 | 区域维度 |
| 障碍度 | `obstacle_lpa` | 第6章 | LPA维度 |
| 障碍度 | `obstacle_province` | 第6章 | 省份短板 |
| 障碍度 | `obstacle_indicator` | 第6章 | 指标障碍度 |
| 障碍度 | `obstacle_annual_evolution` | 第6章 | 年度演化 |
| 障碍度 | `obstacle_province_indicator_detail` | 第6章 | 省份明细 |
| SHAP | `shap_model_metrics` | 第7章 | 模型检验 |
| SHAP | `shap_predictions` | 第7章 | 预测结果 |
| SHAP | `shap_importance` | 第7章 | 特征重要性 |
| SHAP | `shap_annual_dimension_contribution` | 第7章 | 年度维度 |
| SHAP | `shap_lpa_dimension_contribution` | 第7章 | LPA维度 |
| SHAP | `shap_province_summary` | 第7章 | 省份汇总 |
| SHAP | `shap_local_top8` | 第7章 | 局部解释 |
| 布局 | `layout_province_decision` | 第8章 | 省份决策 |
| 布局 | `layout_type_summary` | 第8章 | 类型汇总 |
| 布局 | `layout_type_features` | 第8章 | 特征均值 |
| 布局 | `layout_lpa_matrix` | 第8章 | LPA映射 |
| 布局 | `layout_strategy_library` | 第8章 | 策略库 |
| 布局 | `layout_strategy_priority` | 第8章 | 策略优先级 |

## 后续集成

导入完成后，数据可供以下模块使用：
- **FastAPI** (`backend/api/`) — 提供 REST API 查询
- **前端可视化** (`frontend/`) — 地图、图表、仪表盘
- **RAG 智能体** — 基于数据库查询的智能问答
