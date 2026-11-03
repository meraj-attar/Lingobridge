"""Registration-time policy. Existing hashed passwords remain valid on login."""
import re
from fastapi import HTTPException

COMMON={"password", "password123", "password123!", "12345678", "123456789", "qwerty123", "admin123", "welcome123", "iloveyou", "letmein123"}

def password_errors(password: str) -> list[str]:
    errors=[]
    if len(password)<8 or len(password)>128:errors.append('Use 8–128 characters')
    if not re.search(r'[A-Z]',password):errors.append('Add an uppercase letter')
    if not re.search(r'[a-z]',password):errors.append('Add a lowercase letter')
    if not re.search(r'[0-9]',password):errors.append('Add a number')
    if not re.search(r'[^A-Za-z0-9]',password):errors.append('Add a special character')
    normalized=re.sub(r'[^a-z0-9]', '',password.lower())
    if password.lower() in COMMON or normalized in {re.sub(r'[^a-z0-9]', '',p) for p in COMMON}:
        errors.append('Choose a less common password')
    return errors

def validate_password(password: str) -> None:
    problems=password_errors(password)
    if problems:raise HTTPException(422,detail='Password requirements: '+ '; '.join(problems))
