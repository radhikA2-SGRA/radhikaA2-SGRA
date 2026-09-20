from app.main import SessionLocal, User, Opportunity, Question, pwd, os
from sqlalchemy import select
s=SessionLocal()
if not s.scalar(select(Opportunity)):
    s.add_all([
      Opportunity(kind='scholarship',name='DEMO — Need-based education support',provider='Demo provider · verify before applying',description='Illustrative seed record only. Eligibility, amount and deadline are not official.',verification_status='Needs Review',is_demo=True),
      Opportunity(kind='scholarship',name='DEMO — STEM learner grant',provider='Demo provider · verify before applying',description='Illustrative STEM funding route. Check the official source for current criteria.',verification_status='Needs Review',is_demo=True),
      Opportunity(kind='college',name='DEMO — Government engineering college',provider='Demo institution · verify before relying',description='Illustrative college record. Fees, courses and admissions are intentionally not presented as facts.',verification_status='Needs Review',is_demo=True),
      Opportunity(kind='college',name='DEMO — Open learning university',provider='Demo institution · verify before relying',description='Illustrative flexible degree route. Confirm recognition and current admissions from the official website.',verification_status='Needs Review',is_demo=True)])
if not s.scalar(select(Question)):
    s.add_all([Question(text='If A is greater than B and B is greater than C, which is correct?',category='Reasoning',options='A is smallest|B is smallest|C is smallest|All are equal',answer='C is smallest'),Question(text='Which tool is commonly used to style a web page?',category='Computer',options='CSS|SQL|SMTP|DNS',answer='CSS'),Question(text='What is 15% of 200?',category='Mathematics',options='15|20|30|45',answer='30')])
s.commit(); print('Demo data ready. All records are marked for verification.')
