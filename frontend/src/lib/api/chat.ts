/**
 * Chat API client.
 *
 * When NEXT_PUBLIC_USE_MOCK=true, returns mock responses without calling the backend.
 * When false, calls the real POST /api/chat endpoint.
 */

import { getMockResponse, mockDelay } from "@/lib/mock/chatMock";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface ChatResponse {
  answer: string;
  category: string;
  toolCalls: string[];
  ragSources: string[];
}

// ---------------------------------------------------------------------------
// User-facing error messages (never expose backend internals)
// ---------------------------------------------------------------------------

const USER_FRIENDLY_ERRORS: Record<string, string> = {
  "DEEPSEEK_API_KEY": "AI 模型服务暂未配置，请联系管理员。",
  "DATABASE_URL": "数据库连接未配置，请联系管理员。",
  "connection refused": "后端服务暂时不可用，请稍后重试。",
  "Internal Server Error": "服务暂时异常，请稍后重试。",
  "Failed to fetch": "无法连接到后端服务，请检查网络连接。",
  "NetworkError": "网络连接失败，请检查网络后重试。",
  "timeout": "请求超时，请稍后重试。",
  "RAG": "知识库检索暂时不可用。",
};

function sanitizeError(raw: string): string {
  for (const [key, msg] of Object.entries(USER_FRIENDLY_ERRORS)) {
    if (raw.includes(key)) return msg;
  }
  // Generic fallback — never expose raw error
  return "服务暂时不可用，请稍后重试。";
}

// ---------------------------------------------------------------------------
// API call
// ---------------------------------------------------------------------------

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL || undefined;

function apiUrl(path: string): string {
  return BASE ? `${BASE}${path}` : path;
}

export async function sendChat(question: string): Promise<ChatResponse> {
  // --- Mock mode ---
  if (process.env.NEXT_PUBLIC_USE_MOCK === "true") {
    await mockDelay();
    return getMockResponse(question);
  }

  // --- Real API (with retry) ---
  let lastError: Error | null = null;
  for (let attempt = 0; attempt < 3; attempt++) {
    try {
      if (attempt > 0) {
        await new Promise((r) => setTimeout(r, 1000 * attempt)); // backoff
      }
      const res = await fetch(apiUrl("/api/chat"), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
        signal: AbortSignal.timeout(45000),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        const detail = (body as { detail?: string }).detail || res.statusText;
        // 400 errors (relevance, validation) should NOT be retried
        if (res.status === 400) {
          throw new Error(sanitizeError(detail));
        }
        // 429, 500, 502, 503 — retry
        lastError = new Error(sanitizeError(detail));
        continue;
      }

      const data = await res.json();
      return {
        answer: data.answer || "",
        category: data.category || "",
        toolCalls: data.tool_calls || [],
        ragSources: data.rag_sources || [],
      };
    } catch (e: unknown) {
      if (e instanceof DOMException && e.name === "TimeoutError") {
        lastError = new Error(sanitizeError("timeout"));
        continue;
      }
      if (e instanceof TypeError && e.message.includes("fetch")) {
        lastError = new Error(sanitizeError("Failed to fetch"));
        continue;
      }
      // Don't retry 400 errors
      if (e instanceof Error && e.message.includes("请提出")) {
        throw e;
      }
      lastError = e instanceof Error ? e : new Error("Unknown error");
      if (attempt < 2) continue;
    }
  }
  throw lastError || new Error(sanitizeError("Failed to fetch"));
}
