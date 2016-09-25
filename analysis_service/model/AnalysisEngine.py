from app import app

db = app.config['db']


class AnalysisEngineModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    path = db.Column(db.String(512), nullable=False)
    cmd = db.Column(db.String(512), nullable=False)

    def __init__(self, name, path, cmd):
        self.name = name
        self.path = path
        self.cmd = cmd

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}