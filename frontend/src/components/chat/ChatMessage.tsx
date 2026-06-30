"use client";

export interface ChatMessageData {
  role: "user" | "assistant";
  content: string;
  category?: string;
  toolCalls?: string[];
  ragSources?: string[];
}

const CATEGORY_LABELS: Record<string, string> = {
  concept_explanation: "概念解释",
  data_query: "数据查询",
  province_diagnosis: "省域诊断",
  layout_recommendation: "布局建议",
  future_prediction: "未来预测",
  unsupported: "暂不支持",
};

const CATEGORY_COLORS: Record<string, string> = {
  concept_explanation: "bg-blue-500/15 text-blue-400",
  data_query: "bg-emerald-500/15 text-emerald-400",
  province_diagnosis: "bg-amber-500/15 text-amber-400",
  layout_recommendation: "bg-violet-500/15 text-violet-400",
  future_prediction: "bg-rose-500/15 text-rose-400",
  unsupported: "bg-slate-500/15 text-slate-400",
};

interface Props {
  message: ChatMessageData;
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[88%] sm:max-w-[80%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-primary/15 border border-primary/20 text-white rounded-br-md"
            : "bg-dark-lighter border border-dark-lighter/50 text-slate-200 rounded-bl-md"
        }`}
      >
        {/* Metadata bar (assistant only) */}
        {!isUser && message.category && (
          <div className="flex flex-wrap items-center gap-1.5 mb-2">
            <span
              className={`inline-block px-2 py-0.5 rounded-md text-[11px] font-medium ${
                CATEGORY_COLORS[message.category] || "bg-slate-500/15 text-slate-400"
              }`}
            >
              {CATEGORY_LABELS[message.category] || message.category}
            </span>
            {message.toolCalls && message.toolCalls.length > 0 && (
              <span className="text-[11px] text-slate-500">
                {message.toolCalls.slice(0, 3).join(" · ")}
                {message.toolCalls.length > 3 && ` +${message.toolCalls.length - 3}`}
              </span>
            )}
            {message.ragSources && message.ragSources.length > 0 && (
              <span className="text-[11px] text-slate-600" title={message.ragSources.join(", ")}>
                📚 {message.ragSources.length} 篇文档
              </span>
            )}
          </div>
        )}

        {/* Content with basic markdown rendering */}
        <div className="text-sm leading-relaxed prose-sm prose-invert max-w-none">
          <MarkdownContent content={message.content} />
        </div>
      </div>
    </div>
  );
}

/**
 * Simple markdown renderer: handles ##, **, ``, tables, and newlines.
 */
function MarkdownContent({ content }: { content: string }) {
  const lines = content.split("\n");
  const elements: React.ReactNode[] = [];

  let inTable = false;
  let tableRows: string[][] = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Table detection
    if (line.startsWith("|") && line.endsWith("|")) {
      if (!inTable) {
        inTable = true;
        tableRows = [];
      }
      const cells = line.split("|").slice(1, -1).map((c) => c.trim());
      // Skip separator rows like |---|---|
      if (!cells.every((c) => /^[-:]+$/.test(c))) {
        tableRows.push(cells);
      }
      // If next line isn't a table row or we're at the end, render the table
      const nextLine = i + 1 < lines.length ? lines[i + 1] : "";
      if (!nextLine.startsWith("|") || i === lines.length - 1) {
        elements.push(
          <div key={`tbl-${i}`} className="overflow-x-auto my-2">
            <table className="min-w-full text-xs border-collapse">
              <tbody>
                {tableRows.map((row, ri) => (
                  <tr
                    key={ri}
                    className={ri === 0 ? "border-b border-dark-lighter font-semibold text-slate-300" : "border-b border-dark/40"}
                  >
                    {row.map((cell, ci) => (
                      <td key={ci} className="px-2 py-1 whitespace-nowrap">
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        inTable = false;
        tableRows = [];
      }
      continue;
    }

    // Headings
    if (line.startsWith("## ")) {
      elements.push(
        <h3 key={i} className="text-base font-semibold text-white mt-3 mb-1">
          {line.slice(3)}
        </h3>
      );
      continue;
    }
    if (line.startsWith("### ")) {
      elements.push(
        <h4 key={i} className="text-sm font-semibold text-slate-200 mt-2 mb-1">
          {line.slice(4)}
        </h4>
      );
      continue;
    }

    // Code block
    if (line.startsWith("```")) {
      const codeLines: string[] = [];
      i++;
      while (i < lines.length && !lines[i].startsWith("```")) {
        codeLines.push(lines[i]);
        i++;
      }
      elements.push(
        <pre key={i} className="bg-dark/50 rounded-lg p-3 my-2 overflow-x-auto text-xs text-slate-300 font-mono">
          {codeLines.join("\n")}
        </pre>
      );
      continue;
    }

    // Bold
    let processed = line.replace(/\*\*(.*?)\*\*/g, (_: string, text: string) => {
      return `<strong class="font-semibold text-white">${text}</strong>`;
    });

    // Inline code
    processed = processed.replace(/`([^`]+)`/g, (_: string, text: string) => {
      return `<code class="bg-dark/60 px-1 py-0.5 rounded text-xs font-mono text-primary-light">${text}</code>`;
    });

    // Blockquote
    if (line.startsWith("> ")) {
      elements.push(
        <blockquote key={i} className="border-l-3 border-primary/30 pl-3 my-1 text-xs text-slate-400 italic">
          <span dangerouslySetInnerHTML={{ __html: line.slice(2) }} />
        </blockquote>
      );
      continue;
    }

    // Empty line
    if (!line.trim()) {
      elements.push(<div key={i} className="h-2" />);
      continue;
    }

    // Regular paragraph
    elements.push(
      <p key={i} className="my-1">
        <span dangerouslySetInnerHTML={{ __html: processed }} />
      </p>
    );
  }

  return <>{elements}</>;
}
