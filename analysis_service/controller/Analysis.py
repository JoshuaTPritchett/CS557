from flask_restful import Resource, reqparse
from model.AnalysisEngine import AnalysisEngineModel
from model.AnalysisResult import AnalysisResultModel
from model.CodeSnippet import CodeSnippetModel
from controller.Helper import AnalysisWrapper

from app import app


db = app.config['db']


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

    def get(self, id=None):
        parser = reqparse.RequestParser()
        parser.add_argument('delete', type=int)
        parser.add_argument('offset', type=int)
        parser.add_argument('limit', type=int)
        args = parser.parse_args()
        if id is None:
            if args['offset'] is not None and args['limit'] is not None:
                return self.list(args['offset'], args['limit'])
            else:
                return self.list()
        else:
            if args['delete'] == 1:
                return self.delete(id)
            else:
                return self.read(id)

    def post(self, id=None):
        parser = reqparse.RequestParser()
        if id is None:
            parser.add_argument('url', required=True, location='json')
            parser.add_argument('content', required=True, location='json')
            return self.create(parser.parse_args())
        else:
            return self.update(id, parser.parse_args())