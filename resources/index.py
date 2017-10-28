from flask_restful import Resource, reqparse
from flask import redirect

class Index(Resource):
    def get(self):
        return redirect('/users')
