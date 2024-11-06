from prometheus_client import Counter, Histogram, Gauge

# Prometheus 메트릭 정의 (backend)
REQUEST_COUNT = Counter("request_count", "Total request count", ["method", "path"])
REQUEST_DURATION = Histogram("request_duration_seconds", "Request duration", ["method", "path"])
RESPONSE_STATUS = Counter('http_response_status', 'HTTP Response Status Codes', ['method', 'path', 'status_code'])

# Prometheus 메트릭 정의 (postgres)
ACTIVE_CONNECTIONS = Gauge('pg_active_connections', 'Number of active connections')
TOTAL_CACHE_HIT_RATIO = Gauge('pg_total_cache_hit_ratio', 'Total cache hit ratio')
INDEX_SCAN_RATIO = Gauge('pg_index_scan_ratio', 'Index scan ratio')
FETCH_RATE = Gauge('pg_fetch_rate', 'Fetch throughput')
INSERT_RATE = Gauge('pg_insert_rate', 'Insert throughput')
UPDATE_RATE = Gauge('pg_update_rate', 'Update throughput')
DELETE_RATE = Gauge('pg_delete_rate', 'Delete throughput')
DEADLOCK_COUNT = Gauge('pg_deadlock_count', 'Number of deadlocks')
REPLICATION_LAG_BYTES = Gauge('pg_replication_lag_bytes', 'Replication lag in bytes')
COMMIT_COUNT = Gauge('pg_stat_database_xact_commit', 'Number of commit transactions')
ROLLBACK_COUNT = Gauge('pg_stat_database_xact_rollback', 'Number of rollback transactions')
READ_DISK = Gauge('pg_stat_database_blks_read', 'Number of blocks read from disk')
READ_CACHE = Gauge('pg_stat_database_blks_hit', 'Number of blocks read from cache')

CACHE_HIT_RATIO_METRICS = {}
