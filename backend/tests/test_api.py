"""
API Integration tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHCPEndpoints:
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_create_hcp(self):
        """Test creating HCP"""
        hcp_data = {
            "name": "Dr. Test",
            "specialty": "Cardiology",
            "organization": "Test Hospital",
            "email": "test@example.com",
            "phone": "555-1234",
            "location": "New York"
        }
        response = client.post("/api/hcps/", json=hcp_data)
        assert response.status_code == 200
        assert response.json()["name"] == "Dr. Test"
    
    def test_list_hcps(self):
        """Test listing HCPs"""
        response = client.get("/api/hcps/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

class TestInteractionEndpoints:
    
    def test_chat_message(self):
        """Test chat message endpoint"""
        chat_data = {
            "message": "Test interaction with HCP",
            "hcp_id": 1
        }
        response = client.post("/api/chat/message", json=chat_data)
        assert response.status_code in [200, 404]  # May not have HCP created

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
