# Synthesis
## RESTful API 
## Last Updated: 05/04/2020
### Synthesis - The Automatic Garden
### Authors: Leo Au-Yeung, Stanley Lim, Daniel Mallia, Jayson Tan


This repository contains the code developed by the above authors in the 
Spring 2020 CSCI Capstone course under Professor Maryash at Hunter College, for 
the purpose of running an automated garden with a web interface. 

### Getting Started 
1. Please follow below instructions to set up a Python environment
2. In addition, please check out other directories with their respective setup including: 
    - [Raspberry Pi Hardware setup](https://github.com/tanj299/synthesis/tree/python-arduino-dev)
    - [React Application](https://github.com/tanj299/synthesis/tree/master/frontend-new)
    - [Flutter Application](https://github.com/tanj299/synthesis/tree/flutter-app-dev)

### Prerequisites 

1. Install [Python](https://www.python.org/ "Python Main page") 

    On Mac: You can use Homebrew to install Python using
    ~~~~
    brew install python
    ~~~~

    By default, pip (Python package manager) is included in Python 2.7.9> and pip3 is included for Python 3.4>

2. Install virtualenv via pip - we will use Python's virtual environment so as not to muddle with your OS' Python version
    ~~~~
    python3 -m pip install --user -upgrade pip
    ~~~~

### Setup Environment and Run Script
1.  Clone or pull this repository, ```cd``` into the directory, and create a virtual environment  
	~~~~
	cd <THIS_FOLDER_NAME>
    python3 -m venv env
	~~~~

2.  Activate the virtual environment:
	~~~~
	$ source env/bin/activate
	~~~~
    You should see ```(env)``` activated next to the shell prompt

3.  Install ```requirements.txt```, which are all the dependencies for this project
    ~~~~
    $ pip3 install -r requirements.txt
    ~~~~

4.  In your terminal, set your Flask environment variable to `main.py`; run the following:
    ~~~~
    $ export FLASK_APP=main.py
    $ flask run 
    ~~~~
    **Note: There is NO whitespace between `FLASK_APP=<file_name>`**

    If you want to be lazy and not have to run `export FLASK_APP=main.py` every time, create a `.env` file and add the following:
    ~~~~
    #.env file
    FLASK_APP=main
    FLASK_ENV=development
    ~~~~

    Now you can just use `flask run` and it will use `main.py` as the Flask app

    Alternatively, you can run the Flask app directly:
    ~~~~
    $ python main.py
    ~~~~

5. After setting up the environment, you should see the following: 
    ```
    * Serving Flask app "main.py"
    * Environment: developement
    * Debug mode: off
    Execute `flask run` instead
    Execute `flask run` instead
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```
    Congratulations, your Flask backend is now running! Go to your favorite browser and go to 
    `localhost:5000` (or `http://127.0.0.1:5000/`) and you will be greeted with `Welcome to the backend!`

    **05/04/2020: Flask application deployed <br/>
    See "Deployment" section for details**

### Notes
GET Request: The `time` argument must be converted from a string to a formatted time string to be queried<br/>
Datetime object format: `2020-04-30 04:10:38`<br/>
Formatted to: `2020-04-30+04%3A10%3A38`<br/>
For all colons (:) in string, it must be replaced with: `%3A`<br/>
For all whitespace in string, it must be replaced with: `+`<br/>
Above is a custom Python function, def convert_time_format(date), which takes in a datetime object <br/>
And returns an appropriate string for querying; however, this must be done on client-side<br/>

### Routes Supported
Routes are modularized using Flask's Blueprint object<br/> 
You can find the registered blueprint objects in `main.py` for the `url_prefix`<br/>
They are also listed here for your convenience. <br/>

Route format: `localhost:5000/<REGISTERED_BLUEPRINT>/<ROUTE_DECORATOR>`<br/>

**Example route using `plants` prefix, `/plants`, to fetch all plants:**
<br/>
<br/>
`localhost:5000/plants/all`
<br/>
<br/> 
Format:<br/>
`REQUEST_METHOD` | `ROUTE_DECORATOR`: Description
<br/><br/>


**Plants | `plants.py`**<br/>
`url_prefix`: `/plants`
<br/>
`POST`      | `/insert`: Add a plant to the database<br/>
`GET`       | `/all`: Fetch all plants<br/>
`GET`       | `/plant/<int:id>`: Fetch a single plant via their ID number<br/>
`DELETE`    | `/plant/<int:id>`: Remove a single plant via their ID number<br/>
`PUT`       | `/update/<int:id>`: Update a plant's information via their ID number<br/>
<br/>

**Logs | `logs.py`**<br/>
`url_prefix`: `/logs`
<br/>
`GET`       | `/all`: Fetch all logs<br/>
`GET`       | `/all/<int:id>`: Fetch all logs given a `plant_id`<br/>
`GET`       | `/<int:id>`: Fetch a single plant's log via their ID number<br/>
`POST`      | `/insert`: Add a log entry to the database<br/>
<br/>

**Configuration | `configuration.py`**<br/>
**NOTE: Email requires the forward slash at the end of the decorator**<br/>
`url_prefix`: `/config`
<br>
`GET`       | `/<string:user_email>/`: Fetch the user's configuration for initial setup<br/>
<br/>

**Requests | `make_requests.py`**<br/>
`url_prefix`: `/requests`
<br/>

`POST`      | `/insert`: Add a request to the database with a valid category, including 'water', 'light', or 'picture'<br/>
`GET`       | `/<int:id>`: Fetch the latest request made by a user with plant_id<br/>
`GET`       | `/all/<int:id>/<string:time>`: Fetch the latest requests made by a user with plant_id after given timestamp; PLEASE SEE ABOVE FOR FORMATTING DATE TIME IN **NOTES**<br/>

**Alert | `alert.py`**<br/>
`url_prefix`: `/alert`

`GET`       | `/<int:id>/water`: Send email notification to user that water tank level is low
`GET`       | `/<int:id>/new`: Send email notification to user that a new plant has been added 

### DEPLOYMENT
**05/04/2020 - Deployed using AWS Elastic Beanstalk**<br/>
**URL: http://backend-dev222222.us-east-1.elasticbeanstalk.com/**
- [Ref](https://medium.com/@rodkey/deploying-a-flask-application-on-aws-a72daba6bb80)

- Deployed using the following resources (Note: configure beforehand):
    - AWS Elastic Beanstalk
    - AWS RDS MySQL
    - AWS IAM User Policies

- For Flask app, we are using Elastic Beanstalk for deployment
- Set up an IAM user and grant it AdministratorAccess
- In your Flask app root directory (`/backend` for us), source your Python environment
- Install AWS EB using: `pip install awscli`
- Initiate your application to verify credentials using: `eb init`
- Configure settings and step through instructions
- Initiate your application for deployment using: `eb create`
    - NOTE: Abiding by Elastic Beanstalk's requirements, your Flask app MUST BE named `application` INSTEAD of `app`
    - Ex: `app = Flask(__name__)` should be `application = Flask(__name__)`
    - Rename your file to `application.py` if possible as well
    - You can always configure this by typing into the terminal, `eb config` and look for `WSGIPath` 
    - Resolves "Your WSGIPath refers to a file that does not exist"
- Update your code using `eb deploy`    