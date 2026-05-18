from pydantic import BaseModel, Field
from typing import Optional, List, Literal


class TextGenerateRequest(BaseModel):
    prompt: str = Field(..., description="用户输入的主题或关键词", min_length=1, max_length=500)
    length: Literal["short", "medium", "long"] = Field(
        "medium", description="生成文本的长度"
    )
    style: Literal["formal", "casual", "humorous", "academic"] = Field(
        "formal", description="文本风格"
    )


class TextGenerateResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: dict = Field(..., description="返回的数据")
    response_time_ms: int = Field(..., description="响应时间（毫秒）")


class TextPolishRequest(BaseModel):
    text: str = Field(..., description="需要润色的原始文本", min_length=1, max_length=10000)
    intensity: Literal["light", "medium", "strong"] = Field(
        "medium", description="润色强度"
    )


class TextPolishResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: dict = Field(..., description="返回的数据")
    response_time_ms: int = Field(..., description="响应时间（毫秒）")


class TextRewriteRequest(BaseModel):
    text: str = Field(..., description="需要改写的原始文本", min_length=1, max_length=10000)
    style: Literal["concise", "detailed", "professional"] = Field(
        "concise", description="改写风格"
    )


class TextRewriteResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: dict = Field(..., description="返回的数据")
    response_time_ms: int = Field(..., description="响应时间（毫秒）")


class TextSummarizeRequest(BaseModel):
    text: str = Field(..., description="需要摘要的长文本", min_length=1, max_length=10000)
    ratio: float = Field(0.2, description="摘要长度比例（0.1-0.5）", ge=0.1, le=0.5)
    format: Literal["paragraph", "bullet"] = Field(
        "paragraph", description="摘要格式"
    )


class TextSummarizeResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: dict = Field(..., description="返回的数据")
    response_time_ms: int = Field(..., description="响应时间（毫秒）")


class TextOptimizeRequest(BaseModel):
    prompt: str = Field(..., description="需要优化的原始提示词", min_length=1, max_length=500)
    target_model: Literal["text", "image", "video", "audio"] = Field(
        "text", description="目标模型类型"
    )


class TextOptimizeResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: dict = Field(..., description="返回的数据")
    response_time_ms: int = Field(..., description="响应时间（毫秒）")


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="请求是否成功")
    error_code: str = Field(..., description="错误码")
    error_message: str = Field(..., description="错误信息")