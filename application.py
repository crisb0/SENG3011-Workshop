#usr/bin/env python3
from flask import Flask
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser 

app = Flask(__name__)
api = Api(app)

class Company(Resource):

	# returns facebook page id
	def getFacebookID(self, name):
		# assume name will be provided as a searchable string e.g 'Woolworths'
		
		# use https://graph.facebook.com/v2.12/search?q=<keyword>&type=page
			# to search by instrument ID
		# else, search by string	


		# next step: name could be provided as ASX ticker code e.g. 'WOW.ASX'
		
    args = {
        'start_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
        'end_time': fields.DateTime(format="%Y-%m-%dT%H:%M:%S.%fZ", required=True),
		'name': fields.Str(required=True),
		#'stats': fields.DelimitedList(fields.Str(), required=True),
				# example usage: "/?stats=id,name,website,description"
				# stats can include id, name, website, description, category, fan_count, post_type, post_message, post_created_time, post_like_count, post_comment_count
    }
    @use_kwargs(args)
    def get(self, start_time, end_time, name):
		page_id = getFacebookID(name);
        return 		{"start": str(start_time), #TESTING PURPOSES ONLY
					 "end": str(end_time), #TESTING PURPOSES ONLY
					 "PageId"= str(page_id)},
					 200

@app.route('/')
def index():
    return "TESTESTEST QT314!"


@parser.error_handler
def handle_error(err):
    abort(422, errors=err.messages)

if __name__ == '__main__':
    api.add_resource(Company, "/company/<string:name>")
    app.run(debug=True)
