import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
        
def test_valid_shorten(client):
    res = client.post("/api/shorten", json={"url": "https://example.com"})
    assert res.status_code == 201
    data = res.get_json()
    assert "short_code" in data
    
def test_invalid_url(client):
    res = client.post("/api/shorten", json={"url": "badurl"})
    assert res.status_code == 400

def test_missing_url(client):
    res = client.post("/api/shorten", json={})
    assert res.status_code == 400

def test_redirect(client):
    res = client.post("/api/shorten", json={"url": "https://google.com"})
    short_code = res.get_json()["short_code"]
    redirect_res = client.get(f"/{short_code}")
    assert redirect_res.status_code == 302

def test_stats(client):
    res = client.post("/api/shorten", json={"url": "https://github.com"})
    short_code = res.get_json()["short_code"]
    client.get(f"/{short_code}")
    stats = client.get(f"/api/stats/{short_code}").get_json()
    assert stats["clicks"] == 1
    assert stats["url"] == "https://github.com"
    
def test_multiple_redirects_increment_clicks(client):
    res = client.post("/api/shorten", json={"url": "https://test.com"})
    short_code = res.get_json()["short_code"]
    for _ in range(5):
        client.get(f"/{short_code}")
    stats = client.get(f"/api/stats/{short_code}").get_json()
    assert stats["clicks"] == 5

def test_nonexistent_stats(client):
    res = client.get("/api/stats/invalidcode")
    assert res.status_code == 404
    
def test_nonexistent_short_code(client):
    res = client.get("/nonexistent")
    assert res.status_code == 404

def test_duplicate_url_returns_same_code(client):
    res1 = client.post("/api/shorten", json={"url": "https://openai.com"})
    res2 = client.post("/api/shorten", json={"url": "https://openai.com"})
    assert res1.get_json()["short_code"] == res2.get_json()["short_code"]
