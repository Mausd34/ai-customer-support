from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health(): assert client.get('/health').status_code==200
def test_chat():
    r=client.post('/chat',json={'message':'I need a refund'})
    assert r.status_code==200
    assert 'reply' in r.json()
