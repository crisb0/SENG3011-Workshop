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
    # print asx_dict.keys()[0] # testing only

    args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'stats': fields.DelimitedList(fields.Str(), required=False),
                # example usage: "/?stats=id,name,website,description"
                # "/?stats=all" will return ALL POSSIBLE RESULTS
                # stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
            }
    @use_kwargs(args) 

    def get(self, name, start_time, end_time, stats):
            # Check to see if name is an instrument id
                # if yes then convert
            page_name = getFacebookID(str(name), self.asx_dict)
            if stats is not None:
                page_fields, post_fields = createFields(stats)

            # Search for the company's facebook page and get it's page id
            page_search = requests.get("https://graph.facebook.com/v2.12/search?q=%s&type=page&fields=verification_status&access_token=%s" % (page_name, os.environ['FB_API_KEY'])).json()
            #print page_search

            #Find the first blue verified result
            #TODO: Figure out how to validate that the page is the right one
            page_id = page_search['data'][0]['id']        
            for x in page_search['data']:
                if x['verification_status'] == 'blue_verified':
                    page_id = x['id']
                    break;

            # Get page stats
            page_stats = requests.get("https://graph.facebook.com/v2.11/%s?fields=%s&access_token=%s" % (page_id, page_fields, os.environ['FB_API_KEY'])).json()  
            # Get page posts
            page_posts = requests.get("https://graph.facebook.com/v2.11/%s/posts?fields=%s&access_token=%s" % (page_id, post_fields, os.environ['FB_API_KEY'])).json()['data'] 

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
            # result['InstrumentIDs'] = name

            if 'name' in stats:
                result['PageName'] = page_stats.pop('name')
            if 'website' in stats and 'website' in page_stats:
                result['Website'] = page_stats.pop('website')
            if 'description' in stats and 'description' in page_stats:
                result['Description'] = page_stats.pop('description')
            if 'category' in stats:
                result['Category'] = page_stats.pop('category')
            if 'fan_count' in stats:
                result['fan_count'] = page_stats.pop('fan_count')


            result['posts'] = page_posts
            
            response = {}
            response['FacebookStatisticData'] = result

            #TODO: include instrument id
            return response
          
@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages) # 422 Unprocessable Entity

if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)