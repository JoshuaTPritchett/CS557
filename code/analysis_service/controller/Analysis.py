from flask_restful import Resource, reqparse
from model.AnalysisEngine import AnalysisEngineModel
from model.AnalysisResult import AnalysisResultModel
from model.CodeSnippet import CodeSnippetModel
from controller.Helper import AnalysisWrapper

from app import app


db = app.config['db']

"""
Current implementation of the get and post functions only call these five actions:
Create  ---
Read    ---
Update  ---
Delete                                  ---
List(Search doesnt accept search query) ---
"""
class AnalysisCtrl(Resource):
    '''
    Issue a new analysis task which consist of analyzing one code snippet with all available engines
    '''
    def create(self, data):
        return [], 201

    '''
    Read analysis result of one single code snippet gathered from different engines
    '''
    def read(self, id):
        return [], 200

    '''
    Issue the engines to analyze an available code snippet again
    '''
    def update(self, id, data):
        return [], 200

    '''
    Remove a code snippet and all of the corresponding analysis result
    '''
    def delete(self, id):
        return [], 201

    '''
    Search/List of collected code snippet
    '''
    def list(self, offset=0, limit=10000):
        return [], 200


    """
    Rest inferface only requires GET/POST for this web service
    """
    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        args = parser.parse_args()

        #Check for ID in the req, if there is no id then grab entire list
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            else:
                return self.list()
        #We have an id and we want to delete or read, the two paths based on the URI definition in the app folder
        else:
            if args['delete'] == 1:
                return self.delete(id)
            else:
                return self.read(id)

    def post(self, id=None):
        parser = reqparse.RequestParser()
        #If no id then create a new analysis for code snippet
        if id is None:
            parser.add_argument('url', required=True, location='json')
            parser.add_argument('content', required=True, location='json')
            #Consider adding more arguments when we want to analyze code snippets

            return self.create(parser.parse_args())
        #Update exisiting analysis
        else:
            return self.update(id, parser.parse_args())
