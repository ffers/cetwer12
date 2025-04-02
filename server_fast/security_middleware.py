from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.status import HTTP_403_FORBIDDEN

BLOCKED_PATHS = [
    ".env", ".git", ".aws", ".docker", ".idea", "config", "backup",
    ".env.local", ".env.dev", ".env.prod", ".env.test", ".env.stage",
    ".env.backup", ".env.dist", ".env.ci", ".git/config", ".aws/credentials"
]

class BlockSuspiciousPathsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path.lower()
        for bad in BLOCKED_PATHS:
            if bad in path:
                return Response("⛔ Forbidden", status_code=HTTP_403_FORBIDDEN)
        return await call_next(request)
