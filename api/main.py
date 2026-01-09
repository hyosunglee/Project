from fastapi import FastAPI
from api.routes import predict, summarize, feedback, search, legacy
from api.routes.legacy import start_training_worker, start_scheduler

app = FastAPI(title="Research Support API", version="1.0")

app.include_router(predict.router, prefix="/api")
app.include_router(summarize.router, prefix="/api")
app.include_router(feedback.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(legacy.router) # No prefix for legacy endpoints

@app.on_event("startup")
async def startup_event():
    start_training_worker()
    start_scheduler()
