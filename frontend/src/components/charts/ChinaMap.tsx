"use client";

import { useEffect, useState, useRef } from "react";
import ReactEChartsCore from "echarts-for-react/lib/core";
import * as echarts from "echarts/core";
import { MapChart } from "echarts/charts";
import { TooltipComponent, VisualMapComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";
import type { EChartsCoreOption } from "echarts/core";

echarts.use([MapChart, TooltipComponent, VisualMapComponent, CanvasRenderer]);

interface Props {
  data: { name: string; value: number; rank?: number; region?: string; typeName?: string }[];
  title?: string;
  height?: number;
}

let geoJsonCache: unknown = null;

// Map DB short names -> GeoJSON full names
const NAME_MAP: Record<string, string> = {
  "北京": "北京市", "天津": "天津市", "上海": "上海市", "重庆": "重庆市",
  "河北": "河北省", "山西": "山西省", "内蒙古": "内蒙古自治区",
  "辽宁": "辽宁省", "吉林": "吉林省", "黑龙江": "黑龙江省",
  "江苏": "江苏省", "浙江": "浙江省", "安徽": "安徽省",
  "福建": "福建省", "江西": "江西省", "山东": "山东省",
  "河南": "河南省", "湖北": "湖北省", "湖南": "湖南省",
  "广东": "广东省", "广西": "广西壮族自治区", "海南": "海南省",
  "四川": "四川省", "贵州": "贵州省", "云南": "云南省",
  "西藏": "西藏自治区", "陕西": "陕西省", "甘肃": "甘肃省",
  "青海": "青海省", "宁夏": "宁夏回族自治区", "新疆": "新疆维吾尔自治区",
};

export default function ChinaMap({ data, title, height = 550 }: Props) {
  const [geoReady, setGeoReady] = useState(false);
  const [geoError, setGeoError] = useState(false);
  const chartRef = useRef<ReactEChartsCore>(null);

  useEffect(() => {
    if (geoReady || geoError) return;

    (async () => {
      try {
        if (!geoJsonCache) {
          const resp = await fetch("/china.json");
          if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
          geoJsonCache = await resp.json();
        }
        echarts.registerMap("china", geoJsonCache as never);
        setGeoReady(true);
      } catch {
        setGeoError(true);
      }
    })();
  }, [geoReady, geoError]);

  // Loading state
  if (!geoReady && !geoError) {
    return (
      <div className="bg-dark-card rounded-xl border border-dark-lighter flex items-center justify-center" style={{ height }}>
        <div className="text-center">
          <div className="w-6 h-6 border-2 border-primary/30 border-t-primary rounded-full animate-spin mx-auto mb-2" />
          <span className="text-slate-500 text-sm">加载地图数据...</span>
        </div>
      </div>
    );
  }

  // Error state
  if (geoError) {
    return (
      <div className="bg-dark-card rounded-xl border border-dark-lighter flex items-center justify-center" style={{ height }}>
        <div className="text-center">
          <span className="text-3xl mb-2 block">🗺️</span>
          <span className="text-slate-400 text-sm">地图数据加载失败</span>
          <p className="text-slate-600 text-xs mt-1">请检查网络连接后刷新页面</p>
        </div>
      </div>
    );
  }

  const maxVal = Math.max(...data.map((d) => d.value), 0.01);

  const option: EChartsCoreOption = {
    title: title ? { text: title, left: "center", top: 5, textStyle: { color: "#e2e8f0", fontSize: 14 } } : undefined,
    tooltip: {
      trigger: "item",
      backgroundColor: "rgba(15,23,42,0.95)",
      borderColor: "#334155",
      textStyle: { color: "#e2e8f0", fontSize: 12 },
      formatter: (p: unknown) => {
        const item = p as { name: string; data?: Record<string, unknown> };
        if (!item.data || (item.data as Record<string, unknown>).value === undefined) return item.name;
        const d = item.data as Record<string, unknown>;
        const v = d.value as number;
        const rk = d.rank as number ?? "-";
        const tp = d.typeName as string ?? "";
        return `<b>${item.name}</b><br/>🏆 得分：<b>${v.toFixed(4)}</b><br/>📊 排名：#${rk}${tp ? `<br/>🏷️ 类型：${tp}` : ""}`;
      },
    },
    visualMap: {
      min: 0.25,
      max: maxVal,
      left: "left",
      bottom: 20,
      text: ["高", "低"],
      textStyle: { color: "#94a3b8" },
      inRange: { color: ["#1e3a5f", "#0e5a8a", "#0ea5e9", "#10b981", "#f59e0b"] },
      calculable: true,
    },
    series: [{
      type: "map",
      map: "china",
      roam: true,
      zoom: 1.2,
      center: [105, 36],
      data: data.map((d) => ({ name: NAME_MAP[d.name] || d.name, value: d.value, rank: d.rank, typeName: d.typeName })),
      label: { show: false },
      emphasis: {
        label: { show: true, color: "#fff", fontSize: 13 },
        itemStyle: { areaColor: "#fbbf24", shadowBlur: 20, shadowColor: "rgba(245,158,11,0.5)" },
      },
      itemStyle: {
        areaColor: "#1e293b",
        borderColor: "#475569",
        borderWidth: 1,
      },
    }],
  };

  return (
    <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
      <ReactEChartsCore
        ref={chartRef}
        echarts={echarts}
        option={option}
        style={{ height }}
        notMerge
        lazyUpdate
      />
    </div>
  );
}
