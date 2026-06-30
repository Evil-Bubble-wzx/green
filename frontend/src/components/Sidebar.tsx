"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const NAV_GROUPS = [
  {
    label: "总览",
    items: [
      { href: "/dashboard", label: "首页总览", icon: "📊" },
    ],
  },
  {
    label: "评价分析",
    items: [
      { href: "/evaluation", label: "综合评价", icon: "🏆" },
      { href: "/regional-difference", label: "区域差异", icon: "📈" },
      { href: "/spatial-cluster", label: "空间集聚", icon: "📍" },
      { href: "/dynamic-evolution", label: "动态演化", icon: "🔄" },
    ],
  },
  {
    label: "诊断决策",
    items: [
      { href: "/province-diagnosis", label: "省域诊断", icon: "🔍" },
      { href: "/type-identification", label: "类型识别", icon: "🏷️" },
      { href: "/shap", label: "SHAP 解释", icon: "🧠" },
      { href: "/layout-decision", label: "布局决策", icon: "🗺️" },
    ],
  },
  {
    label: "智能",
    items: [
      { href: "/chat", label: "智能问答", icon: "💬" },
    ],
  },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-56 bg-dark-card border-r border-dark-lighter flex-shrink-0 flex flex-col overflow-y-auto">
      <div className="h-14 flex items-center gap-3 px-5 border-b border-dark-lighter flex-shrink-0">
        <span className="text-xl">🌿</span>
        <span className="font-bold text-sm text-primary-light leading-tight">
          绿色算力决策平台
        </span>
      </div>

      <nav className="flex-1 py-3 px-3 space-y-4 overflow-y-auto">
        {NAV_GROUPS.map((group) => (
          <div key={group.label}>
            <p className="px-3 mb-1 text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
              {group.label}
            </p>
            <div className="space-y-0.5">
              {group.items.map((item) => {
                const active = pathname === item.href || pathname.startsWith(item.href + "/");
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                      active
                        ? "bg-primary/15 text-primary-light font-semibold"
                        : "text-slate-400 hover:bg-dark-lighter hover:text-white"
                    }`}
                  >
                    <span className="text-base w-5 text-center">{item.icon}</span>
                    <span className="truncate">{item.label}</span>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </nav>

      <div className="px-5 py-3 border-t border-dark-lighter text-xs text-slate-500 flex-shrink-0">
        Green Compute v1.0 · 公开版
      </div>
    </aside>
  );
}
