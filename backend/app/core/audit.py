import logging
import json
from datetime import datetime
from fastapi import Request

audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)
handler = logging.FileHandler("audit.log")
handler.setFormatter(logging.Formatter("%(message)s"))
audit_logger.addHandler(handler)

async def audit_log_middleware(request: Request, call_next):
    # Determine if this is a sensitive action
    path = request.url.path
    method = request.method
    
    sensitive_paths = ["/auth/login", "/auth/signup", "/user/me/purge", "/user/me/export", "/booking/create"]
    
    is_sensitive = any(p in path for p in sensitive_paths) or method in ["POST", "PUT", "DELETE"]

    response = await call_next(request)

    if is_sensitive:
        client_ip = request.client.host
        user_id = getattr(request.state, "user_id", "anonymous")
        
        audit_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "client_ip": client_ip,
            "user_id": user_id,
            "method": method,
            "path": path,
            "status_code": response.status_code,
            "user_agent": request.headers.get("user-agent")
        }
        
        audit_logger.info(json.dumps(audit_record))

    return response
