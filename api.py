from fastapi import FastAPI
from pydantic import BaseModel
from difflib import SequenceMatcher

app=FastAPI(title='AI Customer Support API',version='1.0.0')
FAQ=[('refund','You can request a refund within 7 days through the billing page.'),('password','Use the password reset link on the sign-in page.'),('shipping','Standard delivery usually takes 3 to 5 business days.'),('cancel','Orders can be cancelled before fulfillment starts.'),('contact','A human support agent can be requested at any time.')]
class Chat(BaseModel): message:str
@app.get('/health')
def health(): return {'status':'ok','service':'ai-customer-support'}
@app.post('/chat')
def chat(body:Chat):
    text=body.message.lower().strip(); best=(0,'contact','I can connect you with a human support agent.')
    for intent,answer in FAQ:
        s=SequenceMatcher(None,text,intent).ratio()
        if intent in text:s=max(s,.9)
        if s>best[0]:best=(s,intent,answer)
    confidence=round(best[0],2)
    return {'reply':best[2],'intent':best[1],'confidence':confidence,'escalate':confidence<0.45}
