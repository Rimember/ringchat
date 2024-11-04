import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import init_db
from app.utils.logging import log_exception
from app.routers import auth, me, folders, chatrooms, messages, links, rating, metrics
from app.metrics.prometheus_metrics import REQUEST_COUNT, REQUEST_DURATION, RESPONSE_STATUS
from prometheus_fastapi_instrumentator import Instrumentator 

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Service is starting.")
    # init_db()
    yield
    print("Service is stopped.")


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # 요청 처리 시간 기록
    response.headers["X-Process-Time"] = str(process_time)
    
    # 요청 메트릭을 수집 (HTTP 메서드, 요청 URL)
    method = request.method
    path = request.url.path
    
    # 메트릭 수집
    method = request.method
    path = request.url.path
    status_code = response.status_code

    REQUEST_COUNT.labels(method=method, path=path).inc()
    REQUEST_DURATION.labels(method=method, path=path).observe(process_time)
    RESPONSE_STATUS.labels(method=method, path=path, status_code=status_code).inc()

    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(req: Request, exc: HTTPException):
    log_exception(exception=exc)

    content = {"detail": exc.detail}
    if exc.headers and "X-Error" in exc.headers:
        content["code"] = exc.headers["X-Error"]

    return JSONResponse(status_code=exc.status_code, content=content)


prefix = "/api"

app.include_router(auth.router, prefix=prefix)
app.include_router(me.router, prefix=prefix)
app.include_router(folders.router, prefix=prefix)
app.include_router(chatrooms.router, prefix=prefix)
app.include_router(messages.router, prefix=prefix)
app.include_router(links.router, prefix=prefix)
app.include_router(rating.router, prefix=prefix)
app.include_router(metrics.router)
