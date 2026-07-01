import time
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.metrics import http_requests_total, http_request_duration
from app.core.logging import logger


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:
            # Record failed request before re-raising
            duration = time.perf_counter() - start_time
            try:
                path = request.url.path if hasattr(request, "url") else request.scope.get("path", "")
                method = request.method if hasattr(request, "method") else "UNKNOWN"
                http_requests_total.labels(method=method, path=path, status="500").inc()
                http_request_duration.labels(method=method, path=path).observe(duration)
            except Exception:
                pass
            raise exc

        duration = time.perf_counter() - start_time

        try:
            status = str(response.status_code)
            path = request.url.path if hasattr(request, "url") else request.scope.get("path", "")
            method = request.method if hasattr(request, "method") else "UNKNOWN"

            http_requests_total.labels(
                method=method,
                path=path,
                status=status
            ).inc()

            http_request_duration.labels(
                method=method,
                path=path
            ).observe(duration)
        except Exception as e:
            logger.error(f"Error recording metrics: {e}")

        return response
