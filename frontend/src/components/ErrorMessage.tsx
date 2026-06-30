"use client";

interface Props {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: Props) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-4">
      <span className="text-4xl">⚠️</span>
      <p className="text-slate-300 text-sm max-w-md text-center">{message}</p>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-primary/20 text-primary-light rounded-lg text-sm
                     hover:bg-primary/30 transition-colors"
        >
          重试
        </button>
      )}
    </div>
  );
}
