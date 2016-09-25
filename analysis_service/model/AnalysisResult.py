from app import app
from datetime import *

db = app.config['db']


class AnalysisResultModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code_snippet_id = db.Column(db.Integer, db.ForeignKey('code_snippet_model.id'))
    code_snippet = db.relationship('CodeSnippetModel', foreign_keys=code_snippet_id)
    analysis_engine_id = db.Column(db.Integer, db.ForeignKey('analysis_engine_model.id'))
    analysis_engine = db.relationship('AnalysisEngineModel', foreign_keys=analysis_engine_id)
    raw_output = db.Column(db.String(512))
    msg  = db.Column(db.String(512))
    risk = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __init__(self, code, engine):
        self.code_snippet = code
        self.analysis_engine = engine

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}