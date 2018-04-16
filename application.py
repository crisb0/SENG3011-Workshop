#!flask/bin/python3
from flask import Flask
from flask_restful import Api, Resource, abort

from v1 import Company as v1Company
from v2 import v2Company

app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return "qt314 api"
 
if __name__ == '__main__':
    api.add_resource(v1Company, "/v1/company/<string:name>")
    api.add_resource(v2Company, "/v2/company/<string:name>")

    app.run(debug=True)
