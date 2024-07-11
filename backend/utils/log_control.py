#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
from pathlib import Path
from loguru import logger
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.core.config import ensure_path_sep


now_time_day = time.strftime("%Y-%m-%d", time.localtime())
logs_dir = Path(ensure_path_sep("\\logs"))
logs_dir.mkdir(parents=True, exist_ok=True)

logger.add(
    ensure_path_sep(f"\\logs\\info-{now_time_day}.log"),
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} {level} {module} py:{line} {message}",
    rotation="1 day",
    retention="3 days",
    encoding="utf-8",
)

logger.add(
    ensure_path_sep(f"\\logs\\error-{now_time_day}.log"),
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} {level} {module} py:{line} {message}",
    rotation="1 day",
    retention="3 days",
    encoding="utf-8"
)

logger.add(
    ensure_path_sep(f"\\logs\\warning-{now_time_day}.log"),
    level="WARNING",
    format="{time:YYYY-MM-DD HH:mm:ss} {level} {module} py:{line} {message}",
    rotation="1 day",
    retention="3 days",
    encoding="utf-8"
)


class AccessMiddleware(BaseHTTPMiddleware):
    """
    记录请求日志
    """
    async def dispatch(self, request: Request, call_next) -> Response:
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        logger.info(f'{response.status_code} {request.client.host} {request.method} {request.url} {end_time - start_time}')
        return response

if __name__ == '__main__':
    try:
        logger.info("这是一条信息日志")
        logger.critical("这是一条严重日志")
        logger.warning("这是一条警告日志")

        # 模拟异常以记录堆栈跟踪信息
        1 / 0
    except Exception as e:
        logger.exception("发生了异常")