from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

from stack_overflow_declarative import Questions, Answers,Base
engine = create_engine('sqlite:///stack_overflow.db')

#Any conversation with the database must be started with session
DBSession = sessionmaker(bind=engine)

#can be used for local instance of manipulation
sess = DBSession()
for pk_id in sess.query(Questions.post_id, Questions.title).order_by(Questions.post_id):
    print pk_id
