"""
    Creates SQLLite tables using SQL Alchemy for Stack Overflow Project

    @author Joshua T. Prithchett <jtpritchett@wpi.edu>
    @copyright ALAS LAB WPI, 2016
"""

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

class Questions(Base):
    __tablename__ = 'questions'
    """
        Attributes:
            id_pk                       -- the unique index for the row in the database
            post_id                     -- post ID for the specific question
            title                       --  title of the post
            tags                        -- any tag information reguarding language
            last_editor_display_name    -- the last person to edit the post
            body                        --  the body of text for the question
            score                       --  score (importance) of question (# upvotes - # downvotes)
            view_count                  --  amount of views for a given post
            answer_count                --  number of answers
            comment_count               --  number of comments for post
            favorite_count              --  number of favorites
            owner_user_id               --  user id of the person who created the question
            accepted_answer_id          --  answer that had the most upvotes
            last_editor_user_id         --  last person to edit the post
            creation_date               --  date the question was created
            last_edit_date              --  last date the post was edited
            last_activity_date          --  last date in which someone produced activity for the post1
            community_owned_date        --  a post has become community owned
    """

    id_pk                       = Column(Integer    , primary_key=True)
    post_id                     = Column(Integer    , nullable=False)
    title                       = Column(String(512), nullable=False)
    tags                        = Column(String(128), nullable=True)
    last_editor_display_name    = Column(String(128), nullable=True)
    body                        = Column(Text       , nullable=False)
    score                       = Column(Integer    , nullable=True)
    view_count                  = Column(Integer    , nullable=True)
    answer_count                = Column(Integer    , nullable=True)
    comment_count               = Column(Integer    , nullable=True)
    favorite_count              = Column(Integer    , nullable=True)
    owner_user_id               = Column(Integer    , nullable=True)
    accepted_answer_id          = Column(Integer    , nullable=True)
    last_editor_user_id         = Column(Integer    , nullable=True)
    creation_date               = Column(DateTime   , nullable=True)
    last_edit_date              = Column(DateTime   , nullable=True)
    last_activity_date          = Column(DateTime   , nullable=True)
    community_owned_date        = Column(DateTime   , nullable=True) #could cause problems

class Answers(Base):
    __tablename__ = 'Answers'
    """
        Attributes:
            id_pk                       -- the unique index for the row in the database
            answer_id                   -- post ID for the specific question
            parent_id                   -- any tag information reguarding language
            owner_user_id               --  user id of the person who created the question
            score                       --  score (importance) of question (# upvotes - # downvotes)
            comment_count               --  number of comments for post
            last_editor_user_id         --  last person to edit the post
            last_editor_display_name    --  last date the post was edited
            last_edit_date              --  last date in which someone produced activity for the post1
            last_activity_date          --  title of the post
            creation_date               --  date the question was created
            community_owned_date        --  a post has become community owned
            code                        --  amount of views for a given post
    """
    id_pk                       = Column(Integer    , primary_key=True)
    answer_id                   = Column(Integer    , nullable=False)
    parent_id                   = Column(Integer    , nullable=False)
    owner_user_id               = Column(Integer    , nullable=False)
    score                       = Column(Integer    , nullable=False)
    comment_count               = Column(Integer    , nullable=False)
    last_editor_user_id         = Column(Integer    , nullable=False)
    last_editor_display_name    = Column(String(64) , nullable=False)
    last_edit_date              = Column(DateTime   , nullable=False)
    last_activity_date          = Column(DateTime   , nullable=False)
    creation_date               = Column(DateTime   , nullable=False)
    community_owned_date        = Column(DateTime   , nullable=False)
    code                        = Column(Text       , nullable=False)


# Leverages sql_create engine to create the tables for the database
engine = create_engine('sqlite:///stack_overflow.db')

#Create the tables with the metdata information
# Same as CREATE TABLE in raw SQL
Base.metadata.create_all(engine)
