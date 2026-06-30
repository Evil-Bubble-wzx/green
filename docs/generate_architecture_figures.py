#!/usr/bin/env python3
"""Generate architecture and system design figures for Chapter 9."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Arc
import numpy as np

OUT = "/Users/evilbubble/数据要素/green-compute-system/docs/chapter9_figures"

# Light theme colors
C_BG     = "#ffffff"
C_TEXT   = "#1a1a2e"
C_SUB    = "#334155"
C_BLUE   = "#0284c7"
C_GREEN  = "#059669"
C_AMBER  = "#d97706"
C_VIOLET = "#7c3aed"
C_RED    = "#dc2626"
C_CYAN   = "#0891b2"
C_PINK   = "#db2779"
C_LIGHT_BLUE  = "#e0f2fe"
C_LIGHT_GREEN = "#d1fae5"
C_LIGHT_AMBER = "#fef3c7"
C_LIGHT_VIOLET= "#ede9fe"
C_LIGHT_GRAY  = "#f8fafc"
C_BORDER = "#cbd5e1"

plt.rcParams.update({
    "font.sans-serif": ["PingFang SC", "Heiti SC", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "figure.facecolor": C_BG,
    "axes.facecolor": C_BG,
    "text.color": C_TEXT,
})

def fig9_3_frontend_layout():
    """Frontend page layout structure diagram."""
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_facecolor(C_BG)

    # Sidebar
    sidebar = FancyBboxPatch((0.2, 0.3), 2.0, 8.3, boxstyle="round,pad=0.1",
                              facecolor="#1e293b", edgecolor=C_BORDER, linewidth=1.5)
    ax.add_patch(sidebar)
    ax.text(1.2, 8.7, "导航侧边栏\n224px", ha="center", va="top", fontsize=9,
            color="#e2e8f0", fontweight="bold")

    nav_items = ["[1] 首页总览", "[2] 综合评价", "[3] 区域差异", "[4] 空间聚焦",
                 "[5] 动态演化", "[6] 省域诊断", "[7] 类型识别", "[8] SHAP解释",
                 "[9] 布局决策", "[10] 智能问答"]
    for i, item in enumerate(nav_items):
        y = 8.1 - i * 0.55
        color = "#38bdf8" if i == 0 else "#94a3b8"
        ax.text(1.2, y, item, ha="center", va="center", fontsize=7.5, color=color)

    # Header
    header = FancyBboxPatch((2.4, 8.0), 11.3, 0.7, boxstyle="round,pad=0.08",
                             facecolor=C_LIGHT_GRAY, edgecolor=C_BORDER, linewidth=1.5)
    ax.add_patch(header)
    ax.text(8.05, 8.35, "顶部状态栏 — 系统名称 | 数据状态标签 (2016-2024, 31省份, 数据就绪)",
            ha="center", va="center", fontsize=9, color=C_TEXT, fontweight="bold")

    # Main content area
    main = FancyBboxPatch((2.4, 0.3), 11.3, 7.5, boxstyle="round,pad=0.1",
                           facecolor=C_BG, edgecolor=C_BORDER, linewidth=1.5, linestyle="--")
    ax.add_patch(main)
    ax.text(8.05, 7.9, "中央内容区 (overflow-auto, 响应式网格布局)", ha="center", va="top",
            fontsize=8, color=C_SUB, style="italic")

    # Page cards inside main area
    pages = [
        (2.8, 6.5, "首页总览\n环形图+排名条+统计卡片", C_LIGHT_BLUE, C_BLUE),
        (6.0, 6.5, "综合评价\n玫瑰图+排名表", C_LIGHT_GREEN, C_GREEN),
        (9.2, 6.5, "区域差异\n折线图+堆叠柱状+雷达图", C_LIGHT_AMBER, C_AMBER),
        (2.8, 4.8, "空间聚焦\n中国地图+Moran折线图", C_LIGHT_VIOLET, C_VIOLET),
        (6.0, 4.8, "动态演化\n面积图+转移矩阵表", C_LIGHT_BLUE, C_BLUE),
        (9.2, 4.8, "省域诊断\n障碍条图+布局卡片", C_LIGHT_GREEN, C_GREEN),
        (2.8, 3.1, "类型识别\nLPA排名条+摘要卡片", C_LIGHT_AMBER, C_AMBER),
        (6.0, 3.1, "SHAP解释\n瀑布图+数据明细表", C_LIGHT_VIOLET, C_VIOLET),
        (9.2, 3.1, "布局决策\n进度条+策略卡片", C_LIGHT_BLUE, C_BLUE),
        (6.0, 1.4, "智能问答 (双栏布局)\n对话区+信息面板", "#fce7f3", C_PINK),
    ]

    for x, y, label, fill, edge in pages:
        w = 2.9 if label.startswith("智能") else 2.9
        h = 1.5 if label.startswith("智能") else 1.5
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                               facecolor=fill, edgecolor=edge, linewidth=1.2)
        ax.add_patch(card)
        ax.text(x + w/2, y + h/2, label, ha="center", va="center", fontsize=7, color=C_TEXT)

    ax.set_title("图9-3 前端页面布局结构图", fontsize=15, color=C_TEXT, fontweight="bold", pad=15)
    fig.savefig(f"{OUT}/fig9_3_frontend_layout.png", dpi=300, facecolor=C_BG)
    plt.close()
    print("✅ fig9_3_frontend_layout")


def fig9_5_backend_layers():
    """Backend service layered architecture."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor(C_BG)

    layers = [
        (1.0, 6.5, 12.0, 1.0, C_LIGHT_BLUE, C_BLUE,
         "API 路由层 (api/routes.py)",
         "GET /api/provinces | GET /api/scores | GET /api/overview | GET /api/dagum | GET /api/moran | GET /api/markov\n"
         "GET /api/lpa | GET /api/shap | GET /api/layout | GET /api/obstacles | GET /api/indicators | POST /api/chat",
         "参数校验 · 异常映射 (404/500) · 响应模型序列化"),
        (1.0, 4.8, 12.0, 1.3, C_LIGHT_GREEN, C_GREEN,
         "业务服务层 (services/)",
         "province · score · overview · obstacle · lpa · shap · layout · indicator · dagum · moran · markov  (11个服务模块)",
         "数据查询 · 业务逻辑封装 · Value错误抛出"),
        (1.0, 3.2, 12.0, 1.2, C_LIGHT_AMBER, C_AMBER,
         "数据模型层 (models.py + schemas.py)",
         "23个SQLAlchemy ORM模型 ←→ 42张PostgreSQL数据表  |  30个Pydantic响应模型",
         "ORM映射 · 类型校验 · 数据序列化"),
        (1.0, 1.4, 12.0, 1.4, C_LIGHT_VIOLET, C_VIOLET,
         "数据存储层 (PostgreSQL + SQLAlchemy)",
         "green_compute 数据库 → 基础信息 (3表) · 核心数据 (4表) · LPA (4表) · 空间演化 (12表) · "
         "障碍度 (8表) · SHAP (7表) · 布局决策 (6表)",
         "连接池 (pool_size=5) · 会话管理 · 导入管道"),
    ]

    for x, y, w, h, fill, edge, title, content, sub in layers:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.15",
                              facecolor=fill, edgecolor=edge, linewidth=1.8)
        ax.add_patch(box)
        ax.text(x + 0.3, y + h - 0.25, title, fontsize=11, color=C_TEXT, fontweight="bold", va="top")
        ax.text(x + 0.3, y + h - 0.6, content, fontsize=7.8, color=C_TEXT, va="top")
        ax.text(x + 0.3, y + 0.2, sub, fontsize=7, color=C_SUB, va="bottom", style="italic")

    # Arrows between layers
    for y_from, y_to in [(6.5, 6.1), (4.8, 4.4), (3.2, 2.8)]:
        ax.annotate("", xy=(7.0, y_to+0.05), xytext=(7.0, y_from-0.05),
                    arrowprops=dict(arrowstyle="->", color=C_SUB, lw=2.0))

    # Side labels
    ax.text(0.3, 7.0, "外部\n请求", ha="center", va="center", fontsize=9, color=C_BLUE, fontweight="bold")
    ax.annotate("", xy=(1.0, 7.0), xytext=(0.6, 7.0),
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=1.5))

    # Intelligent Agent box on the right
    agent_box = FancyBboxPatch((10.5, 5.0), 3.0, 2.5, boxstyle="round,pad=0.12",
                                facecolor="#fce7f3", edgecolor=C_PINK, linewidth=1.8)
    ax.add_patch(agent_box)
    ax.text(12.0, 7.15, "智能问答 Agent", fontsize=10, color=C_TEXT, fontweight="bold", ha="center")
    ax.text(12.0, 6.7, "问题分类 → RAG检索\nDB工具调用 → LLM生成", fontsize=7.5, color=C_TEXT, ha="center")
    ax.text(12.0, 6.0, "DeepSeek API\n10个查询工具\n10篇知识文档", fontsize=7, color=C_SUB, ha="center")

    # Connection line from service layer to agent
    ax.annotate("", xy=(10.5, 6.2), xytext=(13.0, 5.45),
                arrowprops=dict(arrowstyle="->", color=C_PINK, lw=1.2, connectionstyle="arc3,rad=-0.2"))

    ax.set_title("图9-5 后端服务分层结构图", fontsize=15, color=C_TEXT, fontweight="bold", pad=15)
    fig.savefig(f"{OUT}/fig9_5_backend_layers.png", dpi=300, facecolor=C_BG)
    plt.close()
    print("✅ fig9_5_backend_layers")


def fig9_6_database_structure():
    """Database table organization diagram."""
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor(C_BG)

    categories = [
        (0.3, 4.5, 2.8, 2.8, C_LIGHT_GRAY, C_BORDER,
         "基础信息\n(3表)", "province_basic\nadjacency_matrix\nindicator_system", C_SUB),
        (3.4, 4.5, 2.8, 2.8, C_LIGHT_BLUE, C_BLUE,
         "核心数据\n(4表)", "indicator_values\nindicator_values_normalized\nindicator_weights\ntopsis_scores", C_BLUE),
        (6.5, 4.5, 2.8, 2.8, C_LIGHT_GREEN, C_GREEN,
         "LPA分析\n(4表)", "lpa_province_assignment\nlpa_type_summary\nlpa_model_fit\nlpa_type_trajectory", C_GREEN),
        (9.6, 4.5, 2.8, 2.8, C_LIGHT_AMBER, C_AMBER,
         "空间演化\n(12表)", "dagum_decomposition\ndagum_intra_region\ndagum_inter_region\nmoran_results · lisa_results\nmarkov_* · spatial_*\nstate_thresholds · kde_*", C_AMBER),
        (12.7, 4.5, 2.8, 2.8, C_LIGHT_VIOLET, C_VIOLET,
         "障碍度\n(8表)", "obstacle_province\nobstacle_national\nobstacle_regional\nobstacle_lpa\nobstacle_indicator\nobstacle_annual_evolution\nobstacle_province_indicator_detail", C_VIOLET),
        (2.0, 1.0, 2.8, 2.8, C_LIGHT_BLUE, C_CYAN,
         "SHAP解释\n(7表)", "shap_local_top8\nshap_importance\nshap_model_metrics\nshap_predictions\nshap_annual_dimension\nshap_lpa_dimension\nshap_province_summary", C_CYAN),
        (5.5, 1.0, 2.8, 2.8, "#fce7f3", C_PINK,
         "布局决策\n(6表)", "layout_province_decision\nlayout_type_summary\nlayout_type_features\nlayout_lpa_matrix\nlayout_strategy_library\nlayout_strategy_priority", C_PINK),
        (9.0, 1.0, 2.8, 2.8, C_LIGHT_GRAY, C_SUB,
         "知识库\n(10篇文档)", "系统概述 · TOPSIS · LPA\n空间演化 · 障碍度\nSHAP · 布局规则\n预测规则 · 指标 · FAQ", C_SUB),
    ]

    for x, y, w, h, fill, edge, title, content, tc in categories:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=fill, edgecolor=edge, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.3, title, fontsize=10, color=tc, fontweight="bold", ha="center", va="top")
        ax.text(x + w/2, y + h/2 - 0.2, content, fontsize=6.5, color=C_TEXT, ha="center", va="center")

    # Central database icon
    db_circle = plt.Circle((8.0, 7.1), 0.5, facecolor=C_BLUE, edgecolor=C_BLUE, linewidth=2, alpha=0.15)
    ax.add_patch(db_circle)
    ax.text(8.0, 7.1, "PostgreSQL\ngreen_compute", ha="center", va="center", fontsize=8, color=C_BLUE, fontweight="bold")
    ax.text(8.0, 5.8, "42张数据表 · 3000+条记录 · 2016-2024年 · 31省", ha="center", fontsize=8, color=C_SUB)

    # Connection lines from DB to categories
    for cx, cy in [(1.7, 4.5), (4.8, 4.5), (7.9, 4.5), (11.0, 4.5), (14.1, 4.5)]:
        ax.plot([8.0, cx + 1.4], [6.6, cy + 2.8], color=C_BORDER, lw=0.8, alpha=0.5)
    for cx, cy in [(3.4, 1.0), (6.9, 1.0), (10.4, 1.0)]:
        ax.plot([8.0, cx + 1.4], [6.6, cy + 2.8], color=C_BORDER, lw=0.8, alpha=0.5)

    ax.set_title("图9-6 数据库/数据文件组织关系图", fontsize=15, color=C_TEXT, fontweight="bold", pad=15)
    fig.savefig(f"{OUT}/fig9_6_database_structure.png", dpi=300, facecolor=C_BG)
    plt.close()
    print("✅ fig9_6_database_structure")


def fig9_7_rag_workflow():
    """RAG intelligent Q&A workflow diagram — VERTICAL with properly sized boxes."""
    fig, ax = plt.subplots(figsize=(14, 20))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 20)
    ax.axis("off")
    ax.set_facecolor(C_BG)

    # Box geometry — wide enough and tall enough for multi-line Chinese text
    box_w = 8.5
    box_h = 2.2
    cx = 7.0
    lx = cx - box_w / 2

    # Each step: (y_top, fill, edge, title_color, title, desc_line1, desc_line2, desc_line3)
    steps = [
        (18.0, C_LIGHT_GRAY, C_BORDER, C_TEXT,
         "① 用户提问",
         "用户通过自然语言输入问题（≤ 2000 字符），支持中文提问",
         "", ""),
        (15.3, C_LIGHT_BLUE, C_BLUE, C_BLUE,
         "② 相关性检查",
         "关键词匹配 77 个领域术语（31 个省份名称 + 46 个专业关键词）",
         "不相关问题直接返回 out_of_scope 引导回答，不消耗 LLM 调用配额",
         ""),
        (12.6, C_LIGHT_GREEN, C_GREEN, C_GREEN,
         "③ 问题分类（DeepSeek LLM + 规则兜底）",
         "6 个类别：概念解释 · 数据查询 · 省域诊断 · 布局建议 · 未来预测 · 暂不支持",
         "DeepSeek 不可用时自动降级为基于关键词的规则分类器",
         ""),
        (9.9, C_LIGHT_AMBER, C_AMBER, C_AMBER,
         "④ RAG 检索增强（TF-IDF 向量空间模型）",
         "scikit-learn TfidfVectorizer（char_wb 中文分词，max_features=2000，ngram 1-2）",
         "余弦相似度检索 Top 5 知识片段 —— 10 篇专业知识文档",
         ""),
        (7.2, C_LIGHT_VIOLET, C_VIOLET, C_VIOLET,
         "⑤ 数据库工具自动调度（10 个查询函数）",
         "排名查询 · 省份得分 · 趋势分析 · LPA 类型 · 障碍诊断 · SHAP 特征",
         "布局推荐 · 多省对比 · 未来潜力预测（6 因子加权）· 最新得分快照",
         ""),
        (4.5, "#fce7f3", C_PINK, C_PINK,
         "⑥ DeepSeek Chat 回答生成",
         "模型：deepseek-chat | temperature = 0.5 | max_tokens = 2048 | 60 s 超时",
         "六段式结构化回答：结论 → 数据依据 → 模型依据 → 解释逻辑 → 建议 → 局限性说明",
         "DeepSeek 不可用时自动降级为离线模式，直接展示数据库查询结果"),
    ]

    for y_top, fill, edge, tc, title, d1, d2, d3 in steps:
        y_bottom = y_top - box_h
        box = FancyBboxPatch((lx, y_bottom), box_w, box_h,
                              boxstyle="round,pad=0.2",
                              facecolor=fill, edgecolor=edge, linewidth=2.2)
        ax.add_patch(box)

        # Title near top
        ax.text(cx, y_bottom + box_h - 0.35, title,
                fontsize=16, color=tc, fontweight="bold", ha="center", va="top")

        # Description lines — stacked inside the remaining box space
        line_y = y_bottom + box_h - 0.90
        for dl in [d1, d2, d3]:
            if dl:
                ax.text(cx, line_y, dl,
                        fontsize=12, color=C_TEXT, ha="center", va="top")
                line_y -= 0.45

    # ---- Vertical arrows between steps ----
    for i in range(len(steps) - 1):
        y_from = steps[i][0] - box_h
        y_to = steps[i+1][0]
        ax.annotate("", xy=(cx, y_to + 0.05), xytext=(cx, y_from - 0.05),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=3.0))

    # ---- OUT-OF-SCOPE side branch (right side) ----
    branch_y = 14.4
    ax.annotate("", xy=(lx + box_w + 0.1, branch_y), xytext=(lx + box_w + 1.8, branch_y),
                arrowprops=dict(arrowstyle="->", color=C_RED, lw=2.2))
    out_box = FancyBboxPatch((lx + box_w + 0.3, branch_y - 0.55), 3.5, 1.1,
                              boxstyle="round,pad=0.1",
                              facecolor="#fef2f2", edgecolor=C_RED, linewidth=2.0)
    ax.add_patch(out_box)
    ax.text(lx + box_w + 2.05, branch_y + 0.35, "不相关",
            fontsize=15, color=C_RED, fontweight="bold", ha="center")
    ax.text(lx + box_w + 2.05, branch_y - 0.10, "返回 out_of_scope\n引导回答（HTTP 200）",
            fontsize=12, color=C_RED, ha="center")

    # ---- BOTTOM: Data source panels (3 columns) ----
    panel_top = 2.5
    panel_h = 2.2
    panel_w = 4.2
    panels = [
        (0.3, C_LIGHT_GRAY, C_BORDER,
         "知识库（10 篇文档）",
         ["系统概述 · TOPSIS 模型", "LPA 模型 · 空间演化分析",
          "障碍度模型 · SHAP 解释", "布局决策规则 · 未来预测规则",
          "指标体系参考 · FAQ"]),
        (4.9, C_LIGHT_BLUE, C_BLUE,
         "数据库工具（10 个）",
         ["排名查询 · 省份得分 · 趋势分析", "LPA 类型 · 障碍诊断",
          "SHAP 特征贡献 · 布局推荐", "多省横向对比", "未来潜力预测（6 因子加权）"]),
        (9.5, C_LIGHT_GREEN, C_GREEN,
         "6 类问题响应策略",
         ["data_query → 排名 + 得分数据", "province_diagnosis → 诊断 + 解释",
          "layout_recommendation → 布局推荐", "future_prediction → 潜力预测",
          "concept_explanation → RAG 知识检索", "unsupported → 粒度说明 + 替代建议"]),
    ]

    for x, fill, edge, title, lines in panels:
        y_bottom = panel_top - panel_h
        box = FancyBboxPatch((x, y_bottom), panel_w, panel_h,
                              boxstyle="round,pad=0.12",
                              facecolor=fill, edgecolor=edge, linewidth=2.0)
        ax.add_patch(box)
        ax.text(x + panel_w / 2, panel_top - 0.30, title,
                fontsize=14, color=C_TEXT, fontweight="bold", ha="center", va="top")
        line_y = panel_top - 0.80
        for line in lines:
            ax.text(x + panel_w / 2, line_y, line,
                    fontsize=11, color=C_SUB, ha="center", va="top")
            line_y -= 0.35

    # Dashed connectors from main flow to bottom panels
    for sx in [2.4, 7.0, 11.6]:
        ax.plot([cx, sx], [box_h + 0.3, panel_top], color="#cbd5e1", lw=1.0, alpha=0.5, linestyle="--")

    ax.set_title("图 9-7  智能问答 RAG 工作流程图", fontsize=22, color=C_TEXT, fontweight="bold", pad=25)
    fig.savefig(f"{OUT}/fig9_7_rag_workflow.png", dpi=300, facecolor=C_BG)
    plt.close()
    print("✅ fig9_7_rag_workflow")


def fig9_8_deployment_architecture():
    """System deployment architecture diagram."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor(C_BG)

    # User layer
    user_box = FancyBboxPatch((4.0, 6.8), 6.0, 0.7, boxstyle="round,pad=0.1",
                               facecolor=C_LIGHT_GRAY, edgecolor=C_BORDER, linewidth=1.5)
    ax.add_patch(user_box)
    ax.text(7.0, 7.15, "用户浏览器 (任何联网设备)", ha="center", va="center", fontsize=10,
            color=C_TEXT, fontweight="bold")

    # ngrok tunnel
    ax.annotate("", xy=(7.0, 6.8), xytext=(7.0, 6.3),
                arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=2.0))
    ngrok_box = FancyBboxPatch((4.5, 5.8), 5.0, 0.5, boxstyle="round,pad=0.08",
                                facecolor=C_LIGHT_GREEN, edgecolor=C_GREEN, linewidth=1.5)
    ax.add_patch(ngrok_box)
    ax.text(7.0, 6.05, "ngrok 公网隧道 (HTTPS)", ha="center", va="center", fontsize=9, color=C_GREEN, fontweight="bold")

    # Next.js server
    ax.annotate("", xy=(7.0, 5.8), xytext=(7.0, 5.3),
                arrowprops=dict(arrowstyle="->", color=C_BLUE, lw=2.0))
    next_box = FancyBboxPatch((4.0, 4.5), 6.0, 0.8, boxstyle="round,pad=0.1",
                               facecolor=C_LIGHT_BLUE, edgecolor=C_BLUE, linewidth=1.8)
    ax.add_patch(next_box)
    ax.text(7.0, 5.1, "Next.js 15 服务器 (Port 3000)", ha="center", va="center", fontsize=10,
            color=C_BLUE, fontweight="bold")
    ax.text(7.0, 4.75, "静态资源 + SSR + API代理 (/api/* → 127.0.0.1:8000)", ha="center", va="center",
            fontsize=7.5, color=C_TEXT)

    # FastAPI backend
    ax.annotate("", xy=(7.0, 4.5), xytext=(7.0, 4.0),
                arrowprops=dict(arrowstyle="->", color=C_VIOLET, lw=2.0))
    backend_box = FancyBboxPatch((4.0, 2.8), 6.0, 1.2, boxstyle="round,pad=0.1",
                                  facecolor=C_LIGHT_VIOLET, edgecolor=C_VIOLET, linewidth=1.8)
    ax.add_patch(backend_box)
    ax.text(7.0, 3.8, "FastAPI 后端服务 (Port 8000)", ha="center", va="center", fontsize=10,
            color=C_VIOLET, fontweight="bold")
    ax.text(7.0, 3.45, "12个REST API + 智能问答Agent (RAG + DeepSeek)", ha="center", va="center", fontsize=7.5, color=C_TEXT)
    ax.text(7.0, 3.1, "崩溃自动重启 (while true + uvicorn)", ha="center", va="center", fontsize=7, color=C_SUB)

    # PostgreSQL
    ax.annotate("", xy=(7.0, 2.8), xytext=(7.0, 2.3),
                arrowprops=dict(arrowstyle="->", color=C_AMBER, lw=2.0))
    db_box = FancyBboxPatch((4.5, 1.3), 5.0, 1.0, boxstyle="round,pad=0.1",
                             facecolor=C_LIGHT_AMBER, edgecolor=C_AMBER, linewidth=1.8)
    ax.add_patch(db_box)
    ax.text(7.0, 2.0, "PostgreSQL 数据库 (Port 5432)", ha="center", va="center", fontsize=10,
            color=C_AMBER, fontweight="bold")
    ax.text(7.0, 1.6, "green_compute · 42张表 · 3000+条记录 · 连接池5", ha="center", va="center", fontsize=7.5, color=C_TEXT)

    # DeepSeek API (external)
    deepseek_box = FancyBboxPatch((11.0, 4.0), 2.8, 1.5, boxstyle="round,pad=0.1",
                                   facecolor="#fce7f3", edgecolor=C_PINK, linewidth=1.5)
    ax.add_patch(deepseek_box)
    ax.text(12.4, 5.2, "DeepSeek API", ha="center", va="center", fontsize=9, color=C_TEXT, fontweight="bold")
    ax.text(12.4, 4.7, "deepseek-chat\n问题分类\n回答生成", ha="center", va="center", fontsize=7.5, color=C_SUB)
    ax.annotate("", xy=(11.0, 4.75), xytext=(10.0, 3.8),
                arrowprops=dict(arrowstyle="<->", color=C_PINK, lw=1.2, connectionstyle="arc3,rad=0.3"))

    # Data files
    data_box = FancyBboxPatch((0.3, 2.0), 2.8, 2.0, boxstyle="round,pad=0.1",
                               facecolor=C_LIGHT_GRAY, edgecolor=C_BORDER, linewidth=1.2)
    ax.add_patch(data_box)
    ax.text(1.7, 3.7, "数据文件", ha="center", va="center", fontsize=9, color=C_TEXT, fontweight="bold")
    ax.text(1.7, 3.2, "10个Excel源文件\n导入管道 (YAML配置)\nTF-IDF索引 (pkl)\nChina GeoJSON地图", ha="center", va="center", fontsize=7, color=C_SUB)
    ax.annotate("", xy=(4.5, 3.0), xytext=(3.1, 3.0),
                arrowprops=dict(arrowstyle="->", color=C_BORDER, lw=1.2))

    # start_public.sh label
    ax.text(7.0, 6.6, "start_public.sh 一键启动脚本", ha="center", va="center", fontsize=8,
            color=C_SUB, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=C_LIGHT_GRAY, edgecolor=C_BORDER, alpha=0.8))

    ax.set_title("图9-8 系统部署架构图", fontsize=15, color=C_TEXT, fontweight="bold", pad=15)
    fig.savefig(f"{OUT}/fig9_8_deployment_architecture.png", dpi=300, facecolor=C_BG)
    plt.close()
    print("✅ fig9_8_deployment_architecture")


def fig9_4_visual_components():
    """Core visualization components overview."""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor(C_BG)

    components = [
        (0.3, 5.5, 2.5, 2.0, C_LIGHT_BLUE, C_BLUE,
         "ChinaMap\n中国地图", "GeoJSON渲染\nChoropleth分级着色\nZoom/Pan/Hover\nProvince信息卡片"),
        (3.1, 5.5, 2.5, 2.0, C_LIGHT_GREEN, C_GREEN,
         "RoseChart\n南丁格尔玫瑰图", "极坐标扇形图\n区域多维对比\n渐进式展开动画\nHover高亮+Tooltip"),
        (5.9, 5.5, 2.5, 2.0, C_LIGHT_AMBER, C_AMBER,
         "DonutChart\n环形饼图", "内外环设计\n中心文字动态显示\n弹性动画\n四色渐变"),
        (8.7, 5.5, 2.5, 2.0, C_LIGHT_VIOLET, C_VIOLET,
         "RankingBar\n横向排名条", "从上到下渐进加载\n前3名金/银/铜\n排序交互\nEmoji奖牌标签"),
        (11.5, 5.5, 2.5, 2.0, C_LIGHT_BLUE, C_CYAN,
         "ShapWaterfall\nSHAP瀑布图", "正负方向颜色编码\n绿色=正向,红色=负向\n按绝对值排序\nDimension Tooltip"),

        (0.3, 2.5, 2.5, 2.0, C_LIGHT_GRAY, C_BORDER,
         "LineChart\n折线图", "平滑曲线\n可配置面积填充\nHover十字准星\n时间序列Tooltip"),
        (3.1, 2.5, 2.5, 2.0, C_LIGHT_BLUE, C_BLUE,
         "AreaChart\n折线面积图", "渐变透明填充\n绿→蓝→紫渐变\n圆形数据标记\n时序变化展示"),
        (5.9, 2.5, 2.5, 2.0, C_LIGHT_GREEN, C_GREEN,
         "StackedBar\n堆叠柱状图", "多系列堆叠\n百分比Y轴\n图例点击切换\nLayer Hover高亮"),
        (8.7, 2.5, 2.5, 2.0, C_LIGHT_AMBER, C_AMBER,
         "BarChart\n柱状图", "垂直/水平方向\n圆角柱形\nEmphasis状态\n四色按类映射"),
        (11.5, 2.5, 2.5, 2.0, C_LIGHT_GRAY, C_SUB,
         "RegionChart\n区域柱状图", "四大区域固定配色\n东部蓝·中部绿\n西部橙·东北紫\nLabel数值标注"),
    ]

    for x, y, w, h, fill, edge, title, content in components:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              facecolor=fill, edgecolor=edge, linewidth=1.5)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.2, title, fontsize=8.5, color=C_TEXT, fontweight="bold", ha="center", va="top")
        ax.text(x + w/2, y + h/2 - 0.15, content, fontsize=6.5, color=C_SUB, ha="center", va="center")

    ax.set_title("图9-4 核心可视化组件示意图", fontsize=15, color=C_TEXT, fontweight="bold", pad=15)
    fig.savefig(f"{OUT}/fig9_4_visual_components.png", dpi=300, facecolor=C_BG)
    plt.close()
    print("✅ fig9_4_visual_components")


if __name__ == "__main__":
    print(f"Generating architecture figures to {OUT}...")
    fig9_3_frontend_layout()
    fig9_4_visual_components()
    fig9_5_backend_layers()
    fig9_6_database_structure()
    fig9_7_rag_workflow()
    fig9_8_deployment_architecture()
    print(f"\n✅ All architecture figures saved to {OUT}")
