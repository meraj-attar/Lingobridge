import os, secrets, hashlib, hmac
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .db import get_db
from .models import User

SECRET = os.getenv('JWT_SECRET','')
if len(SECRET) < 32 and os.getenv('ENVIRONMENT','development') == 'production':
    raise RuntimeError('JWT_SECRET must be set to at least 32 characters in production')
if not SECRET:
    # development-only ephemeral key: sessions invalidate on backend restart
    SECRET = secrets.token_urlsafe(48)
COOKIE = 'lingobridge_session'

def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 390000)
    return 'pbkdf2_sha256$390000$'+salt.hex()+'$'+digest.hex()

def verify_password(password, encoded):
    try:
        _, rounds, salt, digest = encoded.split('$')
        expected=hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), int(rounds))
        return hmac.compare_digest(expected,bytes.fromhex(digest))
    except (ValueError, AttributeError):
        return False

def create_session(user):
    csrf = secrets.token_urlsafe(28)
    token = jwt.encode({'sub':user.id, 'csrf':csrf, 'exp':datetime.now(timezone.utc)+timedelta(hours=12), 'iss':'lingobridge'}, SECRET, algorithm='HS256')
    return token, csrf

def current_user(request: Request, db:Session=Depends(get_db)):
    token=request.cookies.get(COOKIE)
    if not token: raise HTTPException(401,'Please sign in')
    try:
        payload=jwt.decode(token, SECRET, algorithms=['HS256'], issuer='lingobridge',
                           options={'require':['exp','sub','csrf','iss']})
        if not isinstance(payload.get('sub'),str) or not payload['sub'] or not isinstance(payload.get('csrf'),str) or not payload['csrf']:
            raise jwt.InvalidTokenError('Incomplete session claims')
    except jwt.PyJWTError: raise HTTPException(401,'Session expired or invalid')
    user=db.get(User,payload['sub'])
    if not user or not user.is_active: raise HTTPException(401,'Account unavailable')
    if request.method not in ('GET','HEAD','OPTIONS') and not hmac.compare_digest(request.headers.get('X-CSRF-Token',''),payload['csrf']):
        raise HTTPException(403,'Invalid CSRF token')
    request.state.csrf=payload['csrf']
    return user

def admin_user(user:User=Depends(current_user)):
    if user.role!='admin': raise HTTPException(403,'Administrator permission required')
    return user
