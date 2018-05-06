#!flask/bin/python3
from flask import Flask, render_template
from datetime import datetime, date
import requests, os
from operator import itemgetter
from itertools import islice

app = Flask(__name__, static_url_path='/static')

company = {'name':'COCA-COLA AMATIL LIMITED', 'asx':'CCL', 'fbName':'CocaColaAustralia'}
now = datetime.now()
now_date = now.strftime("%Y-%m-%d")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("auth.html")

@app.route('/register')
def register():
    return render_template("reg.html")

@app.route('/dashboard')
def dashboard():
    
    end_date = (subtract_years(now, 1)).strftime("%Y-%m-%d")
    stats = "id,name,website,description,category,fan_count,post_like_count,post_comment_count,post_type,post_message"
    facebook = displayFacebookJSON(company.get('fbName'), end_date+'T00:00:00Z', now_date+'T00:00:00Z', stats)['FacebookStatisticData']
    
    total_likes = 0
    for post in facebook['posts']:
        total_likes += post['post_like_count']

    facebook_data={}
    facebook_data['num_posts'] = len(facebook['posts'])
    facebook_data['daily_posts'] = round(facebook_data['num_posts']/365, 2)
    facebook_data['avg_react_per_post'] = round(total_likes/facebook_data['num_posts'], 2)
    
    # should be done by sentiment but whatever
    post_popularity=islice(sort_posts(facebook['posts']), 10)

    return render_template("dashboard.html", company=company, facebook=facebook, facebook_data=facebook_data, post_popularity=post_popularity)

@app.route('/trackCampaigns')
def trackCampaigns():
    return render_template("trackCampaigns.html")
    
@app.route('/createCampaign')
def createCampaign():
    return render_template("createCampaign.html")

# add any other routes above

#helper methods
def displayStocksJSON(id, date, lower, upper):
    result = requests.get("http://team-distribution.info/api/v3/returns?id=%s&date=%s&varlist=CM_Return&lower=%s&upper=%s" % (id, date, lower, upper)).json()
    return result

def displayFacebookJSON(page, start, end, stats):
    print("Displaying JSON...")
    print("query: " + "http://qt314.herokuapp.com/v2/company/%s?start_date=%s&end_date=%s&stats=%s" % (page, start, end, stats))
    result =  requests.get("http://qt314.herokuapp.com/v2/company/%s?start_date=%s&end_date=%s&stats=%s" % (page, start, end, stats)).json()
    print("Query successful")
    print(result)
    # making the time look nice
    if 'posts' in result:
        print("POSTS HERE")
        for i in result['posts']:
            if 'post_created_time' in i:
                temp = re.sub('[a-zA-Z]', ' ', i['post_created_time'])
                temp = re.sub('\+.*$', '', temp)
                i['post_created_time'] = temp

    if 'Website' in result:
        result['Website'] = re.sub('.*//', '', result['Website'])
    
    return result

def subtract_years(dt, years):
    try:
        dt = dt.replace(year=dt.year-years)
    except ValueError:
        dt = dt.replace(year=dt.year-years, day=dt.day-1)
    return dt

def sort_posts(posts):
    result = sorted(posts, key=itemgetter('post_like_count'), reverse=True)
    return result

if __name__ == "__main__":
    app.run(debug=True)
