# api/v1/__init__.py
from fastapi import APIRouter
from . import transformation, buffering, storage, rules, alarms, analytics

api_router = APIRouter()

api_router.include_router(transformation.router)
api_router.include_router(buffering.router)
api_router.include_router(storage.router)
api_router.include_router(rules.router)
api_router.include_router(alarms.router)
api_router.include_router(analytics.router)
