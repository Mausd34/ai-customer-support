"""Signed-token authentication foundation; replace demo secret with a production secret."""
from datetime import datetime,timedelta,timezone
import hashlib,hmac,os,secrets
SECRET_KEY=os.getenv("JWT_SECRET","change-me-in-production")
def hash_password(password:str)->str:return hashlib.sha256(password.encode()).hexdigest()
def create_token(username:str,minutes:int=60)->str:
 exp=int((datetime.now(timezone.utc)+timedelta(minutes=minutes)).timestamp()); nonce=secrets.token_hex(8); p=f"{username}.{exp}.{nonce}"; s=hmac.new(SECRET_KEY.encode(),p.encode(),hashlib.sha256).hexdigest(); return f"{p}.{s}"
def verify_token(token:str):
 try:
  u,e,n,s=token.split('.'); p=f"{u}.{e}.{n}"; x=hmac.new(SECRET_KEY.encode(),p.encode(),hashlib.sha256).hexdigest(); return u if hmac.compare_digest(s,x) and int(e)>=int(datetime.now(timezone.utc).timestamp()) else None
 except Exception:return None
