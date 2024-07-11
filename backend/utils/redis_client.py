#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from backend.core.config import settings
from redis.asyncio.client import Redis
from backend.utils.log_control import logger
from redis.exceptions import TimeoutError, AuthenticationError, RedisError


class RedisCli(Redis):

    def __init__(self):
        super().__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,  # 转码 utf-8
        )

    async def open(self):
        try:
            # 尝试连接到 Redis 服务器
            await self.ping()
            logger.info("✅ 成功连接到 Redis 服务器")
        except TimeoutError as e:
            logger.error(f"❌ Redis 连接超时: {e}")
            sys.exit()
        except AuthenticationError as e:
            logger.error(f"❌ Redis 身份验证失败: {e}")
            sys.exit()
        except RedisError as e:
            logger.error(f"❌ Redis 连接错误: {e}")
            sys.exit()
        except Exception as e:
            logger.error(f"❌ 未知错误: {e}")
            sys.exit()


redis_client = RedisCli()
