# 1단계: 빌드 환경
FROM python:3.10-slim AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /workdir/backend

COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

# 2단계: 최종 이미지
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

WORKDIR /workdir/backend

COPY --from=builder /root/.local /root/.local

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
