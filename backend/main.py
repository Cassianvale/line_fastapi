#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# /backend/main.py

import uvicorn
from backend.core.initialize import register_app
from backend.core.config import settings

app = register_app()

if __name__ == '__main__':
    uvicorn.run("main:app",
                host=settings.UVICORN_HOST,
                port=settings.UVICORN_PORT,
                reload=True)
