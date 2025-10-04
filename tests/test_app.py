import pytest
from app import create_app
from config import Config

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'

def test_index_endpoint(client):
    """Test index endpoint"""
    response = client.get('/')
    assert response.status_code == 200

def test_search_endpoint_missing_data(client):
    """Test search endpoint with missing data"""
    response = client.post('/api/search', json={})
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] == False
    assert 'error' in data

def test_search_endpoint_empty_data(client):
    """Test search endpoint with empty data"""
    response = client.post('/api/search', json={
        'gemini_api_key': '',
        'scraper_api_key': '',
        'product_name': ''
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] == False