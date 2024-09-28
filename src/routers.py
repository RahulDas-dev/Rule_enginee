from fastapi.routing import APIRouter

from src.endpoints import dataset, rules, scores

api_router = APIRouter()

api_router.include_router(scores.router, prefix="/scores", tags=["scores"])
api_router.include_router(rules.router, prefix="/rules", tags=["rules"])
api_router.include_router(dataset.router, prefix="/dataset", tags=["dataset"])
