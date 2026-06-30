"use client";

interface Props {
  provinces: string[];
  value: string;
  onChange: (province: string) => void;
  loading?: boolean;
}

export default function ProvinceSelector({ provinces, value, onChange, loading }: Props) {
  return (
    <div className="flex items-center gap-2">
      <label className="text-sm text-slate-400 whitespace-nowrap">选择省份：</label>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={loading}
        className="bg-dark-card border border-dark-lighter rounded-lg px-3 py-2 text-sm text-white
                   focus:outline-none focus:ring-2 focus:ring-primary/50 disabled:opacity-50"
      >
        <option value="">-- 请选择 --</option>
        {provinces.map((p) => (
          <option key={p} value={p}>
            {p}
          </option>
        ))}
      </select>
    </div>
  );
}
