#!flask/bin/python3
from flask import Flask
from flask_restful import Api, Resource, abort

from v1 import Company

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return "qt314 api"
 
if __name__ == '__main__':
    api.add_resource(Company, "/v1/company/<string:name>", endpoint='company')

    app.run(debug=True)
