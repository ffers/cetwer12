import time
import tracemalloc
from utils.oc_logger import OC_logger

def wrapper(name=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = name or func.__name__
            logger = OC_logger.oc_log(func_name)

            logger.debug(f"▶ {func_name}() called")
            tracemalloc.start()
            start_time = time.time()

            try:
                result = func(*args, **kwargs)
                duration = round(time.time() - start_time, 4)
                current, peak = tracemalloc.get_traced_memory()

                logger.debug(
                    f"✔ {func_name}() ok ({duration}s, "
                    f"memory: {round(peak / 1024)} KB)"
                )

                return {
                    func_name: "ok",
                    "result": result,
                    "duration": duration,
                    "memory_kb": round(peak / 1024)
                }

            except Exception as e:
                logger.exception(f"✖ {func_name}() failed: {e}")
                return {
                    func_name: "fail",
                    "error": str(e)
                }

            finally:
                tracemalloc.stop()

        return wrapper
    return decorator
