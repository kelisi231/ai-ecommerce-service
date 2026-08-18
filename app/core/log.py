from loguru import logger
import sys
from pathlib import Path
from contextvars import ContextVar

# 创建日志文件夹（上上级目录）
log_dir = Path(__file__).parents[2] / "logs"
log_dir.mkdir(parents=True, exist_ok=True)

# 定义上下文变量（只需要 request_id）
request_id_var = ContextVar("request_id", default="-")

# 移除默认处理器
logger.remove()

# 控制台输出（彩色）
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | req=<cyan>{extra[request_id]}</cyan> | <level>{message}</level>",
    colorize=True,
    level="DEBUG"
)

# 文件输出（JSON格式）
logger.add(
    log_dir / "app_{time:YYYY-MM-DD}.log",
    rotation="200 MB",
    retention="7 days",
    compression="zip",
    serialize=True,
    level="INFO"
)

# 错误日志单独存
logger.add(
    log_dir / "error_{time:YYYY-MM-DD}.log",
    rotation="100 MB",
    retention="30 days",
    level="ERROR"
)

# 配置默认extra字段
logger.configure(extra={"request_id": "-"})


if __name__ == "__main__":
    logger.info("info测试")
    print("完成，查看logs目录")
