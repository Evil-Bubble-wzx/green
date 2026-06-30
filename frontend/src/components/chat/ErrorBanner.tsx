"use client";

interface Props {
  message: string;
  onRetry?: () => void;
  onDismiss?: () => void;
}

export default function ErrorBanner({ message, onRetry, onDismiss }: Props) {
  return (
    <div className="flex items-start gap-3 mx-4 my-3 px-4 py-3 bg-red-500/10 border border-red-500/20 rounded-xl">
      <span className="text-lg flex-shrink-0">⚠️</span>
      <div className="flex-1 min-w-0">
        <p className="text-sm text-red-300">{message}</p>
        <p className="text-xs text-slate-500 mt-1">
          请检查后端服务是否正常运行，或启用 Mock 模式进行演示。
        </p>
      </div>
      <div className="flex items-center gap-2 flex-shrink-0">
        {onRetry && (
          <button
            onClick={onRetry}
            className="px-3 py-1 text-xs bg-red-500/20 hover:bg-red-500/30 text-red-300
                       rounded-lg transition-colors"
          >
            重试
          </button>
        )}
        {onDismiss && (
          <button
            onClick={onDismiss}
            className="px-2 py-1 text-xs text-slate-500 hover:text-slate-300 transition-colors"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
