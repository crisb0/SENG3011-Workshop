#!flask/bin/python
from flask import Flask, request
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import requests, os

app = Flask(__name__)
api = Api(app)

class Company(Resource):
    
    args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
    }
    
    @use_kwargs(args)
    def get(self, name, start_time, end_time):
        
        # Check to see if name is an instrument id
            # if yes then convert
        
        # Search for the company's facebook page and get it's page id
        page_search = requests.get("https://graph.facebook.com/v2.12/search?q=%s&type=page&access_token=%s" % (name, os.environ['FB_API_KEY'])).json()

        # Use the first result
        #TODO: Figure out how to validate that the page is the right one
        page_id = page_search['data'][0]['id']        
        
        # Get page stats
        page_stats = requests.get("https://graph.facebook.com/v2.11/%s?fields=name,website,about,category,fan_count&access_token=%s" % (page_id, os.environ['FB_API_KEY'])).json()  
        
        # Get page posts
        page_posts = requests.get("https://graph.facebook.com/v2.11/%s/posts?access_token=%s" % (page_id, os.environ['FB_API_KEY'])).json()['data'] 

        for post in range(len(page_posts)):
            #print(page_posts[post])
            temp_post = page_posts[post]
            
            temp_post['post_id'] = temp_post.pop('id')
            temp_post['post_message'] = temp_post.pop('message')
            temp_post['post_created_time'] = temp_post.pop('created_time')

            post_type = requests.get("https://graph.facebook.com/v2.11/%s?fields=type&access_token=%s" % (page_posts[post]['post_id'], os.environ['FB_API_KEY'])).json()['type']
            temp_post['post_type'] = post_type
            
            post_likes = requests.get("https://graph.facebook.com/v2.11/%s/likes?summary=true&access_token=%s" % (page_posts[post]['post_id'], os.environ['FB_API_KEY'])).json()['summary']['total_count']
            temp_post['post_like_count'] = post_likes


            post_comments = requests.get("https://graph.facebook.com/v2.11/%s/comments?summary=true&access_token=%s" % (page_posts[post]['post_id'], os.environ['FB_API_KEY'])).json()['summary']['total_count']
            temp_post['post_comment_count'] = post_comments

            page_posts[post] = temp_post
            


        # Make JSON result
        result = page_stats
        result['CompanyNames'] = result.pop('name')
        result['PageId'] = result.pop('id')
        result['Category'] = result.pop('category')
        result['Description'] = result.pop('about')
        result['Website'] = result.pop('website')
        result['posts'] = page_posts           
        
        response = {}
        response['FacebookStatisticData'] = result

        #TODO: include instrument id




        return response

@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages)

if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)
