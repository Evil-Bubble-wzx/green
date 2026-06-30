"use client";
import ReactECharts from "echarts-for-react";

interface Series {
  name: string;
  data: number[];
  color: string;
}

interface Props {
  categories: string[];
  series: Series[];
  title?: string;
  height?: number;
}

export default function StackedBar({ categories, series, title, height = 380 }: Props) {
  const option = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "axis" as const,
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
      formatter: (params: { seriesName: string; value: number; percent?: number }[]) => {
        let html = `<b>${params[0].value !== undefined ? params[0].value?.toFixed?.(1) : ""}</b><br/>`;
        params.forEach((p) => { html += `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:4px;background:${(p as unknown as { color: string }).color || "#fff"}"></span>${p.seriesName}: ${p.value?.toFixed?.(1)}%<br/>`; });
        return html;
      },
    },
    legend: { bottom: 0, textStyle: { color: "#94a3b8", fontSize: 11 }, itemGap: 20 },
    grid: { left: 50, right: 30, top: title ? 40 : 15, bottom: 40 },
    xAxis: { type: "category", data: categories, axisLabel: { color: "#94a3b8", fontSize: 11 } },
    yAxis: { type: "value", min: 0, max: 100, axisLabel: { color: "#94a3b8", formatter: "{value}%" }, splitLine: { lineStyle: { color: "#1e293b" } } },
    series: series.map((s) => ({
      name: s.name,
      type: "bar",
      stack: "total",
      data: s.data,
      itemStyle: { color: s.color, borderRadius: 0 },
      emphasis: { focus: "series" as const },
      barWidth: "50%",
      label: {
        show: s.name === series[series.length - 1]?.name,
        position: "top" as const,
        color: "#94a3b8",
        fontSize: 10,
        formatter: (p: { value: number }) => (p.value > 5 ? p.value.toFixed(0) + "%" : ""),
      },
    })),
    animationEasing: "cubicOut" as const,
  };

  return <div className="bg-dark-card rounded-xl border border-dark-lighter p-4"><ReactECharts option={option} style={{ height }} /></div>;
}
