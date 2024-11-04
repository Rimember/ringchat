from fastapi import APIRouter
from starlette.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.metrics.pg_metrics import record_pg_metrics

router = APIRouter(tags=["metrics"])


@router.get('/metrics/backend')
async def backend_metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
    