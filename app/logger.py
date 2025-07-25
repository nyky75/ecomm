from loguru import logger
import sys
import os


os.makedirs("logs", exist_ok=True)
logger.remove()

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{module}:{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
)

logger.add(
    "logs/test_run.log",
    rotation="5 MB",
    encoding="utf-8",
    level="DEBUG",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    colorize=False,
)

log = logger
