from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import time
import re, requests, os, sys

from datetime import datetime

def create_fb_request(page_name, stats, start_time, end_time):
    passthrough_stats = ["id", "name", "website", "description", "category", "fan_count"]
    post_fields = {
        "post_id": "id",
        "post_type": "type",
        "post_message": "message", 
        "post_created_time": "created_time", 
        "post_like_count": "likes.summary(true)", 
        "post_comment_count": "comments.summary(true).filter(toplevel)" 
    }
    top_level_stats = []
    per_post_stats = []

    for stat in stats:
        if stat in passthrough_stats:
            if stat == "description": stat = "about"
            top_level_stats.append(stat)
        elif stat in post_fields:
            per_post_stats.append(post_fields[stat])
    if per_post_stats:
        requested_post_fields = "posts.fields(%s).since(%s).until(%s)" % \
            (",".join(per_post_stats), int(start_time.timestamp()), int(end_time.timestamp()))
        requested_fields = ",".join(top_level_stats + [requested_post_fields]) 
    else:
        requested_fields = top_level_stats;
    access_token = os.environ.get('FB_API_KEY')
    request_string = "https://graph.facebook.com/v2.12/%s?fields=%s&access_token=%s" % (page_name, requested_fields, access_token)
    print(request_string)
    return request_string


class v3Company(Resource):
    
    args = {
        'start_date': fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ", required=True),
        'end_date': fields.DateTime(format="%Y-%m-%dT%H:%M:%SZ", required=True),
        'stats': fields.DelimitedList(fields.Str(), required=True)
    }

    # example usage: "/?stats=id,name,website,description"
    # stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
    @use_kwargs(args) 
    def get(self, name, start_date, end_date, stats):
        page_name = name #getFacebookID(str(name), self.asx_dict)

        #logging
        execution_start = time.time()

        result = {}

        if stats is not None:

            if start_date >= end_date: return self.log_file(stats, 'Invalid start_date, end_date parameters',execution_start, time.time())
            request_url = create_fb_request(page_name, stats,start_date, end_date)

            # Get page stats
            page_stats = requests.get(request_url).json() 

            if 'error' in page_stats.keys():
                page_stats['log_file'] = self.log_file(stats, page_stats['error']['message'], execution_start, time.time())
                return page_stats


            if 'posts' in page_stats: 
                page_posts = page_stats['posts']['data'] 

                if 'error' in page_stats.keys():
                    page_posts['log_file'] = self.log_file(stats, page_posts['error']['message'], execution_start, time.time())
                    return page_posts

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
            
                result['posts'] = page_posts

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


            
            response = {}
            response['FacebookStatisticData'] = result

            response['log_file'] = self.log_file(stats, None, execution_start, time.time())
            

            #TODO: include instrument id
            return response

    def log_file(self, parameters, error, start, end):
        return {
                'team': 'QT314',
                'module_name': 'facebook_statistics/company',
                'version': 'v3',
                'parameters_passed': parameters,
                'error': error,
                'execution_start': start,
                'execution_end': end,
                'time_elapsed': end - start
               }
               
