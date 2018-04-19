#!flask/bin/python3
from flask import Flask
from flask_restful import Api, Resource, abort
import requests
from v1 import Company as v1Company
from v2 import v2Company

def displayJSON():
    print("Displaying JSON...")
    result = requests.get("http://qt314.herokuapp.com/v1/company/atlassian?start_date=2015-10-01T08:45:10.295Z&end_date=2015-10-01T08:45:10.295Z&stats=id,name,website,description,category,fan_count,post_like_count,post_comment_count,post_type").json()
    print("Query successful...")
    result = result['FacebookStatisticData']

    return result['Description']



app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return "qt314 api" 

api.add_resource(v1Company, "/v1/company/<string:name>")
api.add_resource(v2Company, "/v2/company/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)
