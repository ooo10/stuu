from pydantic import BaseModel, Field
from typing import Optional, Literal


class ImageGenerateRequest(BaseModel):
    prompt: str = Field(..., description="图片生成提示词", min_length=1, max_length=1000)
    style: Optional[Literal["realistic", "cartoon", "abstract", "anime", "photographic"]] = Field(
        "realistic", description="图片风格"
    )
    size: Optional[Literal["512x512", "1024x1024", "1024x1792"]] = Field(
        "512x512", description="图片尺寸"
    )
    num_images: Optional[int] = Field(1, description="生成图片数量", ge=1, le=4)


class ImageGenerateResponse(BaseModel):
    success: bool = Field(True, description="请求是否成功")
    data: dict = Field(..., description="返回的数据")
    response_time_ms: int = Field(..., description="响应时间（毫秒）")


class ErrorResponse(BaseModel):
    success: bool = Field(False, description="请求是否成功")
    error_code: str = Field(..., description="错误码")
    error_message: str = Field(..., description="错误信息")