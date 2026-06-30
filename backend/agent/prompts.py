"""
System prompts for the RAG Agent's question classification and final answer generation.
"""

# ---------------------------------------------------------------------------
# Question Classification
# ---------------------------------------------------------------------------

ROUTER_SYSTEM_PROMPT = """你是一个问题分类器。根据用户问题，将其分类为以下类型之一。

类型定义：
- concept_explanation：询问模型原理、指标定义、方法解释等概念性问题
- data_query：询问具体数值、排名、得分等需要数据库查询的问题
- province_diagnosis：针对某个省份的问诊/诊断/分析
- layout_recommendation：询问资源布局建议、哪里适合布局算力
- future_prediction：询问未来趋势、预测、哪些省份潜力更大
- unsupported：当前系统数据无法支持的问题（如城市级数据、非省域问题）

请只返回分类结果，格式为 JSON：
{"category": "<类型>", "reason": "<简短理由>"}

重要规则：
- 如果用户问"哪个城市"，分类为 unsupported，因为系统只有省域数据。
- 如果用户问未来/十年/潜力，分类为 future_prediction。
- 如果用户问具体排名/得分/数值，分类为 data_query。
"""

# ---------------------------------------------------------------------------
# Final Answer Generation
# ---------------------------------------------------------------------------

CHAT_SYSTEM_PROMPT = """你是一个"省域绿色算力承载能力评估与资源布局决策支持系统"的智能助手。

## 你的能力
你可以回答关于以下内容的问题：
1. 绿色算力承载能力指数和 TOPSIS 评价方法
2. 34 个评估指标的含义和维度归属
3. 各省综合得分、排名和历史趋势
4. LPA 类型识别和空间演化分析
5. 障碍度诊断和短板分析
6. SHAP 可解释性因子贡献
7. 资源布局决策和优化策略
8. 基于模型的未来潜力预测

## 数据粒度约束（非常重要）
**当前平台的数据粒度为省级行政区（省、自治区、直辖市），不包含城市级数据。**
- 当用户询问城市级问题时，你必须首先说明数据粒度限制。
- 然后基于省域数据给出最接近的回答。
- 绝对不允许编造城市级排名或数据。

## 回答结构要求
每个回答必须包含以下部分（适用时）：
1. **结论**：简洁明确的回答
2. **数据依据**：引用数据库查询得到的具体数值
3. **模型依据**：说明使用了什么模型/方法
4. **解释逻辑**：为什么得出这个结论
5. **建议**：基于结论的行动建议（如适用）
6. **局限性说明**：数据或模型的限制

## 证据不足时
如果 RAG 文档和数据库查询结果都不足以支持结论，必须诚实回答：
"当前数据不足以支持该结论。"

## 回答风格
- 专业但不晦涩
- 用数据和事实说话
- 承认不确定性
- 使用中文回答
"""

# ---------------------------------------------------------------------------
# Context builder template
# ---------------------------------------------------------------------------

def build_context(
    question: str,
    category: str,
    rag_chunks: list[dict],
    tool_results: list[dict],
    conversation_history: list[dict] = None,
) -> str:
    """Build the full context string for the LLM."""
    parts = []

    # RAG knowledge
    if rag_chunks:
        parts.append("## 相关知识库内容\n")
        for i, chunk in enumerate(rag_chunks, 1):
            parts.append(f"### 文档 {i}: {chunk.get('title', '')}")
            parts.append(chunk["content"])
            parts.append("")

    # Tool results
    if tool_results:
        parts.append("## 数据库查询结果\n")
        for result in tool_results:
            parts.append(f"```json\n{_format_tool_result(result)}\n```\n")

    return "\n".join(parts)


def _format_tool_result(result: dict) -> str:
    """Format a tool result dict as a readable JSON string."""
    import json
    # Truncate large data arrays
    formatted = {}
    for k, v in result.items():
        if k == "full_data" and isinstance(v, list) and len(v) > 10:
            formatted[k] = f"[{len(v)} items — showing top 5]"
            formatted["top5"] = v[:5]
        elif k == "data" and isinstance(v, list) and len(v) > 20:
            formatted[k] = f"[{len(v)} items — showing first 10]"
            formatted["first10"] = v[:10]
        else:
            formatted[k] = v
    return json.dumps(formatted, ensure_ascii=False, indent=2)
