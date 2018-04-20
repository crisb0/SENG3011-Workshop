#!flask/bin/python3
from flask import Flask, render_template, request, redirect
from flask_restful import Api, Resource, abort
from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser
import re
import requests, os
from v1 import Company as v1Company
from v2 import v2Company 

from other import get_asx_list, getFacebookID, createFields

def displayJSON(page, start, end, stats): #arguments will be all the query args: pageID, start_date, end_date, stats string
    print("Displaying JSON...")
    result = requests.get("http://qt314.herokuapp.com/v1/company/%s?start_date=%s&end_date=%s&stats=%s" % (page, start, end, stats)).json()
    print("Query successful...")

    result = result['FacebookStatisticData']

    # making the time look nice
    for i in result['posts']:
        if 'post_created_time' in i:
            temp = re.sub('[a-zA-Z]', ' ', i['post_created_time'])
            temp = re.sub('\+.*$', '', temp)
            i['post_created_time'] = temp

    return result



app = Flask(__name__)
api = Api(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods = ['POST'])
def result():
    form = request.form
    stats_list = []
    stat1 = request.form.get('stat_id')
    if stat1:
        stats_list.append('id')
    stat2 = request.form.get('stat_name')
    if stat2:
        stats_list.append('name')
    stat3 = request.form.get('stat_website')
    if stat3:
        stats_list.append('website')
    stat4 = request.form.get('stat_description')
    if stat4:
        stats_list.append('description')
    stat5 = request.form.get('stat_category')
    if stat5:
        stats_list.append('category')
    stat6 = request.form.get('stat_fancount')
    if stat6:
        stats_list.append('fan_count')
    stat7 = request.form.get('stat_postlikecount')
    if stat7:
        stats_list.append('post_like_count')
    stat8 = request.form.get('stat_postcommentcount')
    if stat8:
        stats_list.append('post_comment_count')
    stat9 = request.form.get('stat_posttype')
    if stat9:
        stats_list.append('post_type')
    stat10 = request.form.get('stat_postmessage')
    if stat10:
        stats_list.append('post_message')
    stats = ",".join(stats_list)

    result = displayJSON(form['Page'],form['Start'], form['End'], stats)
    return render_template("results.html", result=result)

api.add_resource(v1Company, "/v1/company/<string:name>")
api.add_resource(v2Company, "/v2/company/<string:name>")
if __name__ == '__main__':
    app.run(debug=True)
