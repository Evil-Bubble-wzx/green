"""
/api/chat — Natural language query interface.

Simple protection: question length limit + project relevance check.
No per-IP rate limiting (all users share the same backend IP via proxy).
"""

import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from .chat_service import chat

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])

MAX_QUESTION_LENGTH = 2000


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=MAX_QUESTION_LENGTH)


class ChatResponse(BaseModel):
    answer: str
    category: str
    tool_calls: list[str] = []
    rag_sources: list[str] = []


def _is_relevant(question: str) -> bool:
    """Check if question is related to the green compute project."""
    keywords = [
        "算力", "绿色", "省份", "省域", "能源", "低碳", "碳", "排名", "得分",
        "指标", "维度", "TOPSIS", "LPA", "SHAP", "障碍", "诊断", "短板",
        "布局", "决策", "承载", "数据中心", "枢纽", "潜力", "预测", "演化",
        "Markov", "Moran", "Dagum", "LISA", "基尼", "空间自相关",
        "北京", "天津", "上海", "重庆", "河北", "山西", "内蒙古",
        "辽宁", "吉林", "黑龙江", "江苏", "浙江", "安徽", "福建",
        "江西", "山东", "河南", "湖北", "湖南", "广东", "广西",
        "海南", "四川", "贵州", "云南", "西藏", "陕西", "甘肃",
        "青海", "宁夏", "新疆", "东部", "中部", "西部", "东北",
    ]
    return any(kw in question for kw in keywords)


@router.post("/chat", response_model=ChatResponse, summary="智能问答")
async def chat_endpoint(req: ChatRequest):
    """自然语言智能问答（公开访问）。"""
    # Relevance check
    if not _is_relevant(req.question):
        return ChatResponse(
            answer="你好，我是省域绿色算力承载能力评估与资源布局决策支持系统的智能问答助手。当前主要支持绿色算力、承载能力评估、TOPSIS 排名、障碍因子诊断、空间格局、布局建议和未来预测等问题。你可以问我：上海绿色算力排名是多少？江苏的优势和短板是什么？哪些省份适合布局绿色算力？",
            category="out_of_scope",
            tool_calls=[],
            rag_sources=[],
        )

    try:
        result = await chat(req.question)
        return ChatResponse(
            answer=result["answer"],
            category=result["category"],
            tool_calls=result.get("tool_calls", []),
            rag_sources=result.get("rag_sources", []),
        )
    except Exception as e:
        logger.exception("Chat error")
        raise HTTPException(status_code=500, detail="问答服务暂时不可用，请稍后重试。")
