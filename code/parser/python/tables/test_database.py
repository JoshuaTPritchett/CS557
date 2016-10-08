from sqlalchemy     import create_engine
from sqlalchemy.orm import sessionmaker

from stack_overflow_declarative import Questions, Answers, Base

engine = create_engine('sqlite:///stack_overflow.db')

#Bind the associated metadata from the tables base class
Base.metadata.bind = engine


#Create the DBSession for the processing
DBSession = sessionmaker(bind=engine)


#   Creates a staging area of the all of the database objects to be loaded
#   None of the objects within the database will be updated until you call
#   commit(). Otherwise, call .rollback() on the session
session = DBSession()

#Example for questions
new_question = Questions(post_id=1, title='TEST QUESTION?', body='THIS IS AN EXAMPLE BODY')
session.add(new_question)
session.commit()
