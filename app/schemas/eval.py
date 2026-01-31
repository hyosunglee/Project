from typing import List, Optional
from pydantic import BaseModel, Field

from app.schemas.common import CommonRequest


class EvalRunRequest(BaseModel):
    eval_set: str
    mode: str
    limit: int = 50
    common: Optional[CommonRequest] = None


class EvalCaseSummary(BaseModel):
    case_id: str
    score: int
    hard_fail: bool
    fail_tags: List[str] = Field(default_factory=list)


class EvalRunSummary(BaseModel):
    avg_score: float
    hard_fail_count: int
    avg_cost_tokens: float


class EvalRunResponse(BaseModel):
    run_id: str
    summary: EvalRunSummary
    cases: List[EvalCaseSummary]


class EvalGateRules(BaseModel):
    min_avg_gain: float = 0.0
    max_cost_increase_pct: float = 0.0
    hard_fail_must_not_increase: bool = True


class EvalGateRequest(BaseModel):
    baseline_run_id: str
    candidate_run_id: str
    rules: EvalGateRules


class EvalGateResponse(BaseModel):
    decision: str
    why: List[str]
