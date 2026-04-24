import logging
import sys
import json
from datetime import datetime

SENSITIVE_FIELDS = {"email", "password", "token", "access_token", "refresh_token", "secret", "authorization"}

class JsonFormatter(logging.Formatter):
    def format(self, record):
        # Basic record
        message = record.getMessage()
        
        # Mask sensitive info in the message string
        for field in SENSITIVE_FIELDS:
            if field in message.lower():
                message = f"[MASKED DATA] containing {field}"

        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "name": record.name,
            "message": message,
        }
        
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    
    logging.basicConfig(
        level=logging.INFO,
        handlers=[handler]
    )
    
    # Silence noise
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
