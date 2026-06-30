#!/usr/bin/env python3
"""Generate publication-quality figures for Chapter 9."""

import os, sys, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

# --- Config ---
PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "docs" / "chapter9_figures"
OUT.mkdir(parents=True, exist_ok=True)

# Color palette — chart accent colors (work on both dark and light backgrounds)
C_BLUE   = "#0284c7"
C_GREEN  = "#059669"
C_AMBER  = "#d97706"
C_VIOLET = "#7c3aed"
C_RED    = "#dc2626"
C_CYAN   = "#0891b2"
C_PINK   = "#db2777"

# Light theme (paper-ready)
C_DARK   = "#ffffff"
C_CARD   = "#f8fafc"
C_TEXT   = "#1a1a2e"
C_SUB    = "#334155"
C_EDGE   = "#cbd5e1"
C_GRID   = "#e2e8f0"

plt.rcParams.update({
    "figure.facecolor": C_DARK,
    "axes.facecolor": C_CARD,
    "axes.edgecolor": C_EDGE,
    "axes.labelcolor": C_SUB,
    "text.color": C_TEXT,
    "xtick.color": C_SUB,
    "ytick.color": C_SUB,
    "grid.color": C_GRID,
    "grid.alpha": 0.8,
    "font.size": 10,
    "font.sans-serif": ["Heiti SC", "PingFang SC", "Arial Unicode MS", "DejaVu Sans"],
    "axes.unicode_minus": False,
    "axes.titlesize": 13,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": C_DARK,
})

# --- DB ---
from dotenv import load_dotenv
load_dotenv(PROJECT / ".env")
from sqlalchemy import create_engine, text
engine = create_engine(os.getenv("DATABASE_URL"))

def query(sql, params=None):
    with engine.connect() as conn:
        return [dict(r._mapping) for r in conn.execute(text(sql), params or {}).fetchall()]

# ================================================================
# Figure 9-3: Dashboard overview (donut + ranking lollipop)
# ================================================================
def fig9_3():
    scores = query("SELECT province, composite_score, rank FROM topsis_scores WHERE year=2024 ORDER BY rank")
    dagum = query("SELECT year, total_gini FROM dagum_decomposition ORDER BY year")
    overview = query("SELECT province, region FROM adjacency_matrix")
    region_map = {r["province"]: r["region"] for r in overview}
    # Region averages from scores
    regions = {}
    for s in scores:
        r = region_map.get(s["province"], "Unknown")
        regions.setdefault(r, []).append(s["composite_score"])
    region_avg = {r: sum(v)/len(v) for r, v in regions.items()}

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    # Left: Donut
    ax = axes[0]
    colors = [C_BLUE, C_GREEN, C_AMBER, C_VIOLET]
    vals = list(region_avg.values())
    labels = list(region_avg.keys())
    wedges, texts = ax.pie(vals, labels=None, colors=colors, startangle=90,
                           wedgeprops={"width": 0.35, "edgecolor": "#e2e8f0", "linewidth": 2})
    ax.set_title("区域平均得分分布", fontsize=13, color=C_TEXT, pad=15)
    ax.legend(wedges, [f"{l} ({v:.4f})" for l, v in zip(labels, vals)],
              loc="lower center", ncol=4, frameon=False, labelcolor=C_SUB, fontsize=9)

    # Right: horizontal lollipop ranking (top 15 + bottom 5)
    ax = axes[1]
    top15 = scores[:15]
    bot5 = scores[-5:]
    show = top15 + bot5
    names = [s["province"] for s in show]
    values = [s["composite_score"] for s in show]
    colors_r = [C_AMBER if s["rank"] == 1 else C_GREEN if s["rank"] <= 3 else C_BLUE for s in show]
    ypos = range(len(names))
    ax.hlines(ypos, 0, values, colors=colors_r, linewidth=3, alpha=0.8)
    ax.scatter(values, ypos, c=colors_r, s=60, zorder=3, edgecolors="#1a1a2e", linewidth=0.5)
    ax.set_yticks(ypos)
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("综合得分", color=C_SUB)
    ax.set_title("31 省综合得分排名 (2024)", fontsize=13, color=C_TEXT, pad=15)
    ax.grid(axis="x", alpha=0.3)
    for i, (n, v) in enumerate(zip(names, values)):
        ax.text(v + 0.005, i, f"#{i+1}", va="center", fontsize=7, color=C_SUB)
    fig.tight_layout()
    fig.savefig(OUT / "fig9-3_dashboard.png", dpi=300)
    plt.close()
    print("✅ fig9-3")

# ================================================================
# Figure 9-4: Rose chart for evaluation
# ================================================================
def fig9_4():
    scores = query("SELECT province, composite_score FROM topsis_scores WHERE year=2024")
    overview = query("SELECT province, region FROM adjacency_matrix")
    region_map = {r["province"]: r["region"] for r in overview}
    regions = {}
    for s in scores:
        r = region_map.get(s["province"], "Unknown")
        regions.setdefault(r, []).append(s["composite_score"])
    region_avg = {r: sum(v)/len(v) for r, v in regions.items()}

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})
    categories = list(region_avg.keys())
    values = list(region_avg.values())
    N = len(categories)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]
    colors = [C_BLUE, C_GREEN, C_AMBER, C_VIOLET]
    bars = ax.bar(angles[:-1], values[:-1], width=2*np.pi/N*0.8, bottom=0.05,
                  color=[colors[i % len(colors)] for i in range(N)], alpha=0.85, edgecolor="#e2e8f0", linewidth=1.5)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color=C_TEXT, fontsize=11)
    ax.set_yticklabels([])
    ax.set_title("区域平均得分 — 南丁格尔玫瑰图", fontsize=14, color=C_TEXT, pad=25)
    for i, (cat, val) in enumerate(zip(categories, values[:-1])):
        ax.text(angles[i], val + 0.015, f"{val:.4f}", ha="center", fontsize=9, color=C_TEXT)
    fig.tight_layout()
    fig.savefig(OUT / "fig9-4_rose.png", dpi=300)
    plt.close()
    print("✅ fig9-4")

# ================================================================
# Figure 9-5: Regional difference combo
# ================================================================
def fig9_5():
    dagum = query("SELECT * FROM dagum_decomposition ORDER BY year")
    intra = query("SELECT * FROM dagum_intra_region WHERE year=2024 ORDER BY region")
    inter = query("SELECT * FROM dagum_inter_region WHERE year=2024 ORDER BY inter_region_gini DESC")

    fig, axes = plt.subplots(2, 2, figsize=(14, 11))
    # 1: Line
    ax = axes[0, 0]
    years = [d["year"] for d in dagum]
    gini = [d["total_gini"] for d in dagum]
    ax.fill_between(years, gini, alpha=0.2, color=C_BLUE)
    ax.plot(years, gini, color=C_BLUE, linewidth=2.5, marker="o", markersize=5)
    ax.set_title("总体基尼系数变化趋势", color=C_TEXT)
    ax.set_ylabel("基尼系数", color=C_SUB)
    ax.grid(alpha=0.3)

    # 2: Stacked area
    ax = axes[0, 1]
    i_vals = [d["intra_region_contribution_rate"]*100 for d in dagum]
    e_vals = [d["inter_region_contribution_rate"]*100 for d in dagum]
    h_vals = [d["hypervariable_density_contribution_rate"]*100 for d in dagum]
    ax.stackplot(years, i_vals, e_vals, h_vals,
                 labels=["区域内", "区域间", "超变密度"],
                 colors=[C_BLUE, C_GREEN, C_VIOLET], alpha=0.8)
    ax.set_title("差异贡献率逐年分解", color=C_TEXT)
    ax.set_ylabel("贡献率 (%)", color=C_SUB)
    ax.legend(frameon=False, labelcolor=C_SUB, fontsize=8)
    ax.grid(alpha=0.3)

    # 3: Horizontal bar
    ax = axes[1, 0]
    pairs = [d["region_pair"] for d in inter]
    vals = [d["inter_region_gini"] for d in inter]
    ax.barh(pairs, vals, color=C_GREEN, height=0.5, alpha=0.85)
    ax.set_title("区域间基尼系数 (2024)", color=C_TEXT)
    ax.set_xlabel("基尼系数", color=C_SUB)
    ax.grid(axis="x", alpha=0.3)

    # 4: Radar
    ax = axes[1, 1]
    r_names = [d["region"] for d in intra]
    r_vals = [d["intra_region_gini"] for d in intra]
    N = len(r_names)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    r_vals += r_vals[:1]
    angles += angles[:1]
    ax = plt.subplot(2, 2, 4, projection="polar")
    ax.fill(angles, r_vals, color=C_PINK, alpha=0.2)
    ax.plot(angles, r_vals, color=C_PINK, linewidth=2, marker="o")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(r_names, color=C_TEXT, fontsize=10)
    ax.set_title("区域内基尼系数 (2024)", color=C_TEXT, pad=15)
    ax.set_yticklabels([])
    fig.tight_layout()
    fig.savefig(OUT / "fig9-5_regional_diff.png", dpi=300)
    plt.close()
    print("✅ fig9-5")

# ================================================================
# Figure 9-6: Spatial map (simplified scatter on China outline)
# ================================================================
def fig9_6():
    # Just a placeholder — real map requires GeoJSON rendering
    fig, ax = plt.subplots(figsize=(10, 8))
    scores = query("SELECT province, composite_score, rank FROM topsis_scores WHERE year=2024")
    # Scatter with approximate coordinates
    coords = {
        "北京": (116.4, 39.9), "上海": (121.5, 31.2), "广东": (113.3, 23.1),
        "江苏": (118.8, 32.1), "浙江": (120.2, 30.3), "山东": (117.0, 36.7),
        "河南": (113.7, 34.8), "四川": (104.1, 30.6), "湖北": (114.3, 30.6),
        "湖南": (113.0, 28.2), "福建": (119.3, 26.1), "安徽": (117.3, 31.9),
        "河北": (114.5, 38.0), "陕西": (108.9, 34.3), "辽宁": (123.4, 41.8),
        "江西": (115.9, 28.7), "重庆": (106.5, 29.5), "云南": (102.7, 25.0),
        "贵州": (106.7, 26.6), "广西": (108.3, 22.8), "山西": (112.5, 37.9),
        "内蒙古": (111.7, 40.8), "吉林": (125.3, 43.9), "黑龙江": (126.6, 45.8),
        "甘肃": (103.8, 36.1), "青海": (101.8, 36.6), "宁夏": (106.3, 38.5),
        "新疆": (87.6, 43.8), "西藏": (91.1, 29.6), "海南": (110.3, 20.0),
        "天津": (117.2, 39.1),
    }
    xs, ys, cs, sizes = [], [], [], []
    for s in scores:
        p = s["province"]
        if p in coords:
            xs.append(coords[p][0])
            ys.append(coords[p][1])
            cs.append(s["composite_score"])
            sizes.append(max(20, 150 * s["composite_score"]))
    sc = ax.scatter(xs, ys, c=cs, s=sizes, cmap="YlOrRd", edgecolors="#1a1a2e", linewidth=0.5, alpha=0.9)
    for i, s in enumerate(scores):
        if s["province"] in coords:
            ax.annotate(s["province"], (xs[i], ys[i]+0.5), fontsize=6, ha="center", color=C_TEXT, alpha=0.7)
    cbar = plt.colorbar(sc, ax=ax, shrink=0.7)
    cbar.set_label("综合得分", color=C_SUB)
    cbar.ax.yaxis.set_tick_params(color=C_SUB)
    ax.set_title("省域绿色算力承载能力空间分布 (2024)", color=C_TEXT, fontsize=13)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(OUT / "fig9-6_spatial_map.png", dpi=300)
    plt.close()
    print("✅ fig9-6")

# ================================================================
# Figure 9-7: Dynamic evolution (heatmap-style Markov)
# ================================================================
def fig9_7():
    prob = query("SELECT * FROM markov_probability")
    states = ["低水平", "中低水平", "中高水平", "高水平"]
    matrix = np.zeros((4, 4))
    for i, s in enumerate(states):
        row = next((r for r in prob if r["from_state"] == s), None)
        if row:
            matrix[i, 0] = row["to_low_level_probability"] or 0
            matrix[i, 1] = row["to_mid_low_level_probability"] or 0
            matrix[i, 2] = row["to_mid_high_level_probability"] or 0
            matrix[i, 3] = row["to_high_level_probability"] or 0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # Heatmap
    im = ax1.imshow(matrix, cmap="YlOrRd", aspect="auto", vmin=0, vmax=1)
    ax1.set_xticks(range(4))
    ax1.set_yticks(range(4))
    ax1.set_xticklabels(states, fontsize=9)
    ax1.set_yticklabels(states, fontsize=9)
    ax1.set_title("传统 Markov 转移概率矩阵", color=C_TEXT, fontsize=13)
    for i in range(4):
        for j in range(4):
            ax1.text(j, i, f"{matrix[i,j]:.2f}", ha="center", va="center", fontsize=11, fontweight="bold",
                     color="white" if matrix[i,j] > 0.5 else C_TEXT)
    cbar = plt.colorbar(im, ax=ax1, shrink=0.8)
    cbar.set_label("概率", color=C_SUB)

    # Moran trend
    moran = query("SELECT year, moran_i FROM moran_results ORDER BY year")
    years = [m["year"] for m in moran]
    vals = [m["moran_i"] for m in moran]
    ax2.fill_between(years, vals, alpha=0.2, color=C_VIOLET)
    ax2.plot(years, vals, color=C_VIOLET, linewidth=2.5, marker="s", markersize=6)
    ax2.axhline(y=0, color=C_SUB, linewidth=0.8, linestyle="--")
    ax2.set_title("全局 Moran's I 演化趋势", color=C_TEXT, fontsize=13)
    ax2.set_ylabel("Moran's I", color=C_SUB)
    ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig9-7_dynamic_evolution.png", dpi=300)
    plt.close()
    print("✅ fig9-7")

# ================================================================
# Figure 9-8: Province diagnosis (Shanghai)
# ================================================================
def fig9_8():
    shap = query("SELECT indicator_short_name, shap_value, abs_shap_value, dimension FROM shap_local_top8 WHERE province='上海' ORDER BY abs_shap_value DESC LIMIT 8")
    obs = query("SELECT * FROM obstacle_province WHERE province='上海'")
    obs = obs[0] if obs else {}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    # SHAP waterfall
    names = [s["indicator_short_name"] or s["indicator_name"] for s in shap]
    vals = [s["shap_value"] or 0 for s in shap]
    colors_bar = [C_GREEN if v >= 0 else C_RED for v in vals]
    ax1.barh(names, vals, color=colors_bar, height=0.5, alpha=0.85)
    ax1.axvline(x=0, color=C_SUB, linewidth=0.8)
    ax1.set_title("上海 SHAP 因子贡献 (Top 8)", color=C_TEXT, fontsize=13)
    ax1.set_xlabel("SHAP 值", color=C_SUB)
    ax1.invert_yaxis()
    ax1.grid(axis="x", alpha=0.3)

    # Obstacle donut
    dims = [obs.get("primary_obstacle_dimension", ""), obs.get("secondary_obstacle_dimension", "")]
    degs = [obs.get("primary_obstacle_degree", 0) or 0, obs.get("secondary_obstacle_degree", 0) or 0]
    wedges, _ = ax2.pie(degs, labels=None, colors=[C_AMBER, C_BLUE], startangle=90,
                         wedgeprops={"width": 0.35, "edgecolor": "#e2e8f0", "linewidth": 2})
    ax2.set_title("上海主要障碍因素", color=C_TEXT, fontsize=13, pad=15)
    ax2.legend(wedges, [f"{d} ({v:.1f}%)" for d, v in zip(dims, degs)],
               loc="lower center", frameon=False, labelcolor=C_SUB, fontsize=9)
    fig.suptitle("省域诊断 — 上海", fontsize=15, color=C_TEXT, y=1.02)
    fig.tight_layout()
    fig.savefig(OUT / "fig9-8_province_diagnosis.png", dpi=300)
    plt.close()
    print("✅ fig9-8")

# ================================================================
# Figure 9-9: Type identification (sorted bar)
# ================================================================
def fig9_9():
    lpa = query("SELECT province, type_name, mean_2016_2024, stage_increment FROM lpa_province_assignment ORDER BY mean_2016_2024 DESC")
    names = [p["province"] for p in lpa]
    means = [p["mean_2016_2024"] for p in lpa]
    incrs = [p["stage_increment"] for p in lpa]
    types = [p["type_name"] for p in lpa]
    type_colors = {"高位领先型": C_GREEN, "优势支撑型": C_BLUE, "中位追赶型": C_AMBER, "基础培育型": C_VIOLET}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))
    colors = [type_colors.get(t, C_SUB) for t in types]
    ax1.barh(names, means, color=colors, height=0.6, alpha=0.85)
    ax1.set_title("各省平均得分 (2016-2024, 高→低)", color=C_TEXT, fontsize=13)
    ax1.set_xlabel("平均得分", color=C_SUB)
    ax1.invert_yaxis()
    ax1.tick_params(axis="y", labelsize=7)
    ax1.grid(axis="x", alpha=0.3)
    # Legend
    from matplotlib.patches import Patch
    legend_patches = [Patch(color=c, label=t) for t, c in type_colors.items()]
    ax1.legend(handles=legend_patches, loc="lower right", frameon=False, labelcolor=C_SUB, fontsize=8)

    ax2.barh(names, incrs, color=colors, height=0.6, alpha=0.85)
    ax2.set_title("各省阶段增量 (2016→2024, 高→低)", color=C_TEXT, fontsize=13)
    ax2.set_xlabel("阶段增量", color=C_SUB)
    ax2.invert_yaxis()
    ax2.tick_params(axis="y", labelsize=7)
    ax2.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "fig9-9_type_identification.png", dpi=300)
    plt.close()
    print("✅ fig9-9")

# ================================================================
# Figure 9-10: SHAP (Shanghai default)
# ================================================================
def fig9_10():
    shap = query("SELECT indicator_short_name, shap_value, abs_shap_value, dimension FROM shap_local_top8 WHERE province='上海' ORDER BY abs_shap_value DESC LIMIT 10")
    names = [s["indicator_short_name"] or s["indicator_name"] for s in shap]
    values = [s["shap_value"] or 0 for s in shap]
    dims = [s["dimension"] for s in shap]

    fig, ax = plt.subplots(figsize=(10, 7))
    colors = [C_GREEN if v >= 0 else C_RED for v in values]
    bars = ax.barh(range(len(names)), [abs(v) for v in values], left=[min(0, v) for v in values],
                   color=colors, height=0.5, alpha=0.85, edgecolor="#e2e8f0", linewidth=0.5)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.axvline(x=0, color=C_SUB, linewidth=0.8)
    ax.set_xlabel("SHAP 值 (绿色=正向, 红色=负向)", color=C_SUB)
    ax.set_title("上海 SHAP 特征贡献分析 (2024)", color=C_TEXT, fontsize=14)
    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.3)
    for i, (n, v, d) in enumerate(zip(names, values, dims)):
        side = 0.002 if v >= 0 else -0.002
        ax.text(v + side, i, f"{d}", va="center", fontsize=7, color=C_SUB, ha="left" if v >= 0 else "right")
    fig.tight_layout()
    fig.savefig(OUT / "fig9-10_shap.png", dpi=300)
    plt.close()
    print("✅ fig9-10")

# ================================================================
# Figure 9-11: Layout (Shanghai)
# ================================================================
def fig9_11():
    layout = query("SELECT * FROM layout_province_decision WHERE province='上海'")
    if not layout:
        print("⚠️  No Shanghai layout data")
        return
    d = layout[0]

    fig, axes = plt.subplots(1, 3, figsize=(14, 5))
    # Gauge-like bars
    indices = [
        ("需求网络\n优势", d.get("demand_network_advantage_index") or 0, C_BLUE),
        ("能源低碳\n优势", d.get("energy_low_carbon_advantage_index") or 0, C_GREEN),
        ("综合\n适宜度", d.get("suitability_index") or 0, C_AMBER),
    ]
    for ax, (label, val, color) in zip(axes, indices):
        ax.barh([label], [val], color=color, height=0.4, alpha=0.85)
        ax.set_xlim(0, max(1.0, val * 1.2))
        ax.text(val + 0.02, 0, f"{val:.3f}", va="center", fontsize=11, color=C_TEXT, fontweight="bold")
        ax.set_title(label.strip(), color=C_SUB, fontsize=10)
        ax.grid(axis="x", alpha=0.2)
        ax.set_xticklabels([])

    fig.suptitle(f"上海布局决策 — {d.get('recommended_layout_type', '')} | {d.get('layout_orientation', '')}",
                 fontsize=14, color=C_TEXT, y=1.04)
    fig.tight_layout()
    fig.savefig(OUT / "fig9-11_layout.png", dpi=300)
    plt.close()
    print("✅ fig9-11")

# ================================================================
# Run all
# ================================================================
if __name__ == "__main__":
    print(f"Generating figures to {OUT}...")
    fig9_3()
    fig9_4()
    fig9_5()
    fig9_6()
    fig9_7()
    fig9_8()
    fig9_9()
    fig9_10()
    fig9_11()
    print(f"\n✅ All figures saved to {OUT}")
