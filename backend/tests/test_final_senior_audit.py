"""Independent QA additions; uses only test_integration's disposable SQLite DB."""
from datetime import datetime, timedelta, timezone
import uuid
import jwt
import pytest
from fastapi.testclient import TestClient
from test_integration import app, SessionLocal, make_admin, login
from app import models as m
from app.security import SECRET, COOKIE, hash_password


def _staff():
    make_admin()
    client=TestClient(app)
    login(client, 'admin@example.com', 'AdminPassword123!')
    return client


def _students():
    prefix='qa-page-'+uuid.uuid4().hex[:8]
    ids=[]
    with SessionLocal.begin() as db:
        for index in range(7):
            ident=prefix+str(index)
            db.add(m.User(id=ident, email=f'{ident}@example.com',
                          full_name=f'{prefix} learner {index}',
                          password_hash=hash_password('IrrelevantPassword123!'),
                          is_active=index%2==0, role='student'))
            ids.append(ident)
    return prefix, ids


def test_student_pages_search_sort_filters_and_no_password_leak():
    prefix, ids=_students()
    with _staff() as c:
        first=c.get('/api/admin/students/page',params={'page':1,'page_size':3,'search':prefix,'sort':'name'})
        assert first.status_code==200,first.text
        doc=first.json()
        assert doc['total']==7 and doc['pages']==3 and len(doc['items'])==3
        assert [u['id'] for u in doc['items']]==ids[:3]
        assert all('password_hash' not in u for u in doc['items'])
        second=c.get('/api/admin/students/page',params={'page':2,'page_size':3,'search':prefix,'sort':'name'}).json()
        assert [u['id'] for u in second['items']]==ids[3:6]
        assert c.get('/api/admin/students/page',params={'page':4,'page_size':3,'search':prefix}).json()['items']==[]
        active=c.get('/api/admin/students/page',params={'search':prefix,'status':'active'}).json()
        assert active['total']==4 and all(u['is_active'] for u in active['items'])
        inactive=c.get('/api/admin/students/page',params={'search':prefix,'status':'inactive'}).json()
        assert inactive['total']==3 and all(not u['is_active'] for u in inactive['items'])
        assert c.get('/api/admin/students/page',params={'search':prefix+'%' }).json()['total']==0
        assert c.get('/api/admin/students/page',params={'search':'%'}).json()['total']==0
        assert c.get('/api/admin/students/page',params={'search':prefix+"' OR 1=1 --"}).json()['total']==0


def test_legacy_admin_students_bounded_and_offset_and_param_validation():
    with _staff() as c:
        assert len(c.get('/api/admin/students?limit=1').json())==1
        page_a=c.get('/api/admin/students?limit=2&offset=0').json()
        page_b=c.get('/api/admin/students?limit=2&offset=2').json()
        assert {u['id'] for u in page_a}.isdisjoint({u['id'] for u in page_b})
        for uri in ('/api/admin/students?limit=101', '/api/admin/students?limit=0',
                    '/api/admin/students?offset=-1', '/api/admin/students/page?page_size=51',
                    '/api/admin/students/page?page=0', '/api/admin/students/page?sort=unsafe',
                    '/api/admin/students/page?status=all-or-1=1',
                    '/api/admin/students/page?search='+'a'*121):
            assert c.get(uri).status_code==422,uri


def test_student_page_endpoint_is_admin_only():
    with TestClient(app) as c:
        assert c.get('/api/admin/students/page').status_code==401
        response=c.post('/api/auth/register',json={'email':'qa-'+uuid.uuid4().hex+'@example.com',
                    'full_name':'Limited Learner','password':'SafePassword123!'})
        assert response.status_code==201,response.text
        assert c.get('/api/admin/students/page').status_code==403


@pytest.mark.parametrize('claims',[
    {'sub':'test-admin','csrf':'abc','iss':'lingobridge'},
    {'csrf':'abc','iss':'lingobridge','exp':datetime.now(timezone.utc)+timedelta(hours=1)},
    {'sub':'test-admin','iss':'lingobridge','exp':datetime.now(timezone.utc)+timedelta(hours=1)},
    {'sub':123,'csrf':'abc','iss':'lingobridge','exp':datetime.now(timezone.utc)+timedelta(hours=1)},
    {'sub':'test-admin','csrf':123,'iss':'lingobridge','exp':datetime.now(timezone.utc)+timedelta(hours=1)},
])
def test_incomplete_or_malformed_signed_session_fails_closed(claims):
    make_admin()
    token=jwt.encode(claims,SECRET,algorithm='HS256')
    with TestClient(app) as c:
        c.cookies.set(COOKIE,token)
        response=c.get('/api/auth/me')
        assert response.status_code==401,response.text
