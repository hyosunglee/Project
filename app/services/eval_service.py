import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
EVAL_RUNS_DIR = DATA_DIR / "eval_runs"


def run_eval(eval_set_path: str, mode: str, limit: int) -> dict:
    cases = _load_eval_set(eval_set_path, limit)
    run_id = _build_run_id(mode)
    case_results = []
    total_score = 0
    total_cost_tokens = 0
    hard_fail_count = 0

    for case in cases:
        output = generate_output(case)
        score, hard_fail, fail_tags = score_case(case, output)
        cost_tokens = _estimate_tokens(output)
        total_score += score
        total_cost_tokens += cost_tokens
        if hard_fail:
            hard_fail_count += 1

        case_results.append(
            {
                "case_id": case.get("case_id"),
                "score": score,
                "hard_fail": hard_fail,
                "fail_tags": fail_tags,
                "output": output,
                "cost_tokens": cost_tokens,
                "case": case,
            }
        )

    avg_score = total_score / len(case_results) if case_results else 0
    avg_cost_tokens = total_cost_tokens / len(case_results) if case_results else 0

    run_result = {
        "run_id": run_id,
        "mode": mode,
        "eval_set": eval_set_path,
        "summary": {
            "avg_score": round(avg_score, 2),
            "hard_fail_count": hard_fail_count,
            "avg_cost_tokens": round(avg_cost_tokens, 2),
        },
        "cases": [
            {
                "case_id": item["case_id"],
                "score": item["score"],
                "hard_fail": item["hard_fail"],
                "fail_tags": item["fail_tags"],
                "cost_tokens": item["cost_tokens"],
            }
            for item in case_results
        ],
        "case_details": case_results,
    }

    save_run(run_id, run_result)

    return {
        "run_id": run_id,
        "summary": run_result["summary"],
        "cases": run_result["cases"],
    }


def generate_output(case: dict) -> str:
    input_payload = case.get("input", {})
    text = input_payload.get("text", "")
    task_type = case.get("task_type", "unknown")
    return f"Task:{task_type} Summary: {text[:120]}"


def score_case(case: dict, output: str) -> Tuple[int, bool, List[str]]:
    score = 100
    fail_tags: List[str] = []
    hard_fail = False

    rubric = case.get("rubric", [])
    output_lower = output.lower()

    for item in rubric:
        if item.lower() not in output_lower:
            score -= 10

    expected = case.get("expected", {})
    must_include = expected.get("must_include", [])
    must_not_include = expected.get("must_not_include", [])

    missing_required = [field for field in must_include if field.lower() not in output_lower]
    if missing_required:
        score -= 10 * len(missing_required)
        fail_tags.extend(["missing_required_fields", "evidence_missing"])

    hallucination_hits = [field for field in must_not_include if field.lower() in output_lower]
    if hallucination_hits:
        score -= 50
        fail_tags.append("hallucination_suspected")

    if not output.strip():
        fail_tags.append("format_violation")

    hard_rules = case.get("hard_rules", [])
    max_len_rule = next((rule for rule in hard_rules if rule.startswith("max_len_")), None)
    if max_len_rule:
        try:
            max_len = int(max_len_rule.split("_")[-1])
            if len(output) > max_len:
                score -= 20
                fail_tags.append("too_long")
                hard_fail = True
        except ValueError:
            fail_tags.append("format_violation")

    if "no_hallucination" in hard_rules and "hallucination_suspected" in fail_tags:
        hard_fail = True

    if "missing_required_fields" in hard_rules and "missing_required_fields" in fail_tags:
        hard_fail = True

    score = max(0, min(100, score))
    fail_tags = sorted(set(fail_tags))

    return score, hard_fail, fail_tags


def save_run(run_id: str, run_result: dict) -> None:
    run_dir = EVAL_RUNS_DIR / run_id
    cases_dir = run_dir / "cases"
    outputs_dir = run_dir / "outputs"

    cases_dir.mkdir(parents=True, exist_ok=True)
    outputs_dir.mkdir(parents=True, exist_ok=True)

    results_path = run_dir / "results.json"
    results_path.write_text(
        json.dumps(
            {
                "run_id": run_result["run_id"],
                "mode": run_result["mode"],
                "eval_set": run_result["eval_set"],
                "summary": run_result["summary"],
                "cases": run_result["cases"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    for item in run_result.get("case_details", []):
        case_id = item.get("case_id", "unknown")
        case_path = cases_dir / f"{case_id}.json"
        case_path.write_text(
            json.dumps(
                {
                    "case_id": case_id,
                    "score": item["score"],
                    "hard_fail": item["hard_fail"],
                    "fail_tags": item["fail_tags"],
                    "cost_tokens": item["cost_tokens"],
                    "case": item["case"],
                    "output": item["output"],
                },
                ensure_ascii=False,
                indent=2,
            ),
            encoding="utf-8",
        )
        output_path = outputs_dir / f"{case_id}.txt"
        output_path.write_text(item["output"], encoding="utf-8")


def _build_run_id(mode: str) -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    return f"{timestamp}_{mode}"


def _load_eval_set(eval_set_path: str, limit: int) -> List[Dict]:
    path = Path(eval_set_path)
    if not path.is_file():
        path = DATA_DIR / "eval_sets" / eval_set_path
    if not path.is_file():
        raise FileNotFoundError(f"Eval set not found: {eval_set_path}")

    cases = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            cases.append(json.loads(line))
            if len(cases) >= limit:
                break
    return cases


def _estimate_tokens(output: str) -> int:
    return max(1, len(output.split()))
