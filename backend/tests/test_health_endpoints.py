"""
Tests for health check endpoints.

This module contains tests for the health check endpoints to ensure
they return the correct status and format.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path to import the app
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from numerology_app.main import app


class TestHealthEndpoints:
    """Test cases for health check endpoints."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    def test_root_healthz_endpoint(self):
        """Test the root /healthz endpoint."""
        response = self.client.get("/healthz")
        
        assert response.status_code == 200
        data = response.json()
        assert "ok" in data
        assert data["ok"] is True
    
    def test_api_healthz_endpoint(self):
        """Test the /api/healthz endpoint."""
        response = self.client.get("/api/healthz")
        
        assert response.status_code == 200
        data = response.json()
        assert "ok" in data
        assert data["ok"] is True
        assert "status" in data
        assert data["status"] == "healthy"
        assert "service" in data
        assert data["service"] == "numerology-api"
    
    def test_health_endpoints_response_format(self):
        """Test that health endpoints return the correct format."""
        endpoints = ["/healthz", "/api/healthz"]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 200
            
            data = response.json()
            assert isinstance(data, dict)
            assert "ok" in data
            assert isinstance(data["ok"], bool)
            assert data["ok"] is True
    
    def test_health_endpoints_are_fast(self):
        """Test that health endpoints respond quickly."""
        import time
        
        endpoints = ["/healthz", "/api/healthz"]
        
        for endpoint in endpoints:
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            assert response.status_code == 200
            assert response_time < 1.0, f"Health endpoint {endpoint} took {response_time:.3f} seconds"
    
    def test_health_endpoints_with_different_methods(self):
        """Test that health endpoints only accept GET requests."""
        endpoints = ["/healthz", "/api/healthz"]
        
        for endpoint in endpoints:
            # GET should work
            response = self.client.get(endpoint)
            assert response.status_code == 200
            
            # POST should not work
            response = self.client.post(endpoint)
            assert response.status_code == 405  # Method Not Allowed
            
            # PUT should not work
            response = self.client.put(endpoint)
            assert response.status_code == 405  # Method Not Allowed
            
            # DELETE should not work
            response = self.client.delete(endpoint)
            assert response.status_code == 405  # Method Not Allowed
    
    def test_health_endpoints_headers(self):
        """Test that health endpoints return appropriate headers."""
        endpoints = ["/healthz", "/api/healthz"]
        
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            assert response.status_code == 200
            
            # Should have content-type header
            assert "content-type" in response.headers
            assert "application/json" in response.headers["content-type"]
    
    def test_health_endpoints_consistency(self):
        """Test that health endpoints return consistent responses."""
        endpoints = ["/healthz", "/api/healthz"]
        
        # Make multiple requests to ensure consistency
        for endpoint in endpoints:
            responses = []
            for _ in range(5):
                response = self.client.get(endpoint)
                assert response.status_code == 200
                responses.append(response.json())
            
            # All responses should be identical
            first_response = responses[0]
            for response in responses[1:]:
                assert response == first_response


class TestHealthEndpointIntegration:
    """Integration tests for health endpoints."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = TestClient(app)
    
    def test_health_endpoints_with_other_endpoints(self):
        """Test that health endpoints work alongside other endpoints."""
        # Test health endpoints
        health_response = self.client.get("/healthz")
        assert health_response.status_code == 200
        
        api_health_response = self.client.get("/api/healthz")
        assert api_health_response.status_code == 200
        
        # Test that other endpoints still work
        # (This assumes there are other endpoints available)
        try:
            # Try to access the root endpoint
            root_response = self.client.get("/")
            # Root endpoint might not exist, so we just check it doesn't crash
            assert root_response.status_code in [200, 404]
        except Exception:
            # It's okay if the root endpoint doesn't exist
            pass
    
    def test_health_endpoints_under_load(self):
        """Test health endpoints under simulated load."""
        import concurrent.futures
        import time
        
        def make_health_request(endpoint):
            """Make a health request and return the response time."""
            start_time = time.time()
            response = self.client.get(endpoint)
            end_time = time.time()
            
            return {
                "status_code": response.status_code,
                "response_time": end_time - start_time,
                "data": response.json()
            }
        
        endpoints = ["/healthz", "/api/healthz"]
        
        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for _ in range(20):  # 20 concurrent requests
                for endpoint in endpoints:
                    future = executor.submit(make_health_request, endpoint)
                    futures.append(future)
            
            # Collect results
            results = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                results.append(result)
        
        # All requests should succeed
        for result in results:
            assert result["status_code"] == 200
            assert result["data"]["ok"] is True
            assert result["response_time"] < 2.0  # Should respond within 2 seconds
        
        # Calculate average response time
        avg_response_time = sum(r["response_time"] for r in results) / len(results)
        assert avg_response_time < 1.0, f"Average response time: {avg_response_time:.3f} seconds"


if __name__ == "__main__":
    # Run tests if executed directly
    pytest.main([__file__, "-v"])
