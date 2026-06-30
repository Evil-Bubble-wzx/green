/**
 * Unified API client for Green Compute System backend.
 *
 * Base URL is read from NEXT_PUBLIC_API_BASE_URL (default: http://localhost:8000).
 */

const BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, params?: Record<string, string | number>): Promise<T> {
  const url = BASE ? new URL(path, BASE) : new URL(path, window.location.origin);
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== "") {
        url.searchParams.set(k, String(v));
      }
    });
  }
  const res = await fetch(url.toString());
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    const detail = (body as { detail?: string }).detail || res.statusText;
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

async function post<T>(path: string, body: Record<string, unknown>): Promise<T> {
  const url = BASE ? `${BASE}${path}` : path;
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error((err as { detail?: string }).detail || res.statusText);
  }
  return res.json() as Promise<T>;
}

// ----- Types ------------------------------------------------------------

export interface ProvinceBasic {
  province: string;
  region: string | null;
  is_hub: boolean | null;
  adjacent_provinces: string | null;
  adjacent_count: number | null;
}

export interface ProvinceListOut {
  count: number;
  provinces: ProvinceBasic[];
}

export interface ScoreItem {
  province: string;
  year: number;
  composite_score: number | null;
  rank: number | null;
}

export interface ScoreListOut {
  year: number;
  count: number;
  scores: ScoreItem[];
}

export interface ProvinceProfile {
  province: string;
  year: number;
  region: string | null;
  composite_score: number | null;
  rank: number | null;
  lpa_type: string | null;
  type_name: string | null;
  primary_obstacle_dimension: string | null;
  primary_obstacle_degree: number | null;
  secondary_obstacle_dimension: string | null;
  secondary_obstacle_degree: number | null;
  weakness_diagnosis_type: string | null;
  recommended_layout_type: string | null;
  layout_orientation: string | null;
  functional_positioning: string | null;
  optimization_strategy: string | null;
  risk_warning: string | null;
}

export interface ObstacleProvince {
  province: string;
  region: string | null;
  lpa_type: string | null;
  primary_obstacle_dimension: string | null;
  primary_obstacle_degree: number | null;
  secondary_obstacle_dimension: string | null;
  secondary_obstacle_degree: number | null;
  weakness_diagnosis_type: string | null;
}

export interface LpaProvinceItem {
  province: string;
  lpa_type: string | null;
  type_name: string | null;
  score_2016: number | null;
  score_2024: number | null;
  stage_increment: number | null;
  mean_2016_2024: number | null;
  max_posterior_probability: number | null;
}

export interface LpaTypeItem {
  lpa_type: string | null;
  type_name: string | null;
  province_count: number | null;
  mean_2016: number | null;
  mean_2024: number | null;
  stage_increment: number | null;
  provinces: string | null;
}

export interface LpaListOut {
  province_assignments: LpaProvinceItem[];
  type_summary: LpaTypeItem[];
}

export interface ShapLocalItem {
  indicator_name: string | null;
  indicator_short_name: string | null;
  dimension: string | null;
  shap_value: number | null;
  abs_shap_value: number | null;
}

export interface ShapListOut {
  province: string;
  year: number;
  count: number;
  explanations: ShapLocalItem[];
}

export interface LayoutDecision {
  province: string;
  region: string | null;
  rank: number | null;
  composite_score: number | null;
  stage_increment: number | null;
  type_name: string | null;
  lisa_type: string | null;
  primary_obstacle_dimension: string | null;
  secondary_obstacle_dimension: string | null;
  weakness_diagnosis_type: string | null;
  demand_network_advantage_index: number | null;
  energy_low_carbon_advantage_index: number | null;
  constraint_pressure_index: number | null;
  suitability_index: number | null;
  recommended_layout_type: string | null;
  layout_orientation: string | null;
  functional_positioning: string | null;
  optimization_strategy: string | null;
  risk_warning: string | null;
}

export interface OverviewOut {
  year: number;
  national_avg_score: number | null;
  highest_province: string | null;
  highest_score: number | null;
  lowest_province: string | null;
  lowest_score: number | null;
  top10: ScoreItem[];
  region_averages: { region: string; avg_score: number; province_count: number }[];
}

// ----- Chat types -------------------------------------------------------

export interface ChatRequest {
  question: string;
  history?: { role: string; content: string }[];
}

export interface ChatResponse {
  answer: string;
  category: string;
  tool_calls: string[];
  rag_sources: string[];
}

// ----- API functions ----------------------------------------------------

export async function fetchProvinces(): Promise<ProvinceListOut> {
  return request<ProvinceListOut>("/api/provinces");
}

export async function fetchScores(year: number = 2024): Promise<ScoreListOut> {
  return request<ScoreListOut>("/api/scores", { year });
}

export async function fetchProvinceProfile(
  province: string,
  year: number = 2024
): Promise<ProvinceProfile> {
  return request<ProvinceProfile>(`/api/province/${encodeURIComponent(province)}/profile`, { year });
}

export async function fetchObstacles(province: string): Promise<ObstacleProvince> {
  return request<ObstacleProvince>("/api/obstacles", { province });
}

export async function fetchLpa(): Promise<LpaListOut> {
  return request<LpaListOut>("/api/lpa");
}

export async function fetchShap(
  province: string,
  year: number = 2024
): Promise<ShapListOut> {
  return request<ShapListOut>("/api/shap", { province, year });
}

export async function fetchLayout(province: string): Promise<LayoutDecision> {
  return request<LayoutDecision>("/api/layout", { province });
}

export async function fetchOverview(year: number = 2024): Promise<OverviewOut> {
  return request<OverviewOut>("/api/overview", { year });
}

export async function chat(question: string, history?: { role: string; content: string }[]): Promise<ChatResponse> {
  return post<ChatResponse>("/api/chat", { question, history: history || [] });
}

// ----- New public endpoint types ------------------------------------------

export interface IndicatorItem {
  indicator_code: string | null;
  field_name: string | null;
  indicator_name: string | null;
  dimension: string | null;
  direction: string | null;
  unit: string | null;
  meaning: string | null;
}

export interface IndicatorListOut { count: number; indicators: IndicatorItem[]; }

export interface DagumDecompItem {
  year: number; total_gini: number | null;
  intra_region_difference: number | null;
  inter_region_net_difference: number | null;
  hypervariable_density: number | null;
  intra_region_contribution_rate: number | null;
  inter_region_contribution_rate: number | null;
  hypervariable_density_contribution_rate: number | null;
}

export interface DagumIntraItem { year: number; region: string; sample_size: number | null; mean_value: number | null; intra_region_gini: number | null; }
export interface DagumInterItem { year: number; region_pair: string; high_mean_region: string | null; low_mean_region: string | null; inter_region_gini: number | null; relative_influence_d: number | null; }

export interface DagumOut { decomposition: DagumDecompItem[]; intra_region: DagumIntraItem[]; inter_region: DagumInterItem[]; }

export interface MoranItem { year: number; moran_i: number | null; two_sided_p_value: number | null; positive_p_value: number | null; }
export interface LisaItem { province: string; year: number; composite_score: number | null; standardized_score_z: number | null; spatial_lag_wz: number | null; local_moran_i: number | null; p_value: number | null; lisa_type: string | null; }
export interface MoranOut { moran_series: MoranItem[]; lisa_2024: LisaItem[]; }

export interface MarkovProbItem { from_state: string | null; to_low_level_probability: number | null; to_mid_low_level_probability: number | null; to_mid_high_level_probability: number | null; to_high_level_probability: number | null; }
export interface SpatialMarkovItem { neighborhood_state: string | null; from_state: string | null; to_state: string | null; frequency: number | null; probability: number | null; }
export interface StateThresholdItem { state: string | null; classification_rule: string | null; threshold_note: string | null; }
export interface MarkovOut { probability: MarkovProbItem[]; spatial: SpatialMarkovItem[]; thresholds: StateThresholdItem[]; }

// ----- New API functions --------------------------------------------------

export async function fetchIndicators(): Promise<IndicatorListOut> { return request<IndicatorListOut>("/api/indicators"); }
export async function fetchDagum(): Promise<DagumOut> { return request<DagumOut>("/api/dagum"); }
export async function fetchMoran(): Promise<MoranOut> { return request<MoranOut>("/api/moran"); }
export async function fetchMarkov(): Promise<MarkovOut> { return request<MarkovOut>("/api/markov"); }
