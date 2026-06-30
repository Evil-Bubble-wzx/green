"""
Green Compute System — FastAPI Application
===========================================
省域绿色算力承载能力评估与资源布局决策支持系统

Start with:
    uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

API docs:
    http://localhost:8000/docs
    http://localhost:8000/redoc
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router
from ..agent.router import router as chat_router

app = FastAPI(
    title="Green Compute System API",
    description=(
        "省域绿色算力承载能力评估与资源布局决策支持系统。\n\n"
        "提供指标体系、TOPSIS 综合得分、LPA 类型识别、空间演化分析、"
        "障碍度诊断、SHAP 解释和布局决策结果的数据查询接口。"
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------------------------------
# CORS — allow all origins for development
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
app.include_router(router)
app.include_router(chat_router)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["health"])
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok", "service": "green-compute-api"}
