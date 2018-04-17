from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import time
import re, requests, os, sys

from other import get_asx_list, getFacebookID, createFields

class v2Company(Resource):
    
    asx_dict = get_asx_list()

    args = {
        'start_date': fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ", required=True),
        'end_date': fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ", required=True),
        'stats': fields.DelimitedList(fields.Str(), required=True),
    }
    
    # example usage: "/?stats=id,name,website,description"
    # stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
    @use_kwargs(args) 
    def get(self, name, start_date, end_date, stats):
        page_name = getFacebookID(str(name), self.asx_dict)

        #logging
        execution_start = time.time()

        if stats is not None:
            page_fields, post_fields = createFields(stats)

            # Get page stats
            page_stats = requests.get(
                "https://graph.facebook.com/v2.11/%s?fields=%s&access_token=%s" % (
                page_name, page_fields, 
                os.environ.get('FB_API_KEY'))).json() 

            if 'error' in page_stats.keys():
                page_stats['log_file'] = self.log_file(stats, page_stats['error']['message'], execution_start, time.time())
                return page_stats

            # Get page posts
            page_posts = requests.get(
                "https://graph.facebook.com/v2.11/%s/posts?fields=%s&since=%s&until=%s&access_token=%s" % (
                page_name, post_fields, start_date.timestamp(), end_date.timestamp(), 
                os.environ.get('FB_API_KEY'))).json()

            if 'error' in page_posts.keys():
                page_posts['log_file'] = self.log_file(stats, page_posts['error']['message'], execution_start, time.time())
                return page_posts

            page_posts = page_posts['data']

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

            response['log_file'] = self.log_file(stats, None, execution_start, time.time())
            

            #TODO: include instrument id
            return response

    def log_file(self, parameters, error, start, end):
        return {
                'team': 'QT314',
                'module_name': 'facebook_statistics/company',
                'version': 'v2',
                'parameters_passed': parameters,
                'error': error,
                'execution_start': start,
                'execution_end': end,
                'time_elapsed': end - start
               }
               
