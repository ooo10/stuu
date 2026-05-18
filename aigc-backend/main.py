from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from routers import auth, text, image

load_dotenv()

app = FastAPI(
    title="AIGC实训平台 API",
    description="AIGC实训平台后端接口文档",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(text.router, prefix="/api/text", tags=["文本模块"])
app.include_router(image.router, prefix="/api/image", tags=["图片模块"])

@app.get("/")
async def root():
    return {"message": "AIGC实训平台 API 服务已启动"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}