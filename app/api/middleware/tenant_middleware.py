import contextvars
from typing import Optional
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.core.security import decode_token

current_tenant_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("current_tenant", default=None)


def get_current_tenant_id() -> Optional[str]:
    return current_tenant_var.get()


class TenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_token(token, is_refresh=False)
                tenant_id = payload.get("org_id")
            except Exception:
                pass
        
        token_ctx = current_tenant_var.set(tenant_id)
        try:
            response = await call_next(request)
            return response
        finally:
            current_tenant_var.reset(token_ctx)
