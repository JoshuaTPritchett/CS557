#!/usr/bin/python

from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

from stack_overflow_declarative import Questions, Answers,Base

engine = create_engine('mysql://root:Password01!@localhost/stack_overflow')

#Any conversation with the database must be started with session
DBSession = sessionmaker(bind=engine)

#can be used for local instance of manipulation
session = DBSession()
#for pk_id in sess.query(Questions.post_id, Questions.title).order_by(Questions.post_id):
if session.query(Questions.title).all():
    for question in session.query(Questions.title).all():
        print question
