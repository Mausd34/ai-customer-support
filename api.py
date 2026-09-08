from fastapi import FastAPI,HTTPException,Depends
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from pydantic import BaseModel,Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.auth import hash_password,create_token,verify_token
from app.db import connect,init_db
app=FastAPI(title='AI Customer Support API',version='4.0.0');init_db();security=HTTPBearer(auto_error=False)
FAQ=[('refund','You can request a refund within 7 days through the billing page.'),('password','Use the password reset link on the sign-in page.'),('shipping','Standard delivery usually takes 3 to 5 business days.'),('cancel','Orders can be cancelled before fulfillment starts.'),('contact','A human support agent can be requested at any time.')]
texts=[i+' '+a for i,a in FAQ];vectorizer=TfidfVectorizer(stop_words='english');matrix=vectorizer.fit_transform(texts)
class Credentials(BaseModel):username:str=Field(min_length=3,max_length=80);password:str=Field(min_length=6,max_length=200)
class Chat(BaseModel):message:str=Field(min_length=1,max_length=2000)
def current_user(c:HTTPAuthorizationCredentials=Depends(security)):
    if not c:raise HTTPException(401,'Authentication required')
    u=verify_token(c.credentials)
    if not u:raise HTTPException(401,'Invalid or expired token')
    return u
@app.get('/health')
def health():return {'status':'ok','service':'ai-customer-support','version':'4.0.0','engine':'tfidf-retrieval'}
@app.post('/auth/register')
def register(b:Credentials):
    with connect() as c:
        if c.execute('SELECT 1 FROM users WHERE username=?',(b.username,)).fetchone():raise HTTPException(409,'Username already exists')
        c.execute('INSERT INTO users(username,password_hash) VALUES(?,?)',(b.username,hash_password(b.password)));c.commit()
    return {'message':'registered','username':b.username}
@app.post('/auth/login')
def login(b:Credentials):
    with connect() as c:u=c.execute('SELECT * FROM users WHERE username=?',(b.username,)).fetchone()
    if not u or u['password_hash']!=hash_password(b.password):raise HTTPException(401,'Invalid username or password')
    return {'access_token':create_token(u['username']),'token_type':'bearer'}
@app.get('/auth/me')
def me(u=Depends(current_user)):return u
@app.get('/faqs')
def faqs():return [{'intent':i,'answer':a} for i,a in FAQ]
@app.post('/chat')
def chat(body:Chat,u=Depends(current_user)):
    q=vectorizer.transform([body.message]);sims=cosine_similarity(q,matrix)[0];idx=int(sims.argmax());confidence=round(float(sims[idx]),2)
    if confidence<0.12:return {'reply':'I am not confident enough to answer this. A human support agent should review your request.','intent':'unknown','confidence':confidence,'escalate':True,'user':u['username']}
    intent,answer=FAQ[idx];return {'reply':answer,'intent':intent,'confidence':confidence,'escalate':confidence<0.35,'user':u['username']}
app.mount('/',StaticFiles(directory='web',html=True),name='web')
