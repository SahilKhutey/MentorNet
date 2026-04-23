import logging
import sys

def setup_logging():
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("app.log")
        ]
    )
    
    # Disable propagation for some noisy libraries if needed
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
