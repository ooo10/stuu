from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from schemas.text import (
    TextGenerateRequest,
    TextGenerateResponse,
    TextPolishRequest,
    TextPolishResponse,
    TextRewriteRequest,
    TextRewriteResponse,
    TextSummarizeRequest,
    TextSummarizeResponse,
    TextOptimizeRequest,
    TextOptimizeResponse,
    ErrorResponse
)

from services.text_service import text_service

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


@router.post(
    "/generate",
    response_model=TextGenerateResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="文本生成",
    description="根据用户输入的主题或关键词生成文本内容"
)
async def generate_text(request: TextGenerateRequest, token: str = Depends(oauth2_scheme)):
    """
    根据用户输入的主题或关键词生成文本内容
    
    - **prompt**: 用户输入的主题或关键词（必填）
    - **length**: 生成文本的长度，可选值：short（短）、medium（中）、long（长），默认medium
    - **style**: 文本风格，可选值：formal（正式）、casual（轻松）、humorous（幽默）、academic（学术），默认formal
    
    返回生成的文本内容、字数统计和响应时间
    """
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E001", "error_message": "参数格式错误：prompt不能为空"}
        )
    
    result = text_service.generate_text(
        prompt=request.prompt,
        length=request.length,
        style=request.style
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error_code": result["error_code"], "error_message": result["error_message"]}
        )
    
    return result


@router.post(
    "/polish",
    response_model=TextPolishResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="文本润色",
    description="对原始文本进行润色优化"
)
async def polish_text(request: TextPolishRequest, token: str = Depends(oauth2_scheme)):
    """
    对原始文本进行润色优化
    
    - **text**: 需要润色的原始文本（必填）
    - **intensity**: 润色强度，可选值：light（轻度）、medium（中度）、strong（深度），默认medium
    
    返回润色前后的文本对比和修改说明
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E001", "error_message": "参数格式错误：text不能为空"}
        )
    
    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E002", "error_message": "文本长度超限：最大支持10000字符"}
        )
    
    result = text_service.polish_text(
        text=request.text,
        intensity=request.intensity
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error_code": result["error_code"], "error_message": result["error_message"]}
        )
    
    return result


@router.post(
    "/rewrite",
    response_model=TextRewriteResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="文本改写",
    description="将原文改写成指定风格"
)
async def rewrite_text(request: TextRewriteRequest, token: str = Depends(oauth2_scheme)):
    """
    将原文改写成指定风格
    
    - **text**: 需要改写的原始文本（必填）
    - **style**: 改写风格，可选值：concise（简洁）、detailed（详细）、professional（专业），默认concise
    
    返回改写前后的文本对比和相似度评分
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E001", "error_message": "参数格式错误：text不能为空"}
        )
    
    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E002", "error_message": "文本长度超限：最大支持10000字符"}
        )
    
    result = text_service.rewrite_text(
        text=request.text,
        style=request.style
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error_code": result["error_code"], "error_message": result["error_message"]}
        )
    
    return result


@router.post(
    "/summarize",
    response_model=TextSummarizeResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="文本摘要",
    description="对长文本生成摘要"
)
async def summarize_text(request: TextSummarizeRequest, token: str = Depends(oauth2_scheme)):
    """
    对长文本生成摘要
    
    - **text**: 需要摘要的长文本（必填）
    - **ratio**: 摘要长度比例（0.1-0.5），默认0.2
    - **format**: 摘要格式，可选值：paragraph（段落）、bullet（要点列表），默认paragraph
    
    返回摘要内容、原文和摘要长度、关键要点
    """
    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E001", "error_message": "参数格式错误：text不能为空"}
        )
    
    if len(request.text) > 10000:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E002", "error_message": "文本长度超限：最大支持10000字符"}
        )
    
    result = text_service.summarize_text(
        text=request.text,
        ratio=request.ratio,
        format_type=request.format
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error_code": result["error_code"], "error_message": result["error_message"]}
        )
    
    return result


@router.post(
    "/optimize",
    response_model=TextOptimizeResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="提示词优化",
    description="优化提示词以获得更好的生成效果"
)
async def optimize_prompt(request: TextOptimizeRequest, token: str = Depends(oauth2_scheme)):
    """
    优化提示词以获得更好的生成效果
    
    - **prompt**: 需要优化的原始提示词（必填）
    - **target_model**: 目标模型类型，可选值：text、image、video、audio，默认text
    
    返回优化前后的提示词对比和改进说明
    """
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error_code": "TR-E001", "error_message": "参数格式错误：prompt不能为空"}
        )
    
    result = text_service.optimize_prompt(
        prompt=request.prompt,
        target_model=request.target_model
    )
    
    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error_code": result["error_code"], "error_message": result["error_message"]}
        )
    
    return result