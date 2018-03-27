#usr/bin/env python3
from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 
import json, re

# import fncs from files
from other import get_asx_list

app = Flask(__name__)
api = Api(app)


class Company(Resource):
	asx_dict = get_asx_list()

	# returns facebook page id
	def getFacebookID(self, name):
		# name can be provided as ASX ticker code (WOW.ASX) OR company name (Woolworths)	
		# if ticker code (regex ***.ASX: look through dict
		company_name = name		
		match = re.match(r'([A-Za-z]{3})\.ASX', name).group(1)
		if match is not None and match in asx_dict:
			#if match in asx_dict
			company_name = asx_dict[match]
		else:
			pass #if not a match then must be a searchable company name already	

					
			
		# use https://graph.facebook.com/v2.12/search?q=<COMPANYNAME>&type=page

    args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
		'CompanyID': fields.Str(),	# e.g. 'WOW.AX' or 'Woolworths' 
										# (format is identified in getFacebookID)
		#'CompanyIDs': fields.Str(),	# e.g. 'Woolworths'
		'stats': fields.DelimitedList(fields.Str(), required=True),
				# example usage: "/?stats=id,name,website,description"
				# stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
			}
    @use_kwargs(args)
    def get(self, start_time, end_time, CompanyID):
		page_id = getFacebookID(CompanyID);
        #return 		{"start": str(start_time), #TESTING PURPOSES ONLY
		#			 "end": str(end_time), #TESTING PURPOSES ONLY
		#			 "PageId"= str(page_id)},
		#			 200
		return json.dumps(	{"Facebook Statistic Data":[
								{
									"Start": start_time,
									"End": end_time, 
									"PageId": page_id,
								
								}
							]

							),200

@app.route('/')
def index():
    return "TESTESTEST QT314!"


@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages) # 422 Unprocessable Entity

if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)
	

######## NOTES: #########
#How to identify correct page:
#https://graph.facebook.com/v2.12/search?q=<COMPANYNAME>&type=<PAGE/EVENT/WHATEVER>&fields=<ABOUT, FAN_COUNT, WEBSITE>
#Get the one 	with max(fan_count) 
#				OR keyword OFFICIAL
#				OR .com.au in their website (since we're dealing with AU companies, hopefully)
