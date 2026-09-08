from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from difflib import SequenceMatcher

app=FastAPI(title='AI Customer Support API',version='2.0.0')
FAQ=[('refund','You can request a refund within 7 days through the billing page.'),('password','Use the password reset link on the sign-in page.'),('shipping','Standard delivery usually takes 3 to 5 business days.'),('cancel','Orders can be cancelled before fulfillment starts.'),('contact','A human support agent can be requested at any time.')]
class Chat(BaseModel): message:str=Field(min_length=1,max_length=2000)
@app.get('/health')
def health(): return {'status':'ok','service':'ai-customer-support','version':'2.0.0'}
@app.get('/faqs')
def faqs(): return [{'intent':i,'answer':a} for i,a in FAQ]
@app.post('/chat')
def chat(body:Chat):
    text=body.message.lower().strip(); best=(0,'contact','I can connect you with a human support agent.')
    for intent,answer in FAQ:
        s=SequenceMatcher(None,text,intent).ratio()
        if intent in text:s=max(s,.9)
        if s>best[0]:best=(s,intent,answer)
    confidence=round(best[0],2)
    return {'reply':best[2],'intent':best[1],'confidence':confidence,'escalate':confidence<0.45}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
