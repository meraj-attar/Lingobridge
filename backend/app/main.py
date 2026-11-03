"""LingoBridge REST API. Cookie JWT, CSRF, ownership checks, and server-only answer keys."""
import os, uuid, json, secrets, jwt, hashlib, threading, time
from datetime import date, datetime, timedelta, timezone
from typing import Any, Literal
from fastapi import FastAPI, Depends, HTTPException, Response, Request, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, ValidationError
from sqlalchemy import select, func, delete, update, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .db import get_db
from . import models as m
from .security import current_user, admin_user, hash_password, verify_password, create_session, COOKIE, SECRET
from .password_policy import validate_password

from .learning_metrics import get_streak, review_due, schedule_review
from .video_urls import VideoURLInput

app=FastAPI(title='LingoBridge API',version='2.0')
app.add_middleware(CORSMiddleware,allow_origins=[v.strip() for v in os.getenv('FRONTEND_ORIGIN','http://localhost:5175').split(',')],allow_credentials=True,allow_methods=['GET','POST','PUT','PATCH','DELETE'],allow_headers=['Content-Type','X-CSRF-Token'])

@app.middleware('http')
async def security_headers(request:Request,call_next):
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='strict-origin-when-cross-origin'
    response.headers['X-Frame-Options']='DENY'
    response.headers['Content-Security-Policy']="frame-ancestors 'none'"
    if request.url.path.startswith('/api/auth/'):
        response.headers['Cache-Control']='no-store'
    return response

_LOGIN_FAILURES={}
_LOGIN_LOCK=threading.Lock()
def login_limit(request,email,failed=False,success=False):
    # Local single-process throttling only; add Redis/shared counters at deployment.
    identity=hashlib.sha256((str(request.client.host if request.client else 'unknown')+'\0'+email).encode()).hexdigest()
    now=time.monotonic()
    with _LOGIN_LOCK:
        if len(_LOGIN_FAILURES)>10000:
            for key,(count,expires) in list(_LOGIN_FAILURES.items()):
                if expires<=now:_LOGIN_FAILURES.pop(key,None)
        count,expires=_LOGIN_FAILURES.get(identity,(0,now+900))
        if expires<=now:count,expires=0,now+900
        if success:
            _LOGIN_FAILURES.pop(identity,None)
            return
        if failed:
            _LOGIN_FAILURES[identity]=(count+1,expires)
        elif count>=8:
            raise HTTPException(429,'Too many login attempts; try again later')

def uid():return str(uuid.uuid4())
def iso(v):
    # SQLite returns naive timestamps even for timezone-aware columns. Stored
    # timestamps are UTC, so expose one consistent ISO-8601 representation.
    if isinstance(v, datetime) and v.tzinfo is None: v=v.replace(tzinfo=timezone.utc)
    return v.isoformat() if v else None
def missing(): raise HTTPException(404,'Record not found')
def need(condition,detail='Invalid request',status=400):
    if not condition: raise HTTPException(status,detail)
def row(obj, omit=()):
    return {k:iso(getattr(obj,k)) if isinstance(getattr(obj,k), (datetime,date)) else getattr(obj,k) for k in obj.__table__.columns.keys() if k not in omit}
def user_view(u):return row(u,('password_hash',))
def can_view_lesson(l,u):
    need(l and (l.is_published or (u and u.role=='admin')),'Lesson unavailable',404)

def course_for_lesson(db, lesson):
    module=db.get(m.Module,lesson.module_id)
    return db.get(m.Course,module.course_id) if module else None

def require_course_enrollment(db, user, lesson):
    if user.role=='admin': return
    course=course_for_lesson(db,lesson)
    need(course and course.is_published,'Course unavailable',404)
    need(db.scalar(select(m.CourseEnrollment).where(m.CourseEnrollment.user_id==user.id,m.CourseEnrollment.course_id==course.id)) is not None,
         'Enroll in this course before starting lessons',403)

def course_summary(db, course, user=None):
    result=row(course)
    modules=db.scalars(select(m.Module).where(m.Module.course_id==course.id).order_by(m.Module.sort_order,m.Module.id)).all()
    ids=[l.id for mod in modules for l in db.scalars(select(m.Lesson).where(m.Lesson.module_id==mod.id,m.Lesson.is_published==True)).all()]
    complete=set()
    if user and ids:
        complete=set(db.scalars(select(m.Progress.lesson_id).where(m.Progress.user_id==user.id,m.Progress.lesson_id.in_(ids),m.Progress.status=='completed')).all())
    result.update(lesson_count=len(ids),completed_lessons=len(complete),progress_percent=round(100*len(complete)/len(ids)) if ids else 0,
                  enrolled=bool(user and db.scalar(select(m.CourseEnrollment.id).where(m.CourseEnrollment.user_id==user.id,m.CourseEnrollment.course_id==course.id))))
    return result

def lang_view(l):return row(l)
def lesson_view(l, db):
    d=row(l);d['languages']=row(db.get(m.Language,l.language_id));d['course_levels']=row(db.get(m.Level,l.level_id));d['course_id']=course_for_lesson(db,l).id if course_for_lesson(db,l) else None;return d

def question_view(q, db, include_answers=False):
    opts=db.scalars(select(m.Option).where(m.Option.question_id==q.id).order_by(m.Option.id)).all()
    d=row(q,() if include_answers else ('answer_text','explanation'))
    if not include_answers:
        d['meta']={k:v for k,v in (q.meta or {}).items() if k not in ('solution','pairs')}
        if q.question_type=='matching':
            pairs=(q.meta or {}).get('pairs',[])
            right=[p[1] for p in pairs]
            secrets.SystemRandom().shuffle(right)
            d['meta']={'left':[p[0] for p in pairs], 'right':right}
        if q.question_type=='arrangement':
            original=list((q.meta or {}).get('tokens',[]))
            tokens=list(original)
            secrets.SystemRandom().shuffle(tokens)
            if len(tokens)>1 and tokens==original:tokens=tokens[1:]+tokens[:1]
            d['meta']={'tokens':tokens}
    if not include_answers: secrets.SystemRandom().shuffle(opts)
    d['options']=[row(o,() if include_answers else ('is_correct',)) for o in opts]
    return d

class Credentials(BaseModel):
    email:EmailStr
    password:str
class Registration(Credentials):
    full_name:str=Field(min_length=2,max_length=160)
    password:str=Field(min_length=8,max_length=128)
class ProfilePatch(BaseModel):
    full_name:str|None=Field(None,min_length=2,max_length=160)
    native_language_id:str|None=None
    target_language_id:str|None=None
    daily_goal:int|None=Field(None,ge=1,le=240)

@app.get('/api/health')
def health():return {'status':'ok'}

def set_login_cookie(response:Response, token):
    response.set_cookie(COOKIE,token,httponly=True,secure=os.getenv('COOKIE_SECURE', 'true' if os.getenv('ENVIRONMENT')=='production' else 'false').lower()=='true',samesite='lax',max_age=43200,path='/')

@app.post('/api/auth/register',status_code=201)
def register(data:Registration,response:Response,db:Session=Depends(get_db)):
    email=data.email.strip().lower()
    need(db.scalar(select(m.User).where(m.User.email==email)) is None,'Email already registered',409)
    validate_password(data.password)
    user=m.User(id=uid(),email=email,full_name=data.full_name.strip(),password_hash=hash_password(data.password),role='student')
    db.add(user)
    try:db.commit()
    except IntegrityError:
        db.rollback();raise HTTPException(409,'Email already registered')
    token,csrf=create_session(user);set_login_cookie(response,token)
    return {'user':user_view(user),'csrf':csrf}

@app.post('/api/auth/login')
def login(data:Credentials,response:Response,request:Request,db:Session=Depends(get_db)):
    email=data.email.lower().strip()
    login_limit(request,email)
    user=db.scalar(select(m.User).where(m.User.email==data.email.lower().strip()))
    if not user or not verify_password(data.password,user.password_hash) or not user.is_active:
        login_limit(request,email,failed=True)
        raise HTTPException(401,'Invalid credentials or inactive account')
    login_limit(request,email,success=True)
    token,csrf=create_session(user);set_login_cookie(response,token)
    return {'user':user_view(user),'csrf':csrf}

@app.get('/api/auth/me')
def me(request:Request,u:m.User=Depends(current_user)):
    return {'user':user_view(u),'csrf':request.state.csrf}

@app.post('/api/auth/logout')
def logout(response:Response,u:m.User=Depends(current_user)):
    response.delete_cookie(COOKIE,path='/');return {'ok':True}

@app.patch('/api/profile')
def profile(p:ProfilePatch,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    for field,value in p.model_dump(exclude_unset=True).items():
        if field.endswith('_language_id') and value is not None:need(db.get(m.Language,value) is not None,'Unknown language')
        setattr(u,field,value)
    db.commit();return user_view(u)

@app.get('/api/languages')
def languages(db:Session=Depends(get_db)):
    return [row(l) for l in db.scalars(select(m.Language).order_by(m.Language.name)).all()]

@app.get('/api/languages/{code}')
def language(code:str,db:Session=Depends(get_db)):
    l=db.scalar(select(m.Language).where((m.Language.code==code)|(m.Language.id==code)))
    return row(l) if l else missing()

@app.get('/api/levels')
def levels(db:Session=Depends(get_db)):
    return [row(l) for l in db.scalars(select(m.Level).order_by(m.Level.sort_order)).all()]

@app.get('/api/courses')
def courses(request:Request,language_id:str|None=None,level_id:str|None=None,db:Session=Depends(get_db)):
    q=select(m.Course).join(m.Language,m.Language.id==m.Course.language_id).where(m.Course.is_published==True,m.Language.is_active==True)
    if language_id:q=q.where(m.Course.language_id==language_id)
    if level_id:q=q.where(m.Course.level_id==level_id)
    user=optional_user(request,db)
    return [course_summary(db,x,user) for x in db.scalars(q.order_by(m.Course.language_id,m.Course.level_id,m.Course.title)).all()]

@app.get('/api/courses/enrolled/me')
def enrolled_courses(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    items=db.scalars(select(m.Course).join(m.CourseEnrollment,m.CourseEnrollment.course_id==m.Course.id).where(m.CourseEnrollment.user_id==u.id)).all()
    return [course_summary(db,c,u) for c in items]

@app.post('/api/courses/{cid}/enroll')
def enroll_course(cid:str,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    course=db.get(m.Course,cid)
    need(course and course.is_published and db.get(m.Language,course.language_id).is_active,'Course unavailable',404)
    enrolled=db.scalar(select(m.CourseEnrollment).where(m.CourseEnrollment.course_id==cid,m.CourseEnrollment.user_id==u.id))
    if enrolled is None:
        enrolled=m.CourseEnrollment(id=uid(),user_id=u.id,course_id=cid)
        db.add(enrolled)
        # Keep language selection separate, but sync it for the existing dashboard cards.
        if db.scalar(select(m.Enrollment).where(m.Enrollment.user_id==u.id,m.Enrollment.language_id==course.language_id)) is None:
            db.add(m.Enrollment(id=uid(),user_id=u.id,language_id=course.language_id))
        try:db.commit()
        except IntegrityError:db.rollback();raise HTTPException(409,'Enrollment conflict, refresh and try again')
    return course_summary(db,course,u)

@app.get('/api/courses/{cid}/modules')
def modules(cid:str,db:Session=Depends(get_db)):
    course=db.get(m.Course,cid)
    need(course and course.is_published,'Course unavailable',404)
    results=[]
    for mod in db.scalars(select(m.Module).where(m.Module.course_id==cid).order_by(m.Module.sort_order,m.Module.id)).all():
        d=row(mod)
        d['lessons']=[row(l) for l in db.scalars(select(m.Lesson).where(m.Lesson.module_id==mod.id,m.Lesson.is_published==True).order_by(m.Lesson.lesson_order,m.Lesson.id)).all()]
        results.append(d)
    return results

def optional_user(request,db):
    token=request.cookies.get(COOKIE)
    if not token:return None
    try:
        payload=jwt.decode(token,SECRET,algorithms=['HS256'],issuer='lingobridge')
        user=db.get(m.User,payload['sub'])
        return user if user and user.is_active else None
    except (jwt.PyJWTError,KeyError):return None

@app.get('/api/lessons')
def lessons(language_id:str|None=None,level_id:str|None=None,is_published:bool|None=None,db:Session=Depends(get_db)):
    q=select(m.Lesson).join(m.Module,m.Module.id==m.Lesson.module_id).join(m.Course,m.Course.id==m.Module.course_id).join(m.Language,m.Language.id==m.Course.language_id)
    q=q.where(m.Course.is_published==True,m.Language.is_active==True)
    if language_id:q=q.where(m.Lesson.language_id==language_id)
    if level_id:q=q.where(m.Lesson.level_id==level_id)
    # public catalogue never exposes unpublished lessons
    q=q.where(m.Lesson.is_published==True)
    return [lesson_view(x,db) for x in db.scalars(q.order_by(m.Lesson.language_id,m.Lesson.level_id,m.Lesson.lesson_order)).all()]

@app.get('/api/lessons/{lid}')
def lesson(lid:str,request:Request,db:Session=Depends(get_db),u:m.User=Depends(current_user)):
    l=db.get(m.Lesson,lid);can_view_lesson(l,u)
    require_course_enrollment(db,u,l)
    result=lesson_view(l,db)
    result['vocabulary_items']=[row(x) for x in db.scalars(select(m.Vocabulary).where(m.Vocabulary.lesson_id==lid)).all()]
    result['quiz_questions']=[question_view(q,db,u.role=='admin' and request.query_params.get('include_answers')=='true') for q in db.scalars(select(m.Question).where(m.Question.lesson_id==lid).order_by(m.Question.id)).all()]
    return result

@app.get('/api/enrollments')
def enrollments(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    result=[]
    for e in db.scalars(select(m.Enrollment).where(m.Enrollment.user_id==u.id)).all():
        d=row(e);d['languages']=row(db.get(m.Language,e.language_id));result.append(d)
    return result

@app.post('/api/enrollments')
def enroll(data:dict=Body(...),u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    lid=data.get('language_id');l=db.get(m.Language,lid) if isinstance(lid,str) else None
    need(l and l.is_active,'Invalid language')
    obj=db.scalar(select(m.Enrollment).where(m.Enrollment.user_id==u.id,m.Enrollment.language_id==lid))
    if not obj: obj=m.Enrollment(id=uid(),user_id=u.id,language_id=lid);db.add(obj)
    db.commit();d=row(obj);d['languages']=row(l);return d

@app.get('/api/progress')
def progress(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    lp=[row(p) for p in db.scalars(select(m.Progress).where(m.Progress.user_id==u.id)).all()]
    qa=[row(q,('answers',)) for q in db.scalars(select(m.QuizAttempt).where(m.QuizAttempt.user_id==u.id).order_by(m.QuizAttempt.attempted_at.desc())).all()]
    return {'lesson_progress':lp,'quiz_attempts':qa,'xp':u.xp,'streak':get_streak(db,u.id),'daily_goal':u.daily_goal}

@app.get('/api/activity')
def activity(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    days=[row(d) for d in db.scalars(select(m.DailyActivity).where(m.DailyActivity.user_id==u.id).order_by(m.DailyActivity.day.desc())).all()]
    badges=[{'code':a.achievement_code,'earned_at':iso(a.earned_at)} for a in db.scalars(select(m.UserAchievement).where(m.UserAchievement.user_id==u.id)).all()]
    goal_today=next((a['minutes'] for a in days if a['day']==date.today().isoformat()),0)
    return {'daily_activity':days,'achievements':badges,'xp':u.xp,'level':1+u.xp//100,'streak':get_streak(db,u.id),'daily_goal':u.daily_goal,
            'today_minutes':goal_today,'daily_goal_met':goal_today>=u.daily_goal,'daily_goal_percent':min(100,round(goal_today*100/u.daily_goal))}

@app.post('/api/activity')
def log_activity(data:dict=Body(...),u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    minutes=data.get('minutes',0)
    need(type(minutes)==int and 1<=minutes<=120,'Activity minutes must be 1–120')
    today=date.today().isoformat()
    a=db.scalar(select(m.DailyActivity).where(m.DailyActivity.user_id==u.id,m.DailyActivity.day==today))
    if a is None:a=m.DailyActivity(id=uid(),user_id=u.id,day=today,minutes=0,xp=0);db.add(a)
    a.minutes+=minutes
    db.commit();return {**row(a), 'streak':get_streak(db,u.id)}

@app.post('/api/lessons/{lid}/start')
def start_lesson(lid:str,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    l=db.get(m.Lesson,lid);can_view_lesson(l,u)
    require_course_enrollment(db,u,l)
    p=db.scalar(select(m.Progress).where(m.Progress.user_id==u.id,m.Progress.lesson_id==lid))
    if p is None:db.add(m.Progress(id=uid(),user_id=u.id,lesson_id=lid,status='in_progress'))
    course=course_for_lesson(db,l)
    enr=db.scalar(select(m.CourseEnrollment).where(m.CourseEnrollment.user_id==u.id,m.CourseEnrollment.course_id==course.id))
    if enr:enr.last_accessed_at=datetime.now(timezone.utc)
    db.commit();return {'status':'started'}

@app.get('/api/bookmarks')
def bookmarks(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    return [row(b) for b in db.scalars(select(m.Bookmark).where(m.Bookmark.user_id==u.id)).all()]

@app.post('/api/bookmarks/{lid}')
def bookmark(lid:str,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    l=db.get(m.Lesson,lid);can_view_lesson(l,u)
    b=db.scalar(select(m.Bookmark).where(m.Bookmark.user_id==u.id,m.Bookmark.lesson_id==lid))
    if not b:db.add(m.Bookmark(id=uid(),user_id=u.id,lesson_id=lid));db.commit()
    return {'saved':True}

@app.delete('/api/bookmarks/{lid}')
def unbookmark(lid:str,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    db.execute(delete(m.Bookmark).where(m.Bookmark.user_id==u.id,m.Bookmark.lesson_id==lid));db.commit();return {'saved':False}

@app.get('/api/flashcards')
def flashcards(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    states=db.scalars(select(m.FlashcardState).where(m.FlashcardState.user_id==u.id)).all()
    return [{**row(s),'due':review_due(s)} for s in states]

class FlashcardPatch(BaseModel):
    state: str

@app.put('/api/flashcards/{vid}')
def set_flashcard(vid:str,data:FlashcardPatch,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    need(data.state in ('known','revise'),'Flashcard state must be known or revise')
    word=db.get(m.Vocabulary,vid)
    if not word:missing()
    lesson=db.get(m.Lesson,word.lesson_id)
    can_view_lesson(lesson,u)
    require_course_enrollment(db,u,lesson)
    state=db.get(m.FlashcardState,(u.id,vid))
    if state is None:
        state=m.FlashcardState(user_id=u.id,vocabulary_id=vid,state=data.state)
        db.add(state)
    schedule_review(state,data.state)
    db.commit();return {**row(state),'due':review_due(state)}

@app.get('/api/recommendations')
def recommendations(u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    """Deterministic, explainable guidance based only on this user's saved work."""
    enrolled=db.scalars(select(m.CourseEnrollment.course_id).where(m.CourseEnrollment.user_id==u.id)).all()
    if not enrolled:return {'lessons':[],'review_due':0,'review_total':0}
    lessons=db.scalars(select(m.Lesson).join(m.Module,m.Module.id==m.Lesson.module_id)
        .join(m.Course,m.Course.id==m.Module.course_id)
        .where(m.Module.course_id.in_(enrolled),m.Course.is_published==True,m.Lesson.is_published==True)
        .order_by(m.Course.level_id,m.Module.sort_order,m.Lesson.lesson_order,m.Lesson.id)).all()
    pmap={p.lesson_id:p for p in db.scalars(select(m.Progress).where(m.Progress.user_id==u.id)).all()}
    attempts=db.scalars(select(m.QuizAttempt).where(m.QuizAttempt.user_id==u.id).order_by(m.QuizAttempt.attempted_at.desc())).all()
    last={}
    for a in attempts:last.setdefault(a.lesson_id,a)
    suggestions=[]
    for index,lesson in enumerate(lessons):
        p=pmap.get(lesson.id)
        if p and p.status=='completed':continue
        a=last.get(lesson.id)
        if p and p.status=='in_progress': rank,why=0,'Continue an unfinished lesson'
        elif a and not a.passed: rank,why=1,'Review after a quiz below the pass threshold'
        else: rank,why=2,'Next lesson in your enrolled course'
        suggestions.append((rank,index,{'lesson_id':lesson.id,'title':lesson.title,'language_id':lesson.language_id,'course_id':course_for_lesson(db,lesson).id,'reason':why}))
    suggestions.sort(key=lambda item:(item[0],item[1]))
    ids=[l.id for l in lessons]
    vocab_ids=set(db.scalars(select(m.Vocabulary.id).where(m.Vocabulary.lesson_id.in_(ids))).all()) if ids else set()
    states=db.scalars(select(m.FlashcardState).where(m.FlashcardState.user_id==u.id,m.FlashcardState.vocabulary_id.in_(vocab_ids))).all() if vocab_ids else []
    state_map={s.vocabulary_id:s for s in states}
    return {'lessons':[x[2] for x in suggestions[:3]],
            'review_due':sum(review_due(state_map.get(vid)) for vid in vocab_ids),
            'review_total':len(vocab_ids)}

@app.post('/api/lessons/{lid}/quiz-session')
def start_quiz(lid:str,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    lesson=db.get(m.Lesson,lid);can_view_lesson(lesson,u)
    require_course_enrollment(db,u,lesson)
    questions=db.scalars(select(m.Question).where(m.Question.lesson_id==lid)).all()
    need(bool(questions),'Lesson quiz has no questions')
    secs=sum(max(0,q.time_limit_seconds or 0) for q in questions)
    need(secs<=7200,'Quiz timer may not exceed two hours')
    # Issue one-time tickets even for untimed tests, closing replay/XP farming.
    expiry=datetime.now(timezone.utc)+timedelta(seconds=secs if secs else 3600)
    ticket=m.QuizSession(id=uid(),user_id=u.id,lesson_id=lid,expires_at=expiry)
    db.add(ticket);db.commit()
    claims={'sub':u.id,'lesson':lid,'type':'quiz','jti':ticket.id,'exp':expiry,'iss':'lingobridge'}
    return {'attempt_token':jwt.encode(claims,SECRET,algorithm='HS256'),'limit_seconds':secs}

class Answer(BaseModel):
    question_id:str
    option_id:str|None=None
    text:str|None=None
class Submission(BaseModel):
    answers:list[Answer]=Field(min_length=1,max_length=100)
    attempt_token:str|None=None

def check_answer(q,a:Answer,opts):
    if q.question_type=='mcq':
        need(a.option_id in [o.id for o in opts], 'Invalid quiz option')
        correct=next((o.id for o in opts if o.is_correct),None)
        return a.option_id==correct,correct
    need(a.text is not None,'Exercise answer missing')
    answer=(q.answer_text or '').strip()
    if q.question_type=='matching':
        pairs=(q.meta or {}).get('pairs',[])
        answer='|'.join(f'{x}:{y}' for x,y in pairs)
    return ' '.join(a.text.strip().split()).casefold()==' '.join(answer.split()).casefold(),answer

@app.post('/api/lessons/{lid}/submit')
def submit_quiz(lid:str,data:Submission,u:m.User=Depends(current_user),db:Session=Depends(get_db)):
    l=db.get(m.Lesson,lid);can_view_lesson(l,u)
    require_course_enrollment(db,u,l)
    questions=db.scalars(select(m.Question).where(m.Question.lesson_id==lid)).all()
    need(len(questions)>0,'No quiz exists')
    need(bool(data.attempt_token),'Quiz session required',403)
    try:
        claims=jwt.decode(data.attempt_token,SECRET,algorithms=['HS256'],issuer='lingobridge')
    except jwt.ExpiredSignatureError:raise HTTPException(403,'Quiz time has expired')
    except jwt.PyJWTError:raise HTTPException(403,'Invalid quiz session')
    need(claims.get('sub')==u.id and claims.get('lesson')==lid and claims.get('type')=='quiz','Invalid quiz session',403)
    ticket=db.get(m.QuizSession,claims.get('jti'))
    need(ticket and ticket.user_id==u.id and ticket.lesson_id==lid and ticket.consumed_at is None,'Quiz session already used or unavailable',403)
    # UTC timestamps: SQLite returns naive values, PostgreSQL returns timezone-aware values.
    expires=ticket.expires_at.replace(tzinfo=timezone.utc) if ticket.expires_at.tzinfo is None else ticket.expires_at
    need(expires>datetime.now(timezone.utc),'Quiz time has expired',403)
    ans={a.question_id:a for a in data.answers}
    need(len(ans)==len(data.answers)==len(questions) and set(ans)=={q.id for q in questions},'Submit exactly one answer per question')
    breakdown=[];score=0
    for q in questions:
        opts=db.scalars(select(m.Option).where(m.Option.question_id==q.id)).all()
        ok,correct=check_answer(q,ans[q.id],opts)
        score+=bool(ok)
        breakdown.append({'question_id':q.id,'question_text':q.question_text,'selected_option_id':ans[q.id].option_id,'correct_option_id':correct if q.question_type=='mcq' else None,'correct_text':correct if q.question_type!='mcq' else None,'is_correct':bool(ok),'explanation':q.explanation})
    pct=round(score*100/len(questions));passed=pct>=70
    prev=db.scalar(select(m.Progress).where(m.Progress.user_id==u.id,m.Progress.lesson_id==lid))
    first_pass=passed and (prev is None or prev.status!='completed')
    consumed=db.execute(update(m.QuizSession).where(m.QuizSession.id==ticket.id,m.QuizSession.consumed_at.is_(None)).values(consumed_at=datetime.now(timezone.utc)))
    need(consumed.rowcount==1,'Quiz ticket already consumed',403)
    attempt=m.QuizAttempt(id=uid(),user_id=u.id,lesson_id=lid,score=score,total_questions=len(questions),percentage=pct,passed=passed,answers=[a.model_dump() for a in data.answers])
    db.add(attempt)
    if prev is None:prev=m.Progress(id=uid(),user_id=u.id,lesson_id=lid);db.add(prev)
    if passed:prev.status='completed';prev.completed_at=datetime.now(timezone.utc)
    prev.updated_at=datetime.now(timezone.utc)
    today=date.today().isoformat()
    activity=db.scalar(select(m.DailyActivity).where(m.DailyActivity.user_id==u.id,m.DailyActivity.day==today))
    if activity is None:activity=m.DailyActivity(id=uid(),user_id=u.id,day=today,minutes=0,xp=0);db.add(activity)
    earned=10 if first_pass else 0
    activity.xp+=earned
    if first_pass:activity.minutes+=min(120,max(1,l.duration_minutes))
    u.xp+=earned
    db.flush()
    count=db.scalar(select(func.count(m.Progress.id)).where(m.Progress.user_id==u.id,m.Progress.status=='completed'))
    for a in db.scalars(select(m.Achievement).where(m.Achievement.threshold<=count)).all():
        if db.get(m.UserAchievement,(u.id,a.code)) is None:db.add(m.UserAchievement(user_id=u.id,achievement_code=a.code))
    db.commit()
    return {'attempt_id':attempt.id,'score':score,'total_questions':len(questions),'percentage':pct,'passed':passed,'breakdown':breakdown,'xp_earned':earned,'daily_minutes_credited':activity.minutes}

# Restricted admin data and editor operations.
TABLES={'languages':m.Language,'levels':m.Level,'courses':m.Course,'modules':m.Module,'lessons':m.Lesson,'vocabulary':m.Vocabulary,'questions':m.Question,'options':m.Option,'achievements':m.Achievement}
EDITABLE={
 'languages':{'code','name','native_name','description','flag','icon','color','is_active'},
 'levels':{'code','name','description','sort_order'},
 'courses':{'language_id','level_id','title','description','is_published'},
 'modules':{'course_id','title','sort_order'},
 'lessons':{'module_id','language_id','level_id','title','description','duration_minutes','lesson_order','is_published','video_url','objectives','content','grammar_notes'},
 'vocabulary':{'lesson_id','word','translation','pronunciation','example_sentence','example_translation'},
 'questions':{'lesson_id','question_text','explanation','question_type','time_limit_seconds','answer_text','meta'},
 'options':{'question_id','option_text','is_correct'},
 'achievements':{'code','title','description','threshold'}
}

def validate_question_fields(data):
    kind=data.get('question_type','mcq')
    need(kind in ('mcq','fill_blank','matching','arrangement'),'Invalid exercise type')
    timer=data.get('time_limit_seconds')
    need(timer is None or (type(timer)==int and 10<=timer<=3600),'Timer must be 10–3600 seconds')
    if kind!='mcq':
        need(bool(str(data.get('answer_text') or '').strip()) or kind=='matching','Exercise answer is required')
        if kind=='matching':
            pairs=(data.get('meta') or {}).get('pairs',[])
            need(isinstance(pairs,list) and len(pairs)>=2 and all(isinstance(p,list) and len(p)==2 and all(isinstance(x,str) and x for x in p) for p in pairs),'Matching requires two or more string pairs')
        if kind=='arrangement':
            tokens=(data.get('meta') or {}).get('tokens',[])
            need(isinstance(tokens,list) and len(tokens)>=2 and all(isinstance(x,str) for x in tokens),'Arrangement requires ordered tokens')

def check_lesson_video(data):
    if 'video_url' in data:
        try:
            VideoURLInput.model_validate({'video_url': data['video_url']})
        except ValidationError as exc:
            raise HTTPException(422, exc.errors()[0]['msg'].removeprefix('Value error, ')) from exc


def lock_mcq(db, question_id):
    # PostgreSQL row locking serializes competing option changes. SQLite's
    # development/test backend does not provide equivalent row locks.
    question=db.scalar(select(m.Question).where(m.Question.id==question_id).with_for_update())
    need(question is not None,'Unknown question',404)
    need(question.question_type=='mcq','Only MCQs can have options')
    return question


def mcq_options(db, question_id):
    return db.scalars(select(m.Option).where(m.Option.question_id==question_id)).all()


def validate_lesson_parent(db,data):
    mod=db.get(m.Module,data.get('module_id'))
    need(mod is not None,'Unknown lesson module')
    course=db.get(m.Course,mod.course_id)
    need(course is not None and course.language_id==data.get('language_id') and course.level_id==data.get('level_id'),
         'Lesson language/level must match its parent course')

def allowed_fields(table,data):
    need(isinstance(data,dict) and bool(data),'Object payload required')
    need(not(set(data)-EDITABLE[table]),'Unknown or protected fields: '+','.join(set(data)-EDITABLE[table]))
    return data

@app.get('/api/admin/manage/{table}')
def admin_list(table:str,db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(table in TABLES,'Unknown table',404)
    return [row(obj) for obj in db.scalars(select(TABLES[table])).all()]

@app.post('/api/admin/manage/{table}',status_code=201)
def admin_create(table:str,data:dict=Body(...),db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(table in TABLES,'Unknown table',404);data=allowed_fields(table,data)
    if table=='options':
        need(type(data.get('is_correct')) is bool,'Explicit answer flag required')
        need(isinstance(data.get('option_text'),str) and bool(data['option_text'].strip()),'Option text is required',422)
        question=lock_mcq(db,data.get('question_id'))
        existing=mcq_options(db,question.id)
        need(not quiz_item_was_attempted(db,question.lesson_id,question_id=question.id),
             'Cannot modify an MCQ used in learner attempts; create a new question instead',409)
        need(len(existing)<8,'An MCQ cannot have more than eight options',409)
        if data['is_correct']:
            need(not any(o.is_correct for o in existing),'MCQ already has a correct answer',409)
    if table=='questions':
        need(data.get('question_type','mcq')!='mcq','Create an MCQ with its options through /api/admin/lessons/{id}/questions')
        validate_question_fields(data)
    if table=='lessons' and not data.get('module_id'):
        need(bool(data.get('language_id') and data.get('level_id')),'Select language and proficiency')
        lv=db.get(m.Level,data['level_id']);lg=db.get(m.Language,data['language_id'])
        need(lv is not None and lg is not None,'Invalid course language/level')
        course=db.scalar(select(m.Course).where(m.Course.language_id==lg.id,m.Course.level_id==lv.id).order_by(m.Course.id))
        need(course is not None,'Create a course for this language and level first')
        module=db.scalar(select(m.Module).where(m.Module.course_id==course.id).order_by(m.Module.sort_order))
        need(module is not None,'Create a module for this course first')
        data['module_id']=module.id
    if table=='lessons':
        check_lesson_video(data)
        validate_lesson_parent(db,data)
    cls=TABLES[table];key='code' if table=='achievements' else 'id';ident=(data.get('code') if table=='achievements' else uid())
    if table=='achievements':need(bool(ident),'Achievement code required')
    obj=cls(**{key:ident,**data});db.add(obj)
    try:db.commit()
    except IntegrityError as e:db.rollback();raise HTTPException(409,'Unique constraint or foreign key violation')
    return row(obj)

@app.patch('/api/admin/manage/{table}/{ident}')
def admin_update(table:str,ident:str,data:dict=Body(...),db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(table in TABLES,'Unknown table',404);data=allowed_fields(table,data)
    obj=db.get(TABLES[table],ident)
    if not obj:missing()
    if table=='lessons' and not data.get('module_id') and ('level_id' in data or 'language_id' in data):
        lv=db.get(m.Level,data.get('level_id',obj.level_id));lg=db.get(m.Language,data.get('language_id',obj.language_id))
        need(lv is not None and lg is not None,'Invalid course language/level')
        course=db.scalar(select(m.Course).where(m.Course.language_id==lg.id,m.Course.level_id==lv.id).order_by(m.Course.id))
        need(course is not None,'Create a course for this language and level first')
        module=db.scalar(select(m.Module).where(m.Module.course_id==course.id).order_by(m.Module.sort_order))
        need(module is not None,'Create a module for this course first')
        data['module_id']=module.id
    if table=='courses' and any(k in data and data[k]!=getattr(obj,k) for k in ('language_id','level_id')):
        dependent=db.scalar(select(func.count(m.Lesson.id)).join(m.Module,m.Module.id==m.Lesson.module_id).where(m.Module.course_id==ident))
        need(dependent==0,'Cannot change course language/level while lessons exist',409)
    if table=='modules' and 'course_id' in data and data['course_id']!=obj.course_id:
        dependent=db.scalar(select(func.count(m.Lesson.id)).where(m.Lesson.module_id==ident))
        need(dependent==0,'Cannot move a module containing lessons to another course',409)
    if table=='lessons':
        check_lesson_video(data)
        validate_lesson_parent(db,{**row(obj),**data})
    if table in ('questions','options'):
        q=obj if table=='questions' else db.get(m.Question,obj.question_id)
        need(not quiz_item_was_attempted(db,q.lesson_id,question_id=q.id), 'Cannot change quiz content used in learner attempts; publish a new lesson instead',409)
    if table=='options':
        lock_mcq(db,obj.question_id)
        need('question_id' not in data,'Options cannot be moved between questions; edit the parent MCQ')
        if 'option_text' in data:
            need(isinstance(data['option_text'],str) and bool(data['option_text'].strip()),'Option text is required',422)
        if 'is_correct' in data:
            need(type(data['is_correct']) is bool,'Explicit answer flag required',422)
        if data.get('is_correct') is True and not obj.is_correct:
            need(db.scalar(select(m.Option.id).where(m.Option.question_id==obj.question_id,
                 m.Option.is_correct==True,m.Option.id!=ident).limit(1)) is None,
                 'MCQ already has a correct answer',409)
        if data.get('is_correct') is False and obj.is_correct:
            need(False,'A single-answer MCQ must retain one correct option; edit the complete MCQ',409)
    if table=='questions':
        need('question_type' not in data or data['question_type']==obj.question_type,
             'Use the complete question editor to change exercise type')
        validate_question_fields({**row(obj),**data})
    for k,v in data.items():setattr(obj,k,v)
    try:db.commit()
    except IntegrityError:db.rollback();raise HTTPException(409,'Constraint violation')
    return row(obj)

def quiz_item_was_attempted(db, lesson_id, *, question_id=None, option_id=None):
    # Historical attempts store question/option IDs in their immutable answer JSON.
    # An admin may remove newly authored draft items that were never presented.
    attempts=db.scalars(select(m.QuizAttempt).where(m.QuizAttempt.lesson_id==lesson_id)).all()
    # Empty legacy answer snapshots are ambiguous: fail closed rather than
    # risk deleting a question whose historic options cannot be reconstructed.
    if any(not attempt.answers for attempt in attempts):return True
    return any(isinstance(a,dict) and (
        a.get('question_id')==question_id if question_id else a.get('option_id')==option_id)
        for attempt in attempts for a in (attempt.answers or []))

def content_has_learning_history(db, table, ident):
    """Guard cascading deletes, preserving user progress, card ratings and quiz attempts."""
    if table=='courses':
        if db.scalar(select(m.CourseEnrollment.id).where(m.CourseEnrollment.course_id==ident).limit(1)) is not None:return True
        lesson_ids=select(m.Lesson.id).join(m.Module,m.Lesson.module_id==m.Module.id).where(m.Module.course_id==ident)
    elif table=='modules':
        lesson_ids=select(m.Lesson.id).where(m.Lesson.module_id==ident)
    elif table=='lessons':
        lesson_ids=select(m.Lesson.id).where(m.Lesson.id==ident)
    elif table in ('questions','options'):
        question=db.get(m.Question,ident) if table=='questions' else db.get(m.Question,db.get(m.Option,ident).question_id)
        return quiz_item_was_attempted(db,question.lesson_id,question_id=question.id)
    elif table=='vocabulary':
        word=db.get(m.Vocabulary,ident)
        return db.scalar(select(m.FlashcardState.user_id).where(m.FlashcardState.vocabulary_id==ident).limit(1)) is not None
    else:return False
    # Flashcard review history belongs to a vocabulary row, not directly to a lesson.
    # Without this check, deleting a lesson could silently cascade-delete it.
    if db.scalar(select(m.FlashcardState.user_id).join(m.Vocabulary, m.Vocabulary.id==m.FlashcardState.vocabulary_id)
                 .where(m.Vocabulary.lesson_id.in_(lesson_ids)).limit(1)) is not None:
        return True
    return any(db.scalar(select(cls.id).where(cls.lesson_id.in_(lesson_ids)).limit(1)) is not None
               for cls in (m.Progress,m.QuizAttempt,m.Bookmark)) or (
        db.scalar(select(m.QuizSession.id).where(m.QuizSession.lesson_id.in_(lesson_ids)).limit(1)) is not None)

@app.delete('/api/admin/manage/{table}/{ident}')
def admin_delete(table:str,ident:str,db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(table in TABLES,'Unknown table',404)
    obj=db.get(TABLES[table],ident)
    if not obj:missing()
    if table=='languages':
        # Never cascade a language's students or descendant courses. Archive instead.
        has_children = any(db.scalar(select(cls.id).where(cls.language_id==ident).limit(1)) is not None
                           for cls in (m.Course,m.Lesson,m.Enrollment))
        if has_children:
            obj.is_active=False
            db.commit()
            return {'ok':True,'archived':True,'message':'Language deactivated; enrollment history preserved'}
    need(not content_has_learning_history(db,table,ident),'Cannot delete content with existing learner history; unpublish instead',409)
    if table=='options':
        lock_mcq(db,obj.question_id)
        existing=mcq_options(db,obj.question_id)
        need(len(existing)>2,'An MCQ must retain at least two options; edit the complete question instead',409)
        need(sum(o.is_correct is True for o in existing)==1,'MCQ requires exactly one correct answer; repair the question before deleting options',409)
        need(not obj.is_correct,'Cannot delete the correct MCQ answer; edit the entire question',409)
    if table=='lessons':
        # A card without a review is safe to remove; a reviewed card was caught above.
        pass
    db.delete(obj)
    try:db.commit()
    except IntegrityError:db.rollback();raise HTTPException(409,'This record is referenced by other records; remove dependents first')
    return {'ok':True}

@app.post('/api/admin/lessons/{lid}/vocabulary',status_code=201)
def add_vocab(lid:str,data:dict=Body(...),db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(db.get(m.Lesson,lid) is not None,'Lesson missing',404)
    data=allowed_fields('vocabulary',{**data,'lesson_id':lid})
    need(bool(str(data.get('word','')).strip()),'Word required')
    v=m.Vocabulary(id=uid(),**data);db.add(v);db.commit();return row(v)

def _question_payload(data, *, updating=False):
    data=dict(data)
    opts=data.pop('options',None)
    kind=data.get('question_type','mcq')
    need(kind in ('mcq','fill_blank','matching','arrangement'),'Unsupported exercise type')
    need(bool(str(data.get('question_text','')).strip()),'Question text required')
    fields=allowed_fields('questions',data)
    validate_question_fields(fields)
    if kind=='mcq':
        need(isinstance(opts,list) and 2<=len(opts)<=8,'MCQ requires 2–8 options')
        need(sum(o.get('is_correct') is True for o in opts)==1,'MCQ requires exactly one correct option')
        for o in opts:
            need(isinstance(o,dict) and set(o)<={'option_text','is_correct'},'Invalid option')
            need(bool(str(o.get('option_text','')).strip()) and type(o.get('is_correct')) is bool,'Invalid option text/flag')
    else:
        need(opts is None or opts==[],'Text-based exercise does not use MCQ options')
    return fields,opts or []

@app.post('/api/admin/lessons/{lid}/questions',status_code=201)
def add_question(lid:str,data:dict=Body(...),db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(db.get(m.Lesson,lid) is not None,'Lesson missing',404)
    fields,opts=_question_payload({**data,'lesson_id':lid})
    q=m.Question(id=uid(),**fields);db.add(q);db.flush()
    for opt in opts:db.add(m.Option(id=uid(),question_id=q.id,**opt))
    try:db.commit()
    except IntegrityError:db.rollback();raise HTTPException(409,'Invalid question relationship')
    return question_view(q,db,True)

@app.put('/api/admin/questions/{qid}')
def edit_question(qid:str,data:dict=Body(...),db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    q=db.scalar(select(m.Question).where(m.Question.id==qid).with_for_update())
    if not q:missing()
    need(not quiz_item_was_attempted(db,q.lesson_id,question_id=q.id), 'Cannot change quiz content used in learner attempts',409)
    payload={**row(q),**data}
    payload.pop('id',None)
    keep_existing='options' not in data and payload.get('question_type',q.question_type)==q.question_type
    if keep_existing and q.question_type=='mcq':
        payload['options']=[{'option_text':o.option_text,'is_correct':o.is_correct} for o in db.scalars(select(m.Option).where(m.Option.question_id==qid)).all()]
    fields,opts=_question_payload(payload,updating=True)
    for k,v in fields.items():setattr(q,k,v)
    if not keep_existing:
        db.execute(delete(m.Option).where(m.Option.question_id==qid))
        db.flush()
        for opt in opts:db.add(m.Option(id=uid(),question_id=q.id,**opt))
    try:db.commit()
    except IntegrityError:db.rollback();raise HTTPException(409,'Question relationship constraint')
    return question_view(q,db,True)

@app.get('/api/admin/stats')
def admin_stats(db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    count=lambda t:db.scalar(select(func.count()).select_from(t))
    attempts=count(m.QuizAttempt);passed=db.scalar(select(func.count()).select_from(m.QuizAttempt).where(m.QuizAttempt.passed==True))
    return {'total_courses':db.scalar(select(func.count()).select_from(m.Course)), 'total_vocabulary':count(m.Vocabulary), 'total_students':db.scalar(select(func.count()).select_from(m.User).where(m.User.role=='student')),'total_languages':db.scalar(select(func.count()).select_from(m.Language).where(m.Language.is_active==True)),'total_lessons':db.scalar(select(func.count()).select_from(m.Lesson).where(m.Lesson.is_published==True)),'total_quizzes':db.scalar(select(func.count(func.distinct(m.Question.lesson_id)))),'total_attempts':attempts,'pass_rate':round(100*passed/attempts) if attempts else 0}

def student_admin_detail(db:Session, student:m.User):
    """Build the original admin response shape for one bounded page of accounts."""
    d=user_view(student)
    d['student_languages']=[{'languages':row(db.get(m.Language,x.language_id))} for x in db.scalars(select(m.Enrollment).where(m.Enrollment.user_id==student.id))]
    d['course_enrollments']=[course_summary(db,db.get(m.Course,x.course_id),student) for x in db.scalars(select(m.CourseEnrollment).where(m.CourseEnrollment.user_id==student.id))]
    d['lesson_progress']=[row(x) for x in db.scalars(select(m.Progress).where(m.Progress.user_id==student.id))]
    d['quiz_attempts']=[row(x,('answers',)) for x in db.scalars(select(m.QuizAttempt).where(m.QuizAttempt.user_id==student.id))]
    return d


def student_search_query(search:str, status:Literal['all','active','inactive'], sort:Literal['recent','name']):
    query=select(m.User)
    if search.strip():
        # SQLAlchemy parameterization avoids string-concatenated SQL. Literal
        # LIKE wildcards are escaped so '%' / '_' cannot bypass the filter.
        term=search.strip().replace('\\','\\\\').replace('%','\\%').replace('_','\\_')
        pattern=f'%{term}%'
        query=query.where(or_(m.User.full_name.ilike(pattern,escape='\\'),m.User.email.ilike(pattern,escape='\\')))
    if status!='all':
        query=query.where(m.User.is_active.is_(status=='active'))
    if sort=='name':
        query=query.order_by(m.User.full_name.asc(),m.User.id.asc())
    else:
        query=query.order_by(m.User.created_at.desc(),m.User.id.asc())
    return query


@app.get('/api/admin/students')
def admin_students(limit:int=Query(100,ge=1,le=100), offset:int=Query(0,ge=0),
                   db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    """Backward-compatible list response, now capped to prevent unlimited reads."""
    users=db.scalars(student_search_query('','all','recent').limit(limit).offset(offset)).all()
    return [student_admin_detail(db,student) for student in users]


@app.get('/api/admin/students/page')
def admin_students_page(page:int=Query(1,ge=1), page_size:int=Query(10,ge=1,le=50),
                        search:str=Query('',max_length=120),
                        status:Literal['all','active','inactive']='all',
                        sort:Literal['recent','name']='recent',
                        db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    """Server-side searchable, bounded admin pagination; no schema migration."""
    query=student_search_query(search,status,sort)
    total=db.scalar(select(func.count()).select_from(query.order_by(None).subquery())) or 0
    users=db.scalars(query.offset((page-1)*page_size).limit(page_size)).all()
    return {'items':[student_admin_detail(db,user) for user in users],
            'page':page,'page_size':page_size,'total':total,
            'pages':max(1,(total+page_size-1)//page_size)}

@app.patch('/api/admin/students/{ident}')
def admin_student_update(ident:str,data:dict=Body(...),db:Session=Depends(get_db),u:m.User=Depends(admin_user)):
    need(set(data) <= {'is_active','full_name'},'Only account status and name may be edited')
    obj=db.get(m.User,ident)
    if not obj:missing()
    if obj.id==u.id and data.get('is_active') is False:raise HTTPException(400,'Cannot deactivate yourself')
    for k,v in data.items():setattr(obj,k,v)
    db.commit();return user_view(obj)
