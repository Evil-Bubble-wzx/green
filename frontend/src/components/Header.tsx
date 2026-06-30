"use client";

export default function Header() {
  return (
    <header className="h-14 bg-dark-card border-b border-dark-lighter flex items-center justify-between px-6 flex-shrink-0">
      <h1 className="text-base font-semibold text-slate-200">
        省域绿色算力承载能力评估与资源布局决策支持系统
      </h1>
      <div className="flex items-center gap-3 text-xs text-slate-400">
        <span className="px-2 py-1 rounded bg-dark-lighter">2016–2024</span>
        <span className="px-2 py-1 rounded bg-dark-lighter">31 省份</span>
        <span className="px-2 py-1 rounded bg-accent/15 text-accent">数据就绪</span>
      </div>
    </header>
  );
}
