"""
Chat Service — orchestrates RAG retrieval, tool calling, and DeepSeek LLM.

Flow:
  1. Classify the user question into a category.
  2. Retrieve relevant RAG documents.
  3. Call database tools based on category + question.
  4. Build the final prompt with all context.
  5. Generate the final answer via DeepSeek API.
"""

import os
import json
import re
import asyncio
import logging
from pathlib import Path
from typing import Optional

import requests

from .prompts import ROUTER_SYSTEM_PROMPT, CHAT_SYSTEM_PROMPT, build_context
from .tools import (
    get_latest_scores,
    get_province_score,
    get_province_trend,
    get_top_rankings,
    get_lpa_result,
    get_obstacle_result,
    get_shap_top_features,
    get_layout_recommendation,
    compare_provinces,
    get_future_potential_ranking,
)
from ..rag.retriever import get_retriever

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# DeepSeek API
# ---------------------------------------------------------------------------

DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


def _get_deepseek_key() -> str:
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        # Also try loading from .env
        from dotenv import load_dotenv
        project_root = Path(__file__).resolve().parent.parent.parent
        load_dotenv(project_root / ".env")
        key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("DEEPSEEK_API_KEY not set in .env")
    return key


async def _call_llm(system_prompt: str, user_message: str, temperature: float = 0.3) -> str:
    """Call DeepSeek Chat API (non-blocking, runs in thread pool)."""
    def _sync_call():
        api_key = _get_deepseek_key()
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": temperature,
            "max_tokens": 2048,
        }
        resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=60)
        if resp.status_code != 200:
            raise RuntimeError(f"DeepSeek API error ({resp.status_code}): {resp.text[:500]}")
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    return await asyncio.to_thread(_sync_call)


# ---------------------------------------------------------------------------
# Question Router
# ---------------------------------------------------------------------------

def _rule_based_classify(question: str) -> dict:
    """Fast rule-based classification when DeepSeek is unavailable."""
    q = question.lower()

    # Check for city-level questions
    city_keywords = ["哪个城市", "城市级", "地级市", "城市排名", "城市表现"]
    if any(k in question for k in city_keywords):
        return {"category": "unsupported", "reason": "rule: city-level data not available"}

    # Future prediction
    future_keywords = ["未来", "十年", "潜力", "预测", "趋势", "前景", "将会", "可能更好"]
    if any(k in q for k in future_keywords):
        return {"category": "future_prediction", "reason": "rule: future/prediction keywords"}

    # Layout recommendation
    layout_keywords = ["布局", "适合", "承接", "哪个更", "比较", "对比", "哪里", "哪个省"]
    if any(k in q for k in layout_keywords) and _extract_province(question):
        return {"category": "layout_recommendation", "reason": "rule: layout/comparison keywords"}

    # Province diagnosis
    diag_keywords = ["短板", "障碍", "诊断", "为什么", "怎么样", "如何提升", "分析"]
    if _extract_province(question) and any(k in q for k in diag_keywords):
        return {"category": "province_diagnosis", "reason": "rule: province + diagnosis keywords"}

    # Data query
    data_keywords = ["排名", "前十", "得分", "第几", "top", "多少", "数据", "数值", "查询"]
    if any(k in q for k in data_keywords):
        return {"category": "data_query", "reason": "rule: data query keywords"}

    # Single province mention → province diagnosis
    if _extract_province(question):
        return {"category": "province_diagnosis", "reason": "rule: province mentioned"}

    # Default: concept explanation
    return {"category": "concept_explanation", "reason": "rule: fallback"}


async def classify_question(question: str) -> dict:
    """Classify the user question using DeepSeek, falling back to rules."""
    # Check DeepSeek availability first
    try:
        _get_deepseek_key()
    except RuntimeError:
        return _rule_based_classify(question)

    try:
        result = await _call_llm(ROUTER_SYSTEM_PROMPT, question, temperature=0.0)
        json_match = re.search(r"\{[^}]+\}", result)
        if json_match:
            return json.loads(json_match.group())
        return _rule_based_classify(question)
    except Exception:
        return _rule_based_classify(question)


# ---------------------------------------------------------------------------
# Tool dispatch
# ---------------------------------------------------------------------------

def _extract_province(question: str, category: str = "") -> Optional[str]:
    """Try to extract a province name from the question."""
    provinces = [
        "北京", "天津", "上海", "重庆",
        "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
        "江苏", "浙江", "安徽", "福建", "江西", "山东",
        "河南", "湖北", "湖南", "广东", "广西", "海南",
        "四川", "贵州", "云南", "西藏",
        "陕西", "甘肃", "青海", "宁夏", "新疆",
    ]
    for p in provinces:
        if p in question:
            return p
    return None


def _extract_provinces_from_compare(question: str) -> list[str]:
    """Extract multiple provinces for comparison."""
    provinces = [
        "北京", "天津", "上海", "重庆",
        "河北", "山西", "内蒙古", "辽宁", "吉林", "黑龙江",
        "江苏", "浙江", "安徽", "福建", "江西", "山东",
        "河南", "湖北", "湖南", "广东", "广西", "海南",
        "四川", "贵州", "云南", "西藏",
        "陕西", "甘肃", "青海", "宁夏", "新疆",
    ]
    found = [p for p in provinces if p in question]
    return found if len(found) >= 2 else []


def dispatch_tools(question: str, category: str) -> list[dict]:
    """Run relevant DB tools based on question category and content."""
    results = []
    province = _extract_province(question, category)

    try:
        if category == "data_query":
            if "排名" in question or "top" in question.lower() or "前十" in question:
                results.append(get_top_rankings(2024, 10))
            elif province:
                results.append(get_province_score(province, 2024))
                results.append(get_province_trend(province))
            else:
                results.append(get_latest_scores())

        elif category == "province_diagnosis":
            if province:
                results.append(get_province_score(province, 2024))
                results.append(get_lpa_result(province))
                results.append(get_obstacle_result(province))
                results.append(get_shap_top_features(province, 2024))
            else:
                results.append(get_latest_scores())

        elif category == "layout_recommendation":
            if province:
                results.append(get_layout_recommendation(province))
                results.append(get_province_score(province, 2024))
                results.append(get_obstacle_result(province))
            else:
                # Compare provinces for layout
                compare_provs = _extract_provinces_from_compare(question)
                if len(compare_provs) >= 2:
                    results.append(compare_provinces(compare_provs))
                results.append(get_top_rankings(2024, 10))

        elif category == "future_prediction":
            results.append(get_future_potential_ranking(10))
            results.append(get_latest_scores())

        elif category == "concept_explanation":
            # No DB tools needed for conceptual questions
            pass

        # Always include recent scores for context if category is not concept
        if category != "concept_explanation" and category != "unsupported":
            if not any(r.get("tool") == "get_latest_scores" for r in results):
                results.append(get_latest_scores())

    except Exception as e:
        logger.error(f"Tool error: {e}")
        results.append({"tool": "error", "message": str(e)})

    return results


# ---------------------------------------------------------------------------
# Main Chat Pipeline
# ---------------------------------------------------------------------------

async def chat(question: str, history: list[dict] = None) -> dict:
    """
    Process a user question through the full pipeline:
    classify → retrieve → query DB → generate answer.

    Returns a dict with keys: answer, category, tool_calls, rag_sources.
    This function NEVER raises — all errors are caught and returned as answers.
    """
    try:
        return await _chat_impl(question, history)
    except Exception as e:
        logger.exception("Chat pipeline crashed")
        return {
            "answer": f"抱歉，处理您的问题时遇到了内部错误。请稍后重试或换个问题。",
            "category": "error",
            "tool_calls": [],
            "rag_sources": [],
        }


async def _chat_impl(question: str, history: list[dict] = None) -> dict:
    # 1. Classify
    classification = await classify_question(question)
    category = classification.get("category", "concept_explanation")
    logger.info(f"Question classified as: {category}")

    # Handle unsupported early
    if category == "unsupported":
        return {
            "answer": (
                "当前平台的数据粒度为**省级行政区**（省、自治区、直辖市），"
                "暂不支持您所询问的数据粒度或问题类型。\n\n"
                "如果您需要省域级别的绿色算力分析，我可以为您提供：\n"
                "- 31 省的 TOPSIS 综合得分与排名\n"
                "- 特定省份的障碍度诊断与布局建议\n"
                "- 省域未来潜力预测\n"
                "- LPA 类型识别与空间演化分析\n\n"
                "请尝试以省域视角重新提问。"
            ),
            "category": category,
            "tool_calls": [],
            "rag_sources": [],
        }

    # 2. Retrieve RAG documents
    retriever = get_retriever()
    rag_chunks = retriever.retrieve(question, top_k=5) if retriever.count() > 0 else []

    # 3. Run DB tools
    tool_results = dispatch_tools(question, category)

    # 4. Build context
    context = build_context(question, category, rag_chunks, tool_results, history)

    # 5. Build user message
    user_msg = f"""## 用户问题
{question}

## 问题类型
{category}

{context}

请根据以上信息，按照回答结构要求生成完整的回答。"""

    # 6. Generate answer via DeepSeek (or fallback)
    try:
        answer = await _call_llm(CHAT_SYSTEM_PROMPT, user_msg, temperature=0.5)
    except Exception as e:
        logger.warning(f"LLM unavailable ({e}), using rule-based answer from tool results")
        answer = _fallback_answer(question, category, tool_results)

    return {
        "answer": answer,
        "category": category,
        "tool_calls": [r.get("tool", "unknown") for r in tool_results],
        "rag_sources": [c.get("title", c.get("source", "")) for c in rag_chunks],
    }


def _fallback_answer(question: str, category: str, tool_results: list[dict]) -> str:
    """Generate a basic answer from tool results when LLM is unavailable."""
    if not tool_results:
        return (
            "当前无法连接到 AI 模型服务，且没有可用的数据库查询结果。"
            "请检查 DEEPSEEK_API_KEY 配置或稍后重试。"
        )

    parts = ["## 数据库查询结果（离线模式）\n"]
    for r in tool_results:
        tool_name = r.get("tool", "unknown")
        if "data" in r:
            import json
            parts.append(f"### {tool_name}\n```json\n{json.dumps(r['data'], ensure_ascii=False, indent=2)[:500]}\n```\n")

    parts.append("\n> ⚠️ AI 模型暂时不可用，以上为数据库直接查询结果。")
    return "\n".join(parts)
