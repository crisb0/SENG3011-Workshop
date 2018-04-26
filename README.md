Setup instructions
==================
1. Run `python3 -m venv flask`
2. Run `. flask/bin/activate` to activate the virtual environment
3. Run `pip3 install -r requirements.txt` to install all the required libraries
4. Run `./application.py`

Running Locally
==================
1. Go to the graph api explorer https://developers.facebook.com/tools/explorer/
2. Get personal user access token
3. Go to shell that you will be running the application on
4. Create environment variable `export FB_API_KEY="<USER_ACCESS_TOKEN>"`. To check if environ variable created successfully, `printenv`
5. Run `./application.py`

Calling endpoints
=================
To call endpoints execute `curl -X GET http://localhost:5000` and append the endpoint.
e.g. `curl -X GET "http://localhost:5000/company/company_name?start_time=2015-10-01T08:45:10.295Z&end_time=2015-10-01T08:45:10.295Z"`

Adding new libraries
====================
- When you add new libraries, make sure to update requirements.txt. You can do this by doing `pip freeze > requirements.txt`.

Testing
====================
running `python3 test.py` will make requests to different groups' APIs and generates HTML that contains the diff of the outputs for each pair.


