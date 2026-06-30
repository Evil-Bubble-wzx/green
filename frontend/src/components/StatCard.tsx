interface Props {
  label: string;
  value: string | number;
  sub?: string;
  color?: "blue" | "green" | "amber" | "red";
}

const COLORS = {
  blue: "border-l-primary bg-primary/5",
  green: "border-l-accent bg-accent/5",
  amber: "border-l-warning bg-warning/5",
  red: "border-l-danger bg-danger/5",
};

export default function StatCard({ label, value, sub, color = "blue" }: Props) {
  return (
    <div className={`border-l-4 rounded-lg px-4 py-3 ${COLORS[color]}`}>
      <p className="text-xs text-slate-400 mb-1">{label}</p>
      <p className="text-2xl font-bold text-white">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-0.5">{sub}</p>}
    </div>
  );
}
