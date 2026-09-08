from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app=FastAPI(title='AI Customer Support API',version='3.0.0')
FAQ=[('refund','You can request a refund within 7 days through the billing page.'),('password','Use the password reset link on the sign-in page.'),('shipping','Standard delivery usually takes 3 to 5 business days.'),('cancel','Orders can be cancelled before fulfillment starts.'),('contact','A human support agent can be requested at any time.')]
texts=[i+' '+a for i,a in FAQ]; vectorizer=TfidfVectorizer(stop_words='english'); matrix=vectorizer.fit_transform(texts)
class Chat(BaseModel): message:str=Field(min_length=1,max_length=2000)
@app.get('/health')
def health():return {'status':'ok','service':'ai-customer-support','version':'3.0.0','engine':'tfidf-retrieval'}
@app.get('/faqs')
def faqs():return [{'intent':i,'answer':a} for i,a in FAQ]
@app.post('/chat')
def chat(body:Chat):
    q=vectorizer.transform([body.message]); sims=cosine_similarity(q,matrix)[0]; idx=int(sims.argmax()); confidence=round(float(sims[idx]),2)
    if confidence<0.12:return {'reply':'I am not confident enough to answer this. A human support agent should review your request.','intent':'unknown','confidence':confidence,'escalate':True}
    intent,answer=FAQ[idx];return {'reply':answer,'intent':intent,'confidence':confidence,'escalate':confidence<0.35}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
