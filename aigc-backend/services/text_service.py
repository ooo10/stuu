import time
import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

HAS_LLM = False
llm = None
ChatPromptTemplate = None
StrOutputParser = None

try:
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    API_KEY = os.getenv("OPENAI_API_KEY")
    
    llm = ChatOpenAI(
        model="glm-4",
        api_key=API_KEY,
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
    HAS_LLM = True
    print("智谱AI配置成功")
except Exception as e:
    print(f"智谱AI配置失败: {e}")


class TextService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def generate_text(
        self,
        prompt: str,
        length: Literal["short", "medium", "long"] = "medium",
        style: Literal["formal", "casual", "humorous", "academic"] = "formal"
    ) -> dict:
        """生成文本"""
        start_time = time.time()

        length_mapping = {
            "short": "约100-200字",
            "medium": "约300-500字",
            "long": "约800-1000字"
        }

        style_mapping = {
            "formal": "正式、专业的语气",
            "casual": "轻松、亲切的语气",
            "humorous": "幽默、风趣的语气",
            "academic": "学术、严谨的语气"
        }

        try:
            if HAS_LLM:
                template = ChatPromptTemplate.from_messages([
                    ("system", "你是一位专业的内容创作助手。请根据用户的要求生成高质量的文本内容。"),
                    ("human", "请围绕主题「{prompt}」创作一篇{length}的文章，要求使用{style}。")
                ])
                chain = template | llm | StrOutputParser()
                content = chain.invoke({
                    "prompt": prompt,
                    "length": length_mapping[length],
                    "style": style_mapping[style]
                })
            else:
                content = f"模拟生成关于「{prompt}」的{length_mapping[length]}文本内容，使用{style_mapping[style]}。这是一个示例响应，实际应用中需要配置智谱AI API Key。"

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "data": {
                    "content": content,
                    "word_count": len(content),
                    "style": style
                },
                "response_time_ms": response_time_ms
            }
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "error_code": "TR-E003",
                "error_message": f"服务调用失败: {str(e)}",
                "response_time_ms": response_time_ms
            }

    def polish_text(
        self,
        text: str,
        intensity: Literal["light", "medium", "strong"] = "medium"
    ) -> dict:
        """润色文本"""
        start_time = time.time()

        intensity_mapping = {
            "light": "轻度润色，保持原文风格，仅修正明显错误",
            "medium": "中度润色，优化表达和词汇，提升流畅度",
            "strong": "深度润色，全面优化结构、语法和表达方式"
        }

        try:
            if HAS_LLM:
                template = ChatPromptTemplate.from_messages([
                    ("system", "你是一位专业的文本润色专家。请根据用户的要求对文本进行润色。"),
                    ("human", "请对以下文本进行{intensity}：\n\n{text}\n\n请保留原文的核心含义不变。")
                ])
                chain = template | llm | StrOutputParser()
                polished = chain.invoke({
                    "intensity": intensity_mapping[intensity],
                    "text": text
                })
            else:
                polished = f"模拟润色后的文本：{text[:50]}...（实际应用中需要配置智谱AI API Key）"

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "data": {
                    "original": text,
                    "polished": polished,
                    "changes": ["词汇替换", "语法修正", "句式优化"]
                },
                "response_time_ms": response_time_ms
            }
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "error_code": "TR-E003",
                "error_message": f"服务调用失败: {str(e)}",
                "response_time_ms": response_time_ms
            }

    def rewrite_text(
        self,
        text: str,
        style: Literal["concise", "detailed", "professional"] = "concise"
    ) -> dict:
        """改写文本"""
        start_time = time.time()

        style_mapping = {
            "concise": "简洁明了，去除冗余",
            "detailed": "详细丰富，增加细节",
            "professional": "专业正式，适合商务场景"
        }

        try:
            if HAS_LLM:
                template = ChatPromptTemplate.from_messages([
                    ("system", "你是一位专业的文本改写专家。请根据用户的要求对文本进行改写。"),
                    ("human", "请将以下文本改写成{style}的风格：\n\n{text}\n\n请保持原文的核心含义不变。")
                ])
                chain = template | llm | StrOutputParser()
                rewritten = chain.invoke({
                    "style": style_mapping[style],
                    "text": text
                })
            else:
                rewritten = f"模拟改写后的文本：{text[:50]}...（实际应用中需要配置智谱AI API Key）"

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "data": {
                    "original": text,
                    "rewritten": rewritten,
                    "similarity_score": 0.85
                },
                "response_time_ms": response_time_ms
            }
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "error_code": "TR-E003",
                "error_message": f"服务调用失败: {str(e)}",
                "response_time_ms": response_time_ms
            }

    def summarize_text(
        self,
        text: str,
        ratio: float = 0.2,
        format_type: Literal["paragraph", "bullet"] = "paragraph"
    ) -> dict:
        """生成文本摘要"""
        start_time = time.time()

        format_mapping = {
            "paragraph": "段落形式",
            "bullet": "要点列表形式"
        }

        try:
            if HAS_LLM:
                template = ChatPromptTemplate.from_messages([
                    ("system", "你是一位专业的文本摘要专家。请根据用户的要求生成文本摘要。"),
                    ("human", "请对以下文本生成{format}的摘要，摘要长度约为原文的{ratio}%：\n\n{text}")
                ])
                chain = template | llm | StrOutputParser()
                summary = chain.invoke({
                    "format": format_mapping[format_type],
                    "ratio": int(ratio * 100),
                    "text": text
                })
            else:
                summary = f"模拟生成的摘要：{text[:30]}...（实际应用中需要配置智谱AI API Key）"

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "data": {
                    "original_length": len(text),
                    "summary": summary,
                    "summary_length": len(summary),
                    "key_points": ["要点1", "要点2", "要点3"]
                },
                "response_time_ms": response_time_ms
            }
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "error_code": "TR-E003",
                "error_message": f"服务调用失败: {str(e)}",
                "response_time_ms": response_time_ms
            }

    def optimize_prompt(
        self,
        prompt: str,
        target_model: Literal["text", "image", "video", "audio"] = "text"
    ) -> dict:
        """优化提示词"""
        start_time = time.time()

        model_mapping = {
            "text": "文本生成模型",
            "image": "图像生成模型（如DALL-E、Stable Diffusion）",
            "video": "视频生成模型",
            "audio": "音频生成模型"
        }

        try:
            if HAS_LLM:
                template = ChatPromptTemplate.from_messages([
                    ("system", "你是一位专业的提示词优化专家。请根据目标模型优化用户的提示词。"),
                    ("human", "请优化以下提示词，使其更适合{model}：\n\n{prompt}\n\n请提供优化前后的对比，并说明改进点。")
                ])
                chain = template | llm | StrOutputParser()
                optimized = chain.invoke({
                    "model": model_mapping[target_model],
                    "prompt": prompt
                })
            else:
                optimized = f"优化后的提示词：{prompt}（增加细节描述，明确风格要求）"

            response_time_ms = int((time.time() - start_time) * 1000)

            return {
                "success": True,
                "data": {
                    "original": prompt,
                    "optimized": optimized,
                    "improvements": ["增加细节描述", "明确风格要求", "添加约束条件"]
                },
                "response_time_ms": response_time_ms
            }
        except Exception as e:
            response_time_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "error_code": "TR-E003",
                "error_message": f"服务调用失败: {str(e)}",
                "response_time_ms": response_time_ms
            }


text_service = TextService()