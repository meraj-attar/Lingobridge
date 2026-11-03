"""Interactive administrator account bootstrap / password reset. Never writes credentials to output."""
import getpass
from email_validator import validate_email, EmailNotValidError
from sqlalchemy import select
from .db import SessionLocal
from .models import User,Role
from .security import hash_password
from .main import uid

def main():
    print('LingoBridge administrator setup (run after migration + seed)')
    email=input('Administrator email: ').strip().lower()
    try:email=validate_email(email,check_deliverability=False).normalized
    except EmailNotValidError as exc:raise SystemExit(str(exc))
    name=input('Full name: ').strip()
    if len(name)<2:raise SystemExit('Name must contain at least 2 characters')
    pwd=getpass.getpass('New password (minimum 12 characters): ')
    repeat=getpass.getpass('Confirm password: ')
    if pwd!=repeat or len(pwd)<12:raise SystemExit('Password invalid or does not match')
    with SessionLocal.begin() as db:
        if not db.get(Role,'admin'):raise SystemExit('Run database migrations and seed first')
        user=db.scalar(select(User).where(User.email==email))
        if user:
            if user.role!='admin':raise SystemExit('This address is a student. Refusing automatic privilege escalation.')
            user.password_hash=hash_password(pwd);user.is_active=True
            print('Existing administrator password securely updated.')
        else:
            db.add(User(id=uid(),email=email,full_name=name,password_hash=hash_password(pwd),role='admin'))
            print('New administrator created.')
if __name__=='__main__':main()
