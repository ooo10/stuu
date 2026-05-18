import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestImageModule:
    def test_generate_image_success(self):
        response = client.post(
            "/api/image/generate",
            json={"prompt": "a beautiful sunset over the ocean"},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "data" in data
        assert "images" in data["data"]
        assert len(data["data"]["images"]) > 0
        assert "prompt" in data["data"]
        assert "style" in data["data"]
        assert "size" in data["data"]

    def test_generate_image_with_style(self):
        response = client.post(
            "/api/image/generate",
            json={
                "prompt": "a cute cat",
                "style": "cartoon",
                "size": "512x512",
                "num_images": 1
            },
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["data"]["style"] == "cartoon"
        assert data["data"]["size"] == "512x512"

    def test_generate_image_multiple(self):
        response = client.post(
            "/api/image/generate",
            json={
                "prompt": "abstract art",
                "num_images": 3
            },
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert len(data["data"]["images"]) == 3

    def test_generate_image_empty_prompt(self):
        response = client.post(
            "/api/image/generate",
            json={"prompt": ""},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 422

    def test_generate_image_prompt_too_long(self):
        long_prompt = "a" * 1001
        response = client.post(
            "/api/image/generate",
            json={"prompt": long_prompt},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 422

    def test_generate_image_unauthorized(self):
        response = client.post(
            "/api/image/generate",
            json={"prompt": "test"}
        )
        assert response.status_code == 401

    def test_generate_image_with_different_styles(self):
        styles = ["realistic", "cartoon", "abstract", "anime", "photographic"]
        for style in styles:
            response = client.post(
                "/api/image/generate",
                json={"prompt": f"test image in {style} style", "style": style},
                headers={"Authorization": "Bearer test-token"}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["data"]["style"] == style

    def test_generate_image_response_time(self):
        response = client.post(
            "/api/image/generate",
            json={"prompt": "test response time"},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "response_time_ms" in data
        assert isinstance(data["response_time_ms"], int)
        assert data["response_time_ms"] >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])