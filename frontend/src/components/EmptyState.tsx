export default function EmptyState({ text = "暂无数据" }: { text?: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-3">
      <span className="text-4xl">📭</span>
      <p className="text-sm text-slate-500">{text}</p>
    </div>
  );
}
