# Synthesis
## RESTful API 
## Last Updated: 04/04/2020
### Synthesis - The Automatic Garden
### Authors: Leo Au-Yeung, Stanley Lim, Daniel Mallia, Jayson Tan


This repository contains the code developed by the above authors in the 
Spring 2020 CSCI Capstone course under Professor Maryash at Hunter College, for 
the purpose of running an automated garden with a web interface. 

Please follow below instructions to set up a Python environment


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
1.  Clone or pull this repository, ```cd``` into the director, and create a virtual environment  
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


