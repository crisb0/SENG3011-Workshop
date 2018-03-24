#!flask/bin/python
from flask import Flask, request
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 

app = Flask(__name__)
api = Api(app)

class Company(Resource):
    
    args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
    }
    
    @use_kwargs(args)
    def get(self, name, start_time, end_time):
        print name, start_time, end_time
        
        # Check to see if name is an instrument id
            # if yes then convert
        
        # Search for the company's facebook page and get it's page id

        # Get page stats

        # Get page posts

        # Make JSON result


        return {"name": name, "start": str(start_time), "end": str(end_time)}, 200

@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages)

if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)
