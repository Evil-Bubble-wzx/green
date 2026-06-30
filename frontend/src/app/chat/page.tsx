"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import PageContainer from "@/components/PageContainer";
import ChatMessage, { type ChatMessageData } from "@/components/chat/ChatMessage";
import ChatInput from "@/components/chat/ChatInput";
import SuggestedQuestions from "@/components/chat/SuggestedQuestions";
import ErrorBanner from "@/components/chat/ErrorBanner";
import DataSourceCard from "@/components/chat/DataSourceCard";
import { sendChat } from "@/lib/api/chat";

type PageState = "welcome" | "loading" | "ready" | "error";

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessageData[]>([]);
  const [input, setInput] = useState("");
  const [pageState, setPageState] = useState<PageState>("welcome");
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [lastDataSource, setLastDataSource] = useState<{
    category: string;
    toolCalls: string[];
    ragSources: string[];
  } | null>(null);

  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    const el = scrollRef.current;
    if (el) {
      el.scrollTo({ top: el.scrollHeight, behavior: "smooth" });
    }
  }, [messages, pageState]);

  // Determine if mock mode
  const isMock = process.env.NEXT_PUBLIC_USE_MOCK === "true";
  const isLoading = pageState === "loading";

  const send = useCallback(
    async (question?: string) => {
      const q = (question || input).trim();
      if (!q || pageState === "loading") return;

      // Add user message
      const userMsg: ChatMessageData = { role: "user", content: q };
      setMessages((prev) => [...prev, userMsg]);
      setInput("");
      setPageState("loading");
      setErrorMsg(null);
      setLastDataSource(null);

      try {
        const resp = await sendChat(q);
        const assistantMsg: ChatMessageData = {
          role: "assistant",
          content: resp.answer,
          category: resp.category,
          toolCalls: resp.toolCalls,
          ragSources: resp.ragSources,
        };
        setMessages((prev) => [...prev, assistantMsg]);
        setLastDataSource({
          category: resp.category,
          toolCalls: resp.toolCalls,
          ragSources: resp.ragSources,
        });
        setPageState("ready");
      } catch (e: unknown) {
        const msg = e instanceof Error ? e.message : "服务暂时不可用，请稍后重试。";
        setErrorMsg(msg);
        setPageState("error");
      }
    },
    [input, pageState]
  );

  const dismissError = () => {
    setErrorMsg(null);
    if (messages.length > 0) {
      setPageState("ready");
    } else {
      setPageState("welcome");
    }
  };

  const retryLast = () => {
    // Remove last user message and retry
    if (messages.length > 0) {
      const lastUser = [...messages].reverse().find((m) => m.role === "user");
      if (lastUser) {
        setMessages((prev) => prev.slice(0, -1)); // remove error assistant message
        setErrorMsg(null);
        send(lastUser.content);
      }
    }
  };

  return (
    <PageContainer
      title="智能问答"
      subtitle={isMock ? "演示模式 · 使用预设回答" : "基于 RAG 和数据库的自然语言查询"}
    >
      <div className="flex flex-col lg:flex-row gap-4 h-[calc(100vh-180px)] max-h-[900px]">
        {/* ---- Main chat column ---- */}
        <div className="flex-1 flex flex-col min-w-0 bg-dark-card rounded-xl border border-dark-lighter overflow-hidden">
          {/* Messages area */}
          <div ref={scrollRef} className="flex-1 overflow-auto">
            {/* Welcome state */}
            {pageState === "welcome" && messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full px-4 py-12">
                <div className="text-5xl mb-4">🤖</div>
                <h3 className="text-lg font-semibold text-white mb-2">
                  {isMock ? "智能问答（演示模式）" : "智能问答"}
                </h3>
                <p className="text-sm text-slate-400 mb-8 text-center max-w-md">
                  {isMock
                    ? "当前为演示模式，使用预设回答展示系统功能。设置 NEXT_PUBLIC_USE_MOCK=false 连接真实后端。"
                    : "向 AI 助手提问，获取绿色算力承载能力的智能分析"}
                </p>
                <SuggestedQuestions onSelect={send} loading={isLoading} />
              </div>
            )}

            {/* Messages */}
            {messages.map((msg, i) => (
              <div key={i} className="px-4 first:mt-3">
                <ChatMessage message={msg} />
                {/* Show data source card after the last assistant message */}
                {i === messages.length - 1 && msg.role === "assistant" && lastDataSource && (
                  <DataSourceCard
                    category={lastDataSource.category}
                    toolCalls={lastDataSource.toolCalls}
                    ragSources={lastDataSource.ragSources}
                  />
                )}
              </div>
            ))}

            {/* Loading indicator */}
            {isLoading && (
              <div className="flex justify-start px-4 py-3">
                <div className="bg-dark-lighter rounded-2xl rounded-bl-md px-5 py-3 flex items-center gap-2">
                  <div className="flex gap-1">
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                    <span className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                  </div>
                  <span className="text-sm text-slate-400 ml-2">正在分析</span>
                </div>
              </div>
            )}

            {/* Error banner */}
            {errorMsg && (
              <ErrorBanner message={errorMsg} onRetry={retryLast} onDismiss={dismissError} />
            )}
          </div>

          {/* Input area */}
          <ChatInput
            value={input}
            onChange={setInput}
            onSend={() => send()}
            loading={isLoading}
          />
        </div>

        {/* ---- Right info panel (desktop only) ---- */}
        <aside className="hidden lg:flex lg:w-60 flex-shrink-0 flex-col gap-3">
          {/* What you can ask */}
          <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
            <h3 className="text-sm font-semibold text-slate-300 mb-3">💡 可以问什么</h3>
            <div className="space-y-2.5">
              {[
                { cat: "概念解释", color: "text-blue-400", desc: "绿色算力指数、TOPSIS 模型原理" },
                { cat: "数据查询", color: "text-emerald-400", desc: "排名、得分、趋势数据" },
                { cat: "省域诊断", color: "text-amber-400", desc: "短板分析、障碍因素、LPA 类型" },
                { cat: "布局建议", color: "text-violet-400", desc: "布局对比、选址建议" },
                { cat: "未来预测", color: "text-rose-400", desc: "未来十年潜力排名" },
              ].map((item) => (
                <div key={item.cat} className="text-xs">
                  <span className={`font-medium ${item.color}`}>{item.cat}</span>
                  <p className="text-slate-500 mt-0.5">{item.desc}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Data policy */}
          <div className="bg-dark-card rounded-xl border border-dark-lighter p-4">
            <h3 className="text-sm font-semibold text-slate-300 mb-2">⚠️ 数据说明</h3>
            <p className="text-xs text-slate-500 leading-relaxed">
              数据粒度：<strong className="text-slate-300">省级行政区</strong>
              <br />
              时间范围：2016–2024 年
              <br />
              覆盖范围：31 个省份
              <br />
              不支持城市级查询
            </p>
          </div>

          {/* Mock mode badge */}
          {isMock && (
            <div className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4">
              <h3 className="text-sm font-semibold text-amber-400 mb-1">🎭 演示模式</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                使用预设回答进行演示。设置环境变量
                <code className="text-amber-300/80 text-[11px] mx-0.5">NEXT_PUBLIC_USE_MOCK=false</code>
                连接真实后端。
              </p>
            </div>
          )}
        </aside>

        {/* Mock badge for mobile */}
        {isMock && (
          <div className="lg:hidden fixed bottom-20 right-4 z-50">
            <span className="px-2.5 py-1 text-[11px] bg-amber-500/20 text-amber-400 rounded-full border border-amber-500/30">
              🎭 演示
            </span>
          </div>
        )}
      </div>
    </PageContainer>
  );
}
