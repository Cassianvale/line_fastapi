#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from typing import Optional, Any
from fastapi import Response
from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    统一返回模型
    """
    code: int = 200
    msg: str = "Success"
    data: Optional[Any] = None


class ApiResponse:
    @staticmethod
    def __response(code: int, msg: str, data: Optional[Any] = None) -> ResponseModel:
        return ResponseModel(code=code, msg=msg, data=data)
    
    @classmethod
    def success(cls, *, code: int = 200, msg: str = 'Success', data: Optional[Any] = None) -> Response:
        response_model = cls.__response(code=code, msg=msg, data=data)
        return cls(content=response_model.model_dump())
    
    @classmethod
    def fail(cls, *, code: int = 400, msg: str = 'Bad Request', data: Optional[Any] = None) -> Response:
        response_model = cls.__response(code=code, msg=msg, data=data)
        return cls(content=response_model.model_dump())
    
response_api = ApiResponse()

""" 示例
@app.get("/example-success")
async def example_success():
    return response_api.success(data={"key": "value"})

@app.get("/example-fail")
async def example_fail():
    return response_api.fail(msg="Something went wrong", data={"error": "details"})
"""

