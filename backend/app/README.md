# Green Compute System — FastAPI Backend

## 快速启动

```bash
# 1. 安装依赖
cd green-compute-system
pip install -r requirements.txt

# 2. 确保 .env 已配置
cat .env
# DATABASE_URL=postgresql+psycopg2://postgres:your_password@localhost:5432/green_compute

# 3. 启动服务
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

## API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- 健康检查: http://localhost:8000/health

## 接口列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/provinces` | 所有省份基础信息 |
| GET | `/api/scores?year=2024` | 某年度综合得分与排名 |
| GET | `/api/province/{province}/profile?year=2024` | 省份综合画像 |
| GET | `/api/obstacles?province=贵州` | 省份障碍度诊断 |
| GET | `/api/lpa` | LPA 类型识别结果 |
| GET | `/api/shap?province=贵州&year=2024` | SHAP 局部解释 |
| GET | `/api/layout?province=贵州` | 资源布局决策 |
| GET | `/api/overview?year=2024` | 首页总览 |

## 示例请求

```bash
# 省份列表
curl http://localhost:8000/api/provinces | python3 -m json.tool

# 2024年综合得分
curl "http://localhost:8000/api/scores?year=2024" | python3 -m json.tool

# 贵州综合画像
curl "http://localhost:8000/api/province/%E8%B4%B5%E5%B7%9E/profile?year=2024" | python3 -m json.tool

# 贵州障碍度
curl "http://localhost:8000/api/obstacles?province=%E8%B4%B5%E5%B7%9E" | python3 -m json.tool

# LPA 结果
curl http://localhost:8000/api/lpa | python3 -m json.tool

# 贵州 SHAP 解释
curl "http://localhost:8000/api/shap?province=%E8%B4%B5%E5%B7%9E&year=2024" | python3 -m json.tool

# 贵州布局决策
curl "http://localhost:8000/api/layout?province=%E8%B4%B5%E5%B7%9E" | python3 -m json.tool

# 首页总览
curl "http://localhost:8000/api/overview?year=2024" | python3 -m json.tool
```

## 项目结构

```
backend/app/
├── main.py              # FastAPI 入口，CORS 配置
├── database.py          # SQLAlchemy engine + session
├── models.py            # ORM 模型（12 张表）
├── schemas.py           # Pydantic 响应模型
├── api/
│   └── routes.py        # 8 个 API 路由
└── services/
    ├── province.py      # 省份查询
    ├── score.py         # 得分查询
    ├── obstacle.py      # 障碍度查询
    ├── lpa.py           # LPA 查询
    ├── shap.py          # SHAP 查询
    ├── layout.py        # 布局决策查询
    └── overview.py      # 总览查询
```

## 错误处理

所有接口统一返回 JSON 格式错误：

```json
{
  "detail": "Province 'xxx' not found. Available provinces: [...]"
}
```

- `404` — 数据不存在（含可用值提示）
- `422` — 参数校验失败
- `500` — 内部错误
