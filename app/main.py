from fastapi import FastAPI

from app.routes import eval as eval_routes

app = FastAPI(title="Eval Service", version="0.1")
app.include_router(eval_routes.router)
