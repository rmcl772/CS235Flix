# CS235Flix
NOTE: my pc has 4k screens so there is a possibility that things wont look the best on all screens (either too big or too small), what i made looked fine for me (https://ibb.co/g9CNyfy), hopefully it looks similar for you as well.

## Description
CS235Flix is a web application for browsing and reviewing movies. users can search for movies by Title, Year, Genre, Actor or Director. Upon viewing a movie's page, they will be able to see all the relevant information about that movie, as well as add it to their watchlist, or write a review about it, if logged in. When searching for movies, if only one movies is found given the constraints, the user will be taken directly to that movie's page, instead of a list with one movie. 

## Installation
#### Create a virtual environment and install required packages
```shell script
$ cd CS235Flix
$ py -3 -m venv venv
$ venv\scripts\activate
$ pip install -r requirements.txt
```

#### Then, in pycharm:

File > Settings... > Project: CS235Flix > Project Interpreter

Click on the gear next to the interpreter and click Add...

Select Existing environment

Click the ... button and navigate to CS235Flix/venv/Scripts/python.exe

Click ok

## Execution
While in the CS235Flix directory and with an activated venv (*venv/Scripts/activate*)
```shell script
$ flask run
```
#####Or in pycharm:
with wsgi.py open, press Alt+Shift+10 and select wsgi.py

## Config
Config variables are stored in CS235Flix/.env

These variables are:

`FLASK_APP` - Entry point of the flask application (should always be wsgi.py)

`FLASK_ENV` - The environment in which the app runs (either development or production)

`SECRET_KEY` - Encryption key for session data

`TESTING` - Set the application to testing mode if True

`WTF_CSRF_ENCRYPTION_KEY` - Encryption key for WTForms

`OMDB_KEY` - API key for OMDB

`REFRESH_OMDB_POSTERS` - Enable querying of the OMDB API on initialisation.


