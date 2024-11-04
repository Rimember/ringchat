from prometheus_client import Gauge
from app.db.database import get_connection, close_connection
from app.metrics.prometheus_metrics import *

async def record_pg_metrics():
    # Connect to PostgreSQL
    conn = await get_connection()
    try:
        # Total transactions 
        commit_result = await conn.fetchval("SELECT xact_commit FROM pg_stat_database WHERE datname = current_database();")
        COMMIT_COUNT.set(commit_result)
        
        rollback_result = await conn.fetchval("SELECT xact_rollback FROM pg_stat_database WHERE datname = current_database();")
        ROLLBACK_COUNT.set(rollback_result)
        
        # Active connections
        active_conn_result = await conn.fetchval("SELECT count(*) FROM pg_stat_activity WHERE state = 'active';")
        ACTIVE_CONNECTIONS.set(active_conn_result)
        
        # Total cache hit ration 
        cache_hit_result = await conn.fetchval("""
                SELECT 
                    CASE 
                        WHEN SUM(heap_blks_hit + heap_blks_read) = 0 THEN 0
                        ELSE 100 * SUM(heap_blks_hit) / SUM(heap_blks_hit + heap_blks_read)
                    END AS overall_cache_hit_ratio
                FROM pg_statio_user_tables
                WHERE (heap_blks_hit + heap_blks_read) > 0;
        """)
        if cache_hit_result is not None: 
            TOTAL_CACHE_HIT_RATIO.set(cache_hit_result)
        else: 
            TOTAL_CACHE_HIT_RATIO.set(0)
        
        # Cache hit ratio 
        cache_hit_results = await conn.fetch("""
            SELECT relname,
                   heap_blks_hit,
                   heap_blks_read,
                   CASE 
                       WHEN (heap_blks_hit + heap_blks_read) = 0 THEN 0
                       ELSE 100 * heap_blks_hit / (heap_blks_hit + heap_blks_read)
                   END AS cache_hit_ratio
            FROM pg_statio_user_tables;
        """)
            
        for result in cache_hit_results:
            table_name = result['relname']
            cache_hit_ratio = result['cache_hit_ratio']
            
            # If the metric for this table doesn't exist yet, create it
            if table_name not in CACHE_HIT_RATIO_METRICS:
                CACHE_HIT_RATIO_METRICS[table_name] = Gauge(f'cache_hit_ratio_{table_name}', f'Cache hit ratio for {table_name} table')
            
            # Set the value of the metric to the cache hit ratio
            CACHE_HIT_RATIO_METRICS[table_name].set(cache_hit_ratio)

        # Index scan ratio (with division by zero and None protection)
        index_scan_result = await conn.fetchval("""
            SELECT CASE 
                     WHEN (sum(seq_scan) + sum(idx_scan)) = 0 THEN 0
                     ELSE sum(idx_scan) / (sum(seq_scan) + sum(idx_scan))
                   END AS index_scan_ratio
            FROM pg_stat_user_tables;
        """)

        # Handle None case for index scan ratio
        INDEX_SCAN_RATIO.set(index_scan_result)

        # Fetch, Insert, Update, Delete rates
        rates_result = await conn.fetchrow("""
            SELECT tup_fetched, tup_inserted, tup_updated, tup_deleted 
            FROM pg_stat_database WHERE datname = current_database();
        """)
        FETCH_RATE.set(rates_result['tup_fetched'])
        INSERT_RATE.set(rates_result['tup_inserted'])
        UPDATE_RATE.set(rates_result['tup_updated'])
        DELETE_RATE.set(rates_result['tup_deleted'])

        # Deadlock count
        deadlock_result = await conn.fetchval("""
            SELECT deadlocks FROM pg_stat_database WHERE datname = current_database();
        """)
        DEADLOCK_COUNT.set(deadlock_result)

        # Replication lag (in bytes)
        replication_lag_result = await conn.fetchval("""
            SELECT pg_current_wal_lsn() - replay_lsn AS replication_lag_bytes 
            FROM pg_stat_replication;
        """)

        # Handle None case for replication lag
        if replication_lag_result is not None:
            REPLICATION_LAG_BYTES.set(replication_lag_result)
        else:
            REPLICATION_LAG_BYTES.set(0)  # Set to 0 if no 
            
        
        # Data transfer volume 
        disk_result = await conn.fetchval("SELECT blks_read FROM pg_stat_database WHERE datname = current_database();")
        READ_DISK.set(disk_result)
        
        cache_result = await conn.fetchval("SELECT blks_hit FROM pg_stat_database WHERE datname = current_database();")
        READ_CACHE.set(cache_result)    
        
        
    finally:
        await close_connection(conn)
