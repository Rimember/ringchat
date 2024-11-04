from prometheus_client import Counter, Histogram, Gauge

# Prometheus 메트릭 정의 (backend)
REQUEST_COUNT = Counter("request_count", "Total request count", ["method", "path"])
REQUEST_DURATION = Histogram("request_duration_seconds", "Request duration", ["method", "path"])
RESPONSE_STATUS = Counter('http_response_status', 'HTTP Response Status Codes', ['method', 'path', 'status_code'])
