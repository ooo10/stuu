from fastapi import APIRouter, HTTPException

from schemas.image import (
    ImageGenerateRequest,
    ImageGenerateResponse,
    ErrorResponse
)

from services.image_service import image_service

router = APIRouter()


@router.post(
    "/generate",
    response_model=ImageGenerateResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="图片生成",
    description="根据提示词生成图片"
)
async def generate_image(request: ImageGenerateRequest):
    """
    根据提示词生成图片
    
    - **prompt**: 图片生成提示词（必填）
    - **style**: 图片风格，可选值：realistic（写实）、cartoon（卡通）、abstract（抽象）、anime（动漫）、photographic（摄影），默认realistic
    - **size**: 图片尺寸，可选值：512x512、1024x1024、1024x1792，默认512x512
    - **num_images**: 生成图片数量，范围1-4，默认1
    
    返回生成的图片URL列表、使用的提示词、风格和尺寸
    """
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "IMG-E001", "error_message": "参数格式错误：prompt不能为空"}
        )
    
    if len(request.prompt) > 1000:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "IMG-E002", "error_message": "提示词长度超限：最大支持1000字符"}
        )
    
    result = image_service.generate_image(
        prompt=request.prompt,
        style=request.style,
        size=request.size,
        num_images=request.num_images
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error_code": result["error_code"], "error_message": result["error_message"]}
        )
    
    return result
