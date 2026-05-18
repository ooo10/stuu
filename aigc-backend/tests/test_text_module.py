import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app
from services.text_service import TextService

client = TestClient(app)


class TestTextGenerate:
    """文本生成API测试"""

    def test_generate_text_success(self):
        """测试文本生成成功"""
        with patch.object(TextService, 'generate_text') as mock_generate:
            mock_generate.return_value = {
                "success": True,
                "data": {
                    "content": "测试生成的文本内容",
                    "word_count": 20,
                    "style": "formal"
                },
                "response_time_ms": 1500
            }

            response = client.post(
                "/api/text/generate",
                json={"prompt": "人工智能", "length": "medium", "style": "formal"},
                headers={"Authorization": "Bearer test-token"}
            )

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "content" in response.json()["data"]
            assert response.json()["data"]["style"] == "formal"

    def test_generate_text_empty_prompt(self):
        """测试空prompt返回错误"""
        response = client.post(
            "/api/text/generate",
            json={"prompt": "", "length": "medium", "style": "formal"},
            headers={"Authorization": "Bearer test-token"}
        )

        assert response.status_code == 422

    def test_generate_text_service_failure(self):
        """测试服务调用失败"""
        with patch.object(TextService, 'generate_text') as mock_generate:
            mock_generate.return_value = {
                "success": False,
                "error_code": "TR-E003",
                "error_message": "服务调用失败",
                "response_time_ms": 500
            }

            response = client.post(
                "/api/text/generate",
                json={"prompt": "测试", "length": "medium", "style": "formal"},
                headers={"Authorization": "Bearer test-token"}
            )

            assert response.status_code == 500
            assert "detail" in response.json()


class TestTextPolish:
    """文本润色API测试"""

    def test_polish_text_success(self):
        """测试文本润色成功"""
        with patch.object(TextService, 'polish_text') as mock_polish:
            mock_polish.return_value = {
                "success": True,
                "data": {
                    "original": "原文本",
                    "polished": "润色后的文本",
                    "changes": ["词汇替换"]
                },
                "response_time_ms": 800
            }

            response = client.post(
                "/api/text/polish",
                json={"text": "这是一段需要润色的文本", "intensity": "medium"},
                headers={"Authorization": "Bearer test-token"}
            )

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "polished" in response.json()["data"]

    def test_polish_text_empty_text(self):
        """测试空文本返回错误"""
        response = client.post(
            "/api/text/polish",
            json={"text": "", "intensity": "medium"},
            headers={"Authorization": "Bearer test-token"}
        )

        assert response.status_code == 422

    def test_polish_text_exceeds_length(self):
        """测试文本过长返回错误"""
        long_text = "a" * 10001
        response = client.post(
            "/api/text/polish",
            json={"text": long_text, "intensity": "medium"},
            headers={"Authorization": "Bearer test-token"}
        )

        assert response.status_code == 422


class TestTextRewrite:
    """文本改写API测试"""

    def test_rewrite_text_success(self):
        """测试文本改写成功"""
        with patch.object(TextService, 'rewrite_text') as mock_rewrite:
            mock_rewrite.return_value = {
                "success": True,
                "data": {
                    "original": "原文",
                    "rewritten": "改写后的文本",
                    "similarity_score": 0.85
                },
                "response_time_ms": 1200
            }

            response = client.post(
                "/api/text/rewrite",
                json={"text": "需要改写的文本", "style": "concise"},
                headers={"Authorization": "Bearer test-token"}
            )

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "rewritten" in response.json()["data"]


class TestTextSummarize:
    """文本摘要API测试"""

    def test_summarize_text_success(self):
        """测试文本摘要成功"""
        with patch.object(TextService, 'summarize_text') as mock_summarize:
            mock_summarize.return_value = {
                "success": True,
                "data": {
                    "original_length": 1000,
                    "summary": "摘要内容",
                    "summary_length": 200,
                    "key_points": ["要点1", "要点2"]
                },
                "response_time_ms": 2000
            }

            response = client.post(
                "/api/text/summarize",
                json={"text": "这是一段需要生成摘要的长文本内容", "ratio": 0.2, "format": "paragraph"},
                headers={"Authorization": "Bearer test-token"}
            )

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "summary" in response.json()["data"]


class TestTextOptimize:
    """提示词优化API测试"""

    def test_optimize_prompt_success(self):
        """测试提示词优化成功"""
        with patch.object(TextService, 'optimize_prompt') as mock_optimize:
            mock_optimize.return_value = {
                "success": True,
                "data": {
                    "original": "原提示词",
                    "optimized": "优化后的提示词",
                    "improvements": ["增加细节"]
                },
                "response_time_ms": 600
            }

            response = client.post(
                "/api/text/optimize",
                json={"prompt": "画一只猫", "target_model": "image"},
                headers={"Authorization": "Bearer test-token"}
            )

            assert response.status_code == 200
            assert response.json()["success"] == True
            assert "optimized" in response.json()["data"]


class TestTextServiceUnit:
    """文本服务单元测试"""

    def test_generate_text_default_parameters(self):
        """测试文本生成默认参数"""
        service = TextService()
        result = service.generate_text("测试主题")
        
        assert result["success"] == True
        assert "content" in result["data"]
        assert result["data"]["style"] == "formal"

    def test_generate_text_custom_parameters(self):
        """测试文本生成自定义参数"""
        service = TextService()
        result = service.generate_text("测试", length="short", style="casual")
        
        assert result["success"] == True
        assert result["data"]["style"] == "casual"

    def test_polish_text_various_intensity(self):
        """测试不同润色强度"""
        service = TextService()
        for intensity in ["light", "medium", "strong"]:
            result = service.polish_text("测试文本", intensity=intensity)
            assert result["success"] == True

    def test_service_singleton(self):
        """测试服务单例模式"""
        service1 = TextService()
        service2 = TextService()
        assert service1 is service2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])