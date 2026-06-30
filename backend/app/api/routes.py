"""
API Routes for Green Compute System.

All endpoints return JSON with proper error handling.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas
from ..services import (
    province as province_svc,
    score as score_svc,
    obstacle as obstacle_svc,
    lpa as lpa_svc,
    shap as shap_svc,
    layout as layout_svc,
    overview as overview_svc,
)

router = APIRouter(prefix="/api")


# ---------------------------------------------------------------------------
# 1. GET /api/provinces
# ---------------------------------------------------------------------------

@router.get(
    "/provinces",
    response_model=schemas.ProvinceListOut,
    summary="所有省份基础信息",
)
def list_provinces(db: Session = Depends(get_db)):
    """返回所有省份的区域、枢纽状态和邻接信息。"""
    try:
        rows = province_svc.get_all_provinces(db)
        return schemas.ProvinceListOut(
            count=len(rows),
            provinces=[schemas.ProvinceBasicOut.model_validate(r) for r in rows],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 2. GET /api/scores?year=2024
# ---------------------------------------------------------------------------

@router.get(
    "/scores",
    response_model=schemas.ScoreListOut,
    summary="某年度绿色算力综合得分",
)
def list_scores(
    year: int = Query(2024, ge=2016, le=2030, description="年份"),
    db: Session = Depends(get_db),
):
    """返回某一年所有省份的绿色算力综合得分和排名，按排名升序。"""
    try:
        rows = score_svc.get_scores_by_year(db, year)
        return schemas.ScoreListOut(
            year=year,
            count=len(rows),
            scores=[schemas.ScoreItem.model_validate(r) for r in rows],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 3. GET /api/province/{province}/profile?year=2024
# ---------------------------------------------------------------------------

@router.get(
    "/province/{province}/profile",
    response_model=schemas.ProvinceProfileOut,
    summary="省份综合画像",
)
def get_province_profile(
    province: str,
    year: int = Query(2024, description="年份"),
    db: Session = Depends(get_db),
):
    """
    返回某省某年的综合画像：
    综合得分、排名、区域、LPA类型、主要障碍因素、布局建议。
    """
    try:
        from ..models import (
            TopsisScore,
            LpaProvinceAssignment,
            ObstacleProvince,
            LayoutProvinceDecision,
        )

        score = (
            db.query(TopsisScore)
            .filter(TopsisScore.province == province, TopsisScore.year == year)
            .first()
        )
        lpa = (
            db.query(LpaProvinceAssignment)
            .filter(LpaProvinceAssignment.province == province)
            .first()
        )
        obstacle = (
            db.query(ObstacleProvince)
            .filter(ObstacleProvince.province == province)
            .first()
        )
        layout = (
            db.query(LayoutProvinceDecision)
            .filter(LayoutProvinceDecision.province == province)
            .first()
        )

        if not score and not lpa and not obstacle and not layout:
            # Suggest valid province names
            from ..models import TopsisScore as TS
            all_provs = [
                r[0]
                for r in db.query(TS.province).distinct().order_by(TS.province).all()
            ]
            raise HTTPException(
                status_code=404,
                detail=f"Province '{province}' not found. Available: {all_provs}",
            )

        return schemas.ProvinceProfileOut(
            province=province,
            year=year,
            region=obstacle.region if obstacle else (
                layout.region if layout else None
            ),
            composite_score=score.composite_score if score else None,
            rank=score.rank if score else None,
            lpa_type=lpa.lpa_type if lpa else None,
            type_name=lpa.type_name if lpa else (
                layout.type_name if layout else None
            ),
            primary_obstacle_dimension=(
                obstacle.primary_obstacle_dimension if obstacle else None
            ),
            primary_obstacle_degree=(
                obstacle.primary_obstacle_degree if obstacle else None
            ),
            secondary_obstacle_dimension=(
                obstacle.secondary_obstacle_dimension if obstacle else None
            ),
            secondary_obstacle_degree=(
                obstacle.secondary_obstacle_degree if obstacle else None
            ),
            weakness_diagnosis_type=(
                obstacle.weakness_diagnosis_type if obstacle else None
            ),
            recommended_layout_type=(
                layout.recommended_layout_type if layout else None
            ),
            layout_orientation=layout.layout_orientation if layout else None,
            functional_positioning=layout.functional_positioning if layout else None,
            optimization_strategy=layout.optimization_strategy if layout else None,
            risk_warning=layout.risk_warning if layout else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 4. GET /api/obstacles?province=贵州
# ---------------------------------------------------------------------------

@router.get(
    "/obstacles",
    response_model=schemas.ObstacleProvinceOut,
    summary="省份障碍度诊断",
)
def get_obstacles(
    province: str = Query(..., description="省份名称"),
    db: Session = Depends(get_db),
):
    """返回某省的障碍度诊断结果（首要/次要障碍维度、障碍度、短板类型）。"""
    try:
        row = obstacle_svc.get_obstacle_by_province(db, province)
        return schemas.ObstacleProvinceOut.model_validate(row)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 5. GET /api/lpa
# ---------------------------------------------------------------------------

@router.get(
    "/lpa",
    response_model=schemas.LpaListOut,
    summary="LPA类型识别结果",
)
def get_lpa(db: Session = Depends(get_db)):
    """返回所有省份的LPA类型归属和四类模型汇总。"""
    try:
        data = lpa_svc.get_lpa_results(db)
        return schemas.LpaListOut(
            province_assignments=[
                schemas.LpaProvinceItem.model_validate(r)
                for r in data["province_assignments"]
            ],
            type_summary=[
                schemas.LpaTypeItem.model_validate(r)
                for r in data["type_summary"]
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 6. GET /api/shap?province=贵州&year=2024
# ---------------------------------------------------------------------------

@router.get(
    "/shap",
    response_model=schemas.ShapListOut,
    summary="SHAP局部解释",
)
def get_shap(
    province: str = Query(..., description="省份名称"),
    year: int = Query(2024, description="年份"),
    db: Session = Depends(get_db),
):
    """
    返回某省某年的SHAP局部解释结果（Top 8），按绝对SHAP值从高到低排序。
    """
    try:
        rows = shap_svc.get_shap_local(db, province, year)
        return schemas.ShapListOut(
            province=province,
            year=year,
            count=len(rows),
            explanations=[
                schemas.ShapLocalItem.model_validate(r) for r in rows
            ],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 7. GET /api/layout?province=贵州
# ---------------------------------------------------------------------------

@router.get(
    "/layout",
    response_model=schemas.LayoutDecisionOut,
    summary="资源布局决策",
)
def get_layout(
    province: str = Query(..., description="省份名称"),
    db: Session = Depends(get_db),
):
    """返回某省的资源布局决策结果（推荐布局类型、功能定位、优化策略、风险提示）。"""
    try:
        row = layout_svc.get_layout_by_province(db, province)
        return schemas.LayoutDecisionOut.model_validate(row)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 8. GET /api/overview?year=2024
# ---------------------------------------------------------------------------

@router.get(
    "/overview",
    response_model=schemas.OverviewOut,
    summary="首页总览",
)
def get_overview(
    year: int = Query(2024, ge=2016, le=2030, description="年份"),
    db: Session = Depends(get_db),
):
    """
    返回首页总览数据：
    全国平均得分、最高/最低省份、Top 10排名、四大区域平均值。
    """
    try:
        data = overview_svc.get_overview(db, year)
        return schemas.OverviewOut(
            year=data["year"],
            national_avg_score=data["national_avg_score"],
            highest_province=data["highest_province"],
            highest_score=data["highest_score"],
            lowest_province=data["lowest_province"],
            lowest_score=data["lowest_score"],
            top10=[schemas.ScoreItem.model_validate(r) for r in data["top10"]],
            region_averages=data["region_averages"],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


# ---------------------------------------------------------------------------
# 9-12. New public endpoints (indicators, dagum, moran, markov)
# ---------------------------------------------------------------------------

@router.get("/indicators", response_model=schemas.IndicatorListOut, summary="指标体系")
def list_indicators(db: Session = Depends(get_db)):
    from ..services import indicator as ind_svc
    try:
        rows = ind_svc.get_indicators(db)
        return schemas.IndicatorListOut(
            count=len(rows),
            indicators=[schemas.IndicatorItem.model_validate(r) for r in rows],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@router.get("/dagum", response_model=schemas.DagumOut, summary="Dagum 基尼系数分解")
def get_dagum(db: Session = Depends(get_db)):
    from ..services import dagum as d_svc
    try:
        return schemas.DagumOut(
            decomposition=[schemas.DagumDecompItem.model_validate(r) for r in d_svc.get_dagum_decomposition(db)],
            intra_region=[schemas.DagumIntraItem.model_validate(r) for r in d_svc.get_dagum_intra_region(db)],
            inter_region=[schemas.DagumInterItem.model_validate(r) for r in d_svc.get_dagum_inter_region(db)],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@router.get("/moran", response_model=schemas.MoranOut, summary="Moran's I 空间自相关")
def get_moran(db: Session = Depends(get_db)):
    from ..services import moran as m_svc
    try:
        return schemas.MoranOut(
            moran_series=[schemas.MoranItem.model_validate(r) for r in m_svc.get_moran(db)],
            lisa_2024=[schemas.LisaItem.model_validate(r) for r in m_svc.get_lisa(db)],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")


@router.get("/markov", response_model=schemas.MarkovOut, summary="Markov 转移矩阵")
def get_markov(db: Session = Depends(get_db)):
    from ..services import markov as mk_svc
    try:
        return schemas.MarkovOut(
            probability=[schemas.MarkovProbItem.model_validate(r) for r in mk_svc.get_markov_probability(db)],
            spatial=[schemas.SpatialMarkovItem.model_validate(r) for r in mk_svc.get_spatial_markov(db)],
            thresholds=[schemas.StateThresholdItem.model_validate(r) for r in mk_svc.get_state_thresholds(db)],
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")
