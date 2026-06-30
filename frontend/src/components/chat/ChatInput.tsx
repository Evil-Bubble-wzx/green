"use client";

interface Props {
  value: string;
  onChange: (v: string) => void;
  onSend: () => void;
  loading: boolean;
  placeholder?: string;
}

export default function ChatInput({ value, onChange, onSend, loading, placeholder }: Props) {
  return (
    <div className="border-t border-dark-lighter px-3 sm:px-4 py-3 bg-dark-card">
      <div className="flex gap-2 max-w-3xl mx-auto">
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
          placeholder={placeholder || "输入问题，按 Enter 发送，Shift+Enter 换行"}
          disabled={loading}
          className="flex-1 min-w-0 bg-dark border border-dark-lighter rounded-xl px-4 py-2.5 text-sm
                     text-white placeholder:text-slate-500
                     focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-transparent
                     disabled:opacity-50 transition-colors"
        />
        <button
          onClick={onSend}
          disabled={loading || !value.trim()}
          className="flex-shrink-0 px-4 sm:px-6 py-2.5 bg-primary hover:bg-primary-dark text-white
                     text-sm font-medium rounded-xl transition-colors
                     disabled:opacity-40 disabled:cursor-not-allowed
                     active:scale-95"
        >
          {loading ? (
            <span className="flex items-center gap-1.5">
              <span className="w-3.5 h-3.5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span className="hidden sm:inline">分析中</span>
            </span>
          ) : (
            <span className="flex items-center gap-1">
              <span>发送</span>
              <span className="hidden sm:inline text-xs opacity-60">⏎</span>
            </span>
          )}
        </button>
      </div>
      <p className="text-[11px] text-slate-600 mt-2 text-center max-w-3xl mx-auto">
        数据粒度：省级行政区 · 基于 TOPSIS + LPA + SHAP + 障碍度模型
      </p>
    </div>
  );
}
