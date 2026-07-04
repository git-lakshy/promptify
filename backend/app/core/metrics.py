from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from app.core.logging import logger

# HTTP Metrics
http_requests_total = Counter(
    'promptify_requests_total',
    'Total HTTP requests',
    ['method', 'path', 'status']
)

http_request_duration = Histogram(
    'promptify_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path']
)

# LLM Metrics
llm_calls_total = Counter(
    'promptify_llm_calls_total',
    'Total LLM API calls',
    ['provider', 'mode', 'status']
)

llm_latency = Histogram(
    'promptify_llm_latency_seconds',
    'LLM API call latency in seconds',
    ['provider', 'mode']
)

# User Metrics
active_users_gauge = Gauge(
    'promptify_active_users',
    'Number of active users'
)

rate_limit_hits = Counter(
    'promptify_rate_limit_hits_total',
    'Total rate limit hits',
    ['mode', 'user_type']
)

async def get_metrics():
    return generate_latest()
