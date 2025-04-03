
from .oc_logger import OC_logger  

def handle_error(e, context=""):
    logger = OC_logger.oc_log("error")
    msg = f"[{context}] {type(e).__name__}: {e}"
    logger.error(msg)
