"use client";

interface Question {
  label: string;
  text: string;
}

const QUESTIONS: Question[] = [
  { label: "概念解释", text: "绿色算力承载能力指数是什么？" },
  { label: "数据查询", text: "2024 年排名前十的省份有哪些？" },
  { label: "省域诊断", text: "贵州的发展短板是什么？" },
  { label: "布局建议", text: "贵州和内蒙古哪个更适合未来布局？" },
  { label: "未来预测", text: "未来十年哪些省份表现可能更好？" },
];

interface Props {
  onSelect: (question: string) => void;
  loading?: boolean;
}

export default function SuggestedQuestions({ onSelect, loading }: Props) {
  return (
    <div className="flex flex-wrap justify-center gap-2">
      {QUESTIONS.map((q) => (
        <button
          key={q.text}
          onClick={() => onSelect(q.text)}
          disabled={loading}
          className="group px-3 py-1.5 text-xs bg-dark-lighter/80 hover:bg-primary/15
                     text-slate-400 hover:text-primary-light rounded-full
                     border border-dark-lighter hover:border-primary/30
                     transition-all disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span className="text-[10px] text-slate-600 group-hover:text-primary/60 mr-1">
            [{q.label}]
          </span>
          {q.text}
        </button>
      ))}
    </div>
  );
}
