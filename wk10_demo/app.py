#!flask/bin/python3
from flask import Flask, render_template, request, redirect
from datetime import datetime, date
import requests, os
from operator import itemgetter
from itertools import islice
from forms import LoginForm, RegistrationForm 
from flask_login import LoginManager
from user import User

app = Flask(__name__, static_url_path='/static')
lm = LoginManager(app)

company = {'name':'COCA-COLA AMATIL LIMITED', 'asx':'CCL', 'fbName':'CocaColaAustralia'}
now = datetime.now()
now_date = now.strftime("%Y-%m-%d")

@lm.user_loader
def load_user(id):
    from db_helpers import query_db
    user = query_db('select * from users where id = %s'%(id), (), True)
    return User(user)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("auth.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    import db_helpers

    registration_form = RegistrationForm(request.form)
    db = db_helpers.get_db()
    cur = db.cursor()

    if request.method == 'POST' and registration_form.validate():
        result = request.form
        # check that the company doesn't already exist
        
        # make db entry
        #print('insert into users (email, password, companyName, companyUrl) values ("%s", "%s", "%s", "%s")'%(result['email'], result['password'], result['company_name'], result['company_url'])) 

        cur.execute(
                 'insert into users (email, password, companyName, companyUrl) values ("%s", "%s", "%s", "%s")'%(result['email'], result['password'], result['company_name'], result['company_url']) 
                 )
        db.commit()
        return redirect('/login')
    
    return render_template("reg.html", form=registration_form)

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

@app.route('/createCampaign', methods=['GET', 'POST'])
def createCampaign():
    goals = []
    form = request.form
    if request.method == 'POST':
        new_goal = {}
        new_goal['Goal Start Date'] = request.form.get('start_date')
        new_goal['Goal End Date'] = request.form.get('end_date')
        new_goal['Comments target'] = request.form.get('comment_count')
        new_goal['Likes target'] = request.form.get('like_count')
        print(new_goal)
        goals.append(new_goal)
        return render_template("createCampaign.html", goals=goals)
        #return all_campaigns(goals)
    else:
        return render_template("createCampaign.html", goals=[])

@app.route('/campaigns', methods=['GET', 'POST'])
def all_campaigns(goals):
    print(goals)
    return render_template("createCampaign.html", goals=goals)

@app.route('/viewCampaign')
def viewCampaign():
    return render_template("viewCampaign.html")

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
