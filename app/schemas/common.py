from typing import Optional
from pydantic import BaseModel


class CostBudget(BaseModel):
    tokens: Optional[int] = None
    seconds: Optional[int] = None


class CommonRequest(BaseModel):
    request_id: Optional[str] = None
    timestamp: Optional[str] = None
    cost_budget: Optional[CostBudget] = None
