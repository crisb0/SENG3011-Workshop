Setup instructions
==================
1. Run `pip install flask flask-restful`
2. Run `./app.py`


Testing
==================
This is only a test for the skeleton which echos "Viv"
* Install Postman OR Insomnia on your computer (They are API testing tools)
* Once you have the app running in your local host
* put http://127.0.0.1:5000/company/Viv?start_time=2015-10-01T08:45:10.295Z&end_time=2015-10-01T08:45:10.295Z `should return a JSON object with Name, Start and End
* Other invalid input should throw an error

`curl -X GET http://localhost:5000`
