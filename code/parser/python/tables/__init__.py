#!/usr/bin/python
"""
    The global variables that are going to be used
    withn the stack overflow project to manipulate the
    database.

    Python 2.7.12

    @author Joshua T. Pritchett <jtpritchett@cs.wpi.edu>
    @copyright ALAS LAB WPI, 2016
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from stack_overflow_declarative import Questions, Answers, Base

#   Will determine the SQLite database that we want to
#   connect to.
engine = create_engine('sqlite:///stack_overflow.db')

#   In case we awant to do any inserts or updates to the table
#   values within the database
Base.metadata.bind = engine


#   Create the overall database session we will use
#   If we want we can use DBSession() to create local
#   connections that we can use for later within the
#   database processing environment. If we do not
#   create a session there could be an accident over-
#   writing of data.

#   To write to the database try: your operation:
#       .add()
#       .commit()
#   If there is a failure then you should use except:
#       .rollback()
#   This will wipe all of the temporary data, but will
#   prevent the database from beig corrupted
DBSession = sessionmaker(bind=engine)
session = DBSession()
for pk_id in session.query(Questions.post_id).all():
    print pk_id
