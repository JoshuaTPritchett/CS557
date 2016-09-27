from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import config, time, traceback, os, uuid

app = Flask(__name__)

logFile = "log-" + time.strftime("%Y-%m-%d-%H.%M.%S") + ".log"


"""
    Setup DB Models
"""
app.config['db'] = db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI

from model.CodeSnippet import CodeSnippetModel
from model.AnalysisEngine import AnalysisEngineModel
from model.AnalysisResult import AnalysisResultModel

db.drop_all()
db.create_all()
"""
Used for initialized based on the analysis engine
"""
import seed
db.session.commit()



"""
@app.before_first_request
def create_db():
    None
"""


"""
    Setup Routes
"""
from controller.Analysis import AnalysisCtrl


"""
Inits the app for the api, with the analysis controller
Based on the flask restful module and added to the path
"""
api = Api(app)
api.add_resource(AnalysisCtrl, '/api/analysis', '/api/analysis/<string:id>')




"""
Automaically called when a request has an error by Flask
"""
@app.errorhandler(Exception)
def handle_invalid_usage(error):
    message = time.strftime("%Y-%m-%d-%H.%M.%S") + ": \n" + traceback.format_exc() + "\n\n"
    with open(logFile, 'a') as f:
        f.write(message)
    rv = {}
    rv['message'] = message
    response = jsonify(rv)
    response.status_code = 500
    return response
