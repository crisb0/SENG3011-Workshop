#usr/bin/env python3
from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import re
import requests, os

# import fncs from files
from other import get_asx_list

app = Flask(__name__)
api = Api(app)


class Company(Resource):
    asx_dict = get_asx_list()
    print asx_dict.keys()[0] # testing only

    def getFacebookID(self, name):
        # name can be provided as ASX ticker code (WOW.ASX) OR company name (Woolworths)    
        # if ticker code (regex ***.ASX): look through dict
        company_name = name
        try:
            #if name provided is an instrument id
            match = re.match(r'([A-Za-z]{3})\.ASX', name).group(1)
            if match is not None and match in self.asx_dict:
                company_name = self.asx_dict[match]
                company_name = re.sub('\sLIMITED','',company_name)
                instrument_id = name
            else:
                print("Company not found")
                ### eRROR HANDLING REQUIRED
        except:
            pass

        #TODO: if company name string provided, find instrument id
        return company_name
                    
            

    args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'stats': fields.DelimitedList(fields.Str(), required=False),
                # example usage: "/?stats=id,name,website,description"
                # "/?stats=all" will return ALL POSSIBLE RESULTS
                # stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
            }
    @use_kwargs(args)
    ####################################
    #### GET                        ####
    #### INPUT: queries from args   ####
    #### RETURN: json output        ####
    ####################################
    # GET must return json output with: PageId, InstrumentIDs, CompanyNames, PageName, Website, Description, Category, fan_count, posts[id, type, message, created_time, like_count, comment_count]
    # def get(self, name, start_time, end_time, stats):
    #   page_name = self.getFacebookID(str(name));
    #   print stats;
    #   for x in stats:
    #       print x;
    #       # SEARCH FOR INTERESTED STATISTICS HERE
    #   print page_name;
    #   return "json obj";  

    def get(self, name, start_time, end_time, stats):
            # Check to see if name is an instrument id
                # if yes then convert
            page_name = self.getFacebookID(str(name))
            
            # Search for the company's facebook page and get it's page id
            page_search = requests.get("https://graph.facebook.com/v2.12/search?q=%s&type=page&fields=verification_status&access_token=%s" % (page_name, os.environ['FB_API_KEY'])).json()

            #Find the first blue verified result
            #TODO: Figure out how to validate that the page is the right one
            page_id = page_search['data'][0]['id']        
            for x in page_search['data']:
                if x['verification_status'] == 'blue_verified':
                    # print "FOUND BLUE VERIFIED"
                    page_id = x['id']
                    break;

            print "###############"
            print stats
            if 'id' in stats:
                print "YESSSSSSSSSSSSSSS"
            # Get page stats
            page_stats = requests.get("https://graph.facebook.com/v2.11/%s?fields=name,website,about,category,fan_count&access_token=%s" % (page_id, os.environ['FB_API_KEY'])).json()  
            print page_stats
            # Get page posts
            # page_posts = requests.get("https://graph.facebook.com/v2.11/%s/posts?access_token=%s" % (page_id, os.environ['FB_API_KEY'])).json()['data'] 

            # for post in range(len(page_posts)):
            #     #print(page_posts[post])
            #     temp_post = page_posts[post]
                
            #     temp_post['post_id'] = temp_post.pop('id')
            #     try: 
            #         temp_post['post_message'] = temp_post.pop('message') 
            #     except:
            #         pass
            #     temp_post['post_created_time'] = temp_post.pop('created_time')

            #     post_type = requests.get("https://graph.facebook.com/v2.11/%s?fields=type&access_token=%s" % (page_posts[post]['post_id'], os.environ['FB_API_KEY'])).json()['type']
            #     temp_post['post_type'] = post_type
                
            #     post_likes = requests.get("https://graph.facebook.com/v2.11/%s/likes?summary=true&access_token=%s" % (page_posts[post]['post_id'], os.environ['FB_API_KEY'])).json()['summary']['total_count']
            #     temp_post['post_like_count'] = post_likes


            #     post_comments = requests.get("https://graph.facebook.com/v2.11/%s/comments?summary=true&access_token=%s" % (page_posts[post]['post_id'], os.environ['FB_API_KEY'])).json()['summary']['total_count']
            #     temp_post['post_comment_count'] = post_comments

            #     page_posts[post] = temp_post
                


            # Make JSON result
            result = {}
            if 'id' in stats:
                result['PageId'] = page_stats.pop('id')
            #TODO: find instrument ID and Company Name
            # result['InstrumentIDs'] = name
            if 'name' in stats:
                result['PageName'] = page_stats.pop('name')
            if 'website' in stats:
                result['Website'] = page_stats.pop('website')
            if 'description' in stats:
                result['Description'] = page_stats.pop('about')
            if 'category' in stats:
                result['Category'] = page_stats.pop('category')
            if 'fan_count' in stats:
                result['fan_count'] = page_stats.pop('fan_count')
            # result['posts'] = page_posts
            
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