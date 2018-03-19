#!/usr/bin/env python3
from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

class Company(Resource):
    def get(self, name):
        if name == "Viv":
            return name, 200
        return "Never heard of this company", 404

@app.route('/')
def index():
    return "Hello, World!"



if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)
