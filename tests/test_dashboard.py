from fastapi.testclient import TestClient
from api import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_chat():
    r=client.post('/chat',json={'message':'I need a refund'}); assert r.status_code==200; assert r.json()['intent']=='refund'
