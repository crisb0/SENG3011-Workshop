#!flask/bin/python3
from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import re
import requests, os

# import fncs from files
from other import get_asx_list, getFacebookID, createFields

app = Flask(__name__)
api = Api(app)

class Company(Resource):
    
    asx_dict = get_asx_list()

    args = {
        'start_date': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_date': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'stats': fields.DelimitedList(fields.Str(), required=True),
    }
    
    # example usage: "/?stats=id,name,website,description"
    # stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
    @use_kwargs(args) 
    def get(self, name, start_date, end_date, stats):
        page_name = getFacebookID(str(name), self.asx_dict)
        
        if stats is not None:
            page_fields, post_fields = createFields(stats)

            # Get page stats
            page_stats = requests.get("https://graph.facebook.com/v2.11/%s?fields=%s&access_token=%s" % (page_name, page_fields, os.environ.get('FB_API_KEY'))).json() 

            # Get page posts
            page_posts = requests.get("https://graph.facebook.com/v2.11/%s/posts?fields=%s&access_token=%s" % (page_name, post_fields, os.environ.get('FB_API_KEY'))).json()['data'] 

            # JSON OUTPUT
            for post in range(len(page_posts)):
                if 'post_id' in stats:
                    page_posts[post]['post_id'] = page_posts[post].pop('id')
                if 'post_type' in stats:
                    page_posts[post]['post_type'] = page_posts[post].pop('type')
                if 'post_like_count' in stats:
                    page_posts[post]['post_like_count'] = page_posts[post]['likes']['summary']['total_count']
                    page_posts[post].pop('likes')
                if 'post_comment_count' in stats:
                    page_posts[post]['post_comment_count'] = page_posts[post]['comments']['summary']['total_count']
                    page_posts[post].pop('comments')
                if 'post_message' in stats and 'message' in page_posts[post]:
                         page_posts[post]['post_message'] = page_posts[post].pop('message')
                if 'post_created_time' in stats:
                        page_posts[post]['post_created_time'] = page_posts[post].pop('created_time')

            result = {}
            if 'id' in stats:
                result['PageId'] = page_stats.pop('id')
            #TODO: find instrument ID and Company Name
            if 'name' in stats:
                result['PageName'] = page_stats.pop('name')
            if 'website' in stats and 'website' in page_stats:
                result['Website'] = page_stats.pop('website')
            if 'description' in stats and 'about' in page_stats:
                result['Description'] = page_stats.pop('about')
            if 'category' in stats:
                result['Category'] = page_stats.pop('category')
            if 'fan_count' in stats:
                result['fan_count'] = page_stats.pop('fan_count')


            result['posts'] = page_posts
            
            response = {}
            response['FacebookStatisticData'] = result

            #TODO: include instrument id
            return response

@app.route('/')
def index():
    return "qt314 api"
 
@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages) # 422 Unprocessable Entity

api.add_resource(Company, "/v1/company/<string:name>", endpoint='company')
if __name__ == '__main__':

    app.run(debug=True)
