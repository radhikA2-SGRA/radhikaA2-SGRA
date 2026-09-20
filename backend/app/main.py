from datetime import datetime, timedelta
import os
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./opportunity_finder.db'); SECRET=os.getenv('JWT_SECRET','dev-only-change-me'); ALGORITHM='HS256'
connect_args={'check_same_thread':False} if DATABASE_URL.startswith('sqlite') else {}
engine=create_engine(DATABASE_URL,connect_args=connect_args); SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
class Base(DeclarativeBase): pass
class User(Base):
    __tablename__='users'; id:Mapped[int]=mapped_column(primary_key=True); name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(255),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(255)); role:Mapped[str]=mapped_column(String(20),default='student'); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class StudentProfile(Base):
    __tablename__='student_profiles'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('users.id'),unique=True); state:Mapped[str]=mapped_column(String(80),default=''); city:Mapped[str]=mapped_column(String(80),default=''); education_level:Mapped[str]=mapped_column(String(80),default=''); tenth_percentage:Mapped[Optional[float]]=mapped_column(nullable=True); twelfth_percentage:Mapped[Optional[float]]=mapped_column(nullable=True); career_goal:Mapped[str]=mapped_column(String(160),default=''); interests:Mapped[str]=mapped_column(Text,default=''); updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
class Opportunity(Base):
    __tablename__='opportunities'; id:Mapped[int]=mapped_column(primary_key=True); kind:Mapped[str]=mapped_column(String(30),index=True); name:Mapped[str]=mapped_column(String(200)); provider:Mapped[str]=mapped_column(String(200)); description:Mapped[str]=mapped_column(Text); source_url:Mapped[Optional[str]]=mapped_column(String(500),nullable=True); verification_status:Mapped[str]=mapped_column(String(30),default='Needs Review'); is_demo:Mapped[bool]=mapped_column(Boolean,default=True); last_verified_date:Mapped[Optional[datetime]]=mapped_column(nullable=True)
class Question(Base):
    __tablename__='questions'; id:Mapped[int]=mapped_column(primary_key=True); text:Mapped[str]=mapped_column(Text); category:Mapped[str]=mapped_column(String(50)); options:Mapped[str]=mapped_column(Text); answer:Mapped[str]=mapped_column(String(10)); marks:Mapped[int]=mapped_column(Integer,default=1)
Base.metadata.create_all(engine)
pwd=CryptContext(schemes=['bcrypt'],deprecated='auto'); oauth2=OAuth2PasswordBearer(tokenUrl='/api/auth/login')
class Register(BaseModel): name:str=Field(min_length=2,max_length=120); email:EmailStr; password:str=Field(min_length=8); state:str=Field(min_length=2); city:str=Field(min_length=2); education_level:str=Field(min_length=2)
class Login(BaseModel): email:EmailStr; password:str
class ProfileUpdate(BaseModel): state:Optional[str]=None; city:Optional[str]=None; education_level:Optional[str]=None; tenth_percentage:Optional[float]=Field(default=None,ge=0,le=100); twelfth_percentage:Optional[float]=Field(default=None,ge=0,le=100); career_goal:Optional[str]=None; interests:Optional[str]=None
class AnswerSubmit(BaseModel): answers:dict[str,str]
def db():
    s=SessionLocal()
    try: yield s
    finally:s.close()
def token_for(u:User): return jwt.encode({'sub':str(u.id),'exp':datetime.utcnow()+timedelta(minutes=int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES','60')))},SECRET,algorithm=ALGORITHM)
def current(token:str=Depends(oauth2),s:Session=Depends(db)):
    try: uid=int(jwt.decode(token,SECRET,algorithms=[ALGORITHM])['sub'])
    except (JWTError,KeyError,ValueError): raise HTTPException(status_code=401,detail='Invalid or expired login')
    u=s.get(User,uid)
    if not u: raise HTTPException(status_code=401,detail='User not found')
    return u
app=FastAPI(title='Opportunity Finder API',version='1.0.0')
orig=os.getenv('CORS_ORIGINS','http://localhost:5173').split(','); app.add_middleware(CORSMiddleware,allow_origins=orig,allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
@app.get('/api/health')
def health(): return {'status':'ok'}
@app.post('/api/auth/register')
def register(data:Register,s:Session=Depends(db)):
    if s.scalar(select(User).where(User.email==data.email)): raise HTTPException(409,'An account with this email already exists')
    u=User(name=data.name,email=data.email,password_hash=pwd.hash(data.password));s.add(u);s.flush();s.add(StudentProfile(user_id=u.id,state=data.state,city=data.city,education_level=data.education_level));s.commit();return {'id':u.id,'name':u.name,'email':u.email,'role':u.role,'token':token_for(u)}
@app.post('/api/auth/login')
def login(data:Login,s:Session=Depends(db)):
    u=s.scalar(select(User).where(User.email==data.email))
    if not u or not pwd.verify(data.password,u.password_hash): raise HTTPException(401,'Email or password is incorrect')
    return {'id':u.id,'name':u.name,'email':u.email,'role':u.role,'token':token_for(u)}
@app.get('/api/student/profile')
def profile(u:User=Depends(current),s:Session=Depends(db)):
    p=s.scalar(select(StudentProfile).where(StudentProfile.user_id==u.id)); filled=sum(bool(getattr(p,x)) for x in ['state','city','education_level','career_goal','interests','tenth_percentage','twelfth_percentage']); return {'name':u.name,'email':u.email,'completion':round(filled/7*100),'profile':p.__dict__ if p else {}}
@app.put('/api/student/profile')
def update_profile(data:ProfileUpdate,u:User=Depends(current),s:Session=Depends(db)):
    p=s.scalar(select(StudentProfile).where(StudentProfile.user_id==u.id));
    if not p:p=StudentProfile(user_id=u.id);s.add(p)
    for k,v in data.model_dump(exclude_none=True).items():setattr(p,k,v)
    s.commit();return {'message':'Profile updated'}
@app.get('/api/scholarships')
def scholarships(s:Session=Depends(db)): return [serialize(x) for x in s.scalars(select(Opportunity).where(Opportunity.kind=='scholarship')).all()]
@app.get('/api/colleges')
def colleges(s:Session=Depends(db)): return [serialize(x) for x in s.scalars(select(Opportunity).where(Opportunity.kind=='college')).all()]
def serialize(x): return {'id':x.id,'name':x.name,'provider':x.provider,'description':x.description,'source_url':x.source_url,'is_demo':x.is_demo,'verification_status':x.verification_status,'reasons':['This is a demo record; complete your profile for personalized matching.']}
@app.get('/api/assessment/questions')
def questions(s:Session=Depends(db)): return [{'id':q.id,'text':q.text,'category':q.category,'options':q.options.split('|')} for q in s.scalars(select(Question)).all()]
@app.post('/api/assessment/submit')
def assessment(data:AnswerSubmit,u:User=Depends(current),s:Session=Depends(db)):
    qs=s.scalars(select(Question)).all(); scores={}; totals={}
    for q in qs: totals[q.category]=totals.get(q.category,0)+q.marks; scores[q.category]=scores.get(q.category,0)+(q.marks if data.answers.get(str(q.id))==q.answer else 0)
    categories={k:round(v/totals[k]*100) for k,v in scores.items()}; overall=round(sum(scores.values())/max(sum(totals.values()),1)*100); return {'overall':overall,'categories':categories,'strengths':[k for k,v in categories.items() if v>=70],'improve':[k for k,v in categories.items() if v<60]}
@app.post('/api/roadmap/generate')
def roadmap(u:User=Depends(current)): return {'goal':'Your chosen career goal','steps':[{'title':'Build your foundation','description':'Choose one core skill and practise it weekly.'},{'title':'Make evidence','description':'Create projects, achievements or a portfolio.'},{'title':'Explore opportunities','description':'Check verified courses, scholarships and internships.'},{'title':'Review and adapt','description':'Update your plan as your interests and strengths grow.'}]}
