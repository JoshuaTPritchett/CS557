from app import app
from datetime import *
import hashlib

db = app.config['db']


class CodeSnippetModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(512), nullable=False)
    original_content = db.Column(db.String(16384), nullable=False)
    hash = db.Column(db.String(40), nullable=False)
    analysis_content = db.Column(db.String(16384))
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                       nullable=False,
                       default=datetime.utcnow,
                       onupdate=datetime.utcnow)

    def __init__(self, url, content):
        self.url = url
        self.original_content = content
        self.hash = hashlib.sha256(content).hexdigest()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}