import json
from fastapi import APIRouter, HTTPException

from app.schemas.eval import EvalGateRequest, EvalGateResponse, EvalRunRequest, EvalRunResponse
from app.services import eval_service

router = APIRouter(prefix="/eval", tags=["eval"])


@router.post("/run", response_model=EvalRunResponse)
async def run_eval(request: EvalRunRequest):
    try:
        result = eval_service.run_eval(request.eval_set, request.mode, request.limit)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return result


@router.post("/gate", response_model=EvalGateResponse)
async def gate_eval(request: EvalGateRequest):
    baseline = _load_results(request.baseline_run_id)
    candidate = _load_results(request.candidate_run_id)

    decision, why = _apply_gate_rules(baseline, candidate, request.rules)
    return {"decision": decision, "why": why}


def _load_results(run_id: str) -> dict:
    results_path = eval_service.DATA_DIR / "eval_runs" / run_id / "results.json"
    if not results_path.is_file():
        raise HTTPException(status_code=404, detail=f"Results not found for run_id: {run_id}")
    return json.loads(results_path.read_text(encoding="utf-8"))


def _apply_gate_rules(baseline: dict, candidate: dict, rules) -> tuple[str, list[str]]:
    baseline_summary = baseline.get("summary", {})
    candidate_summary = candidate.get("summary", {})

    baseline_avg = baseline_summary.get("avg_score", 0)
    candidate_avg = candidate_summary.get("avg_score", 0)
    avg_gain = candidate_avg - baseline_avg

    baseline_cost = baseline_summary.get("avg_cost_tokens", 0) or 0
    candidate_cost = candidate_summary.get("avg_cost_tokens", 0) or 0
    cost_increase_pct = 0.0
    if baseline_cost:
        cost_increase_pct = ((candidate_cost - baseline_cost) / baseline_cost) * 100

    baseline_hard_fail = baseline_summary.get("hard_fail_count", 0)
    candidate_hard_fail = candidate_summary.get("hard_fail_count", 0)

    why = []
    decision = "merge"

    if avg_gain >= rules.min_avg_gain:
        why.append(f"avg_score +{avg_gain:.1f}")
    else:
        why.append(f"avg_score +{avg_gain:.1f} below {rules.min_avg_gain}")
        decision = "rollback"

    if cost_increase_pct <= rules.max_cost_increase_pct:
        why.append(f"cost +{cost_increase_pct:.1f}% within limit")
    else:
        why.append(f"cost +{cost_increase_pct:.1f}% above {rules.max_cost_increase_pct}")
        decision = "rollback"

    if rules.hard_fail_must_not_increase:
        if candidate_hard_fail <= baseline_hard_fail:
            why.append("hard_fail no increase")
        else:
            why.append("hard_fail increased")
            decision = "rollback"

    return decision, why
