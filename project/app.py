# ------------------------- CONFIGURE ENVIRONMENT ------------------------- #

import flask
from flask import request, jsonify, render_template, send_from_directory

import requests
from bs4 import BeautifulSoup
from lxml import html
from urllib.request import Request, urlopen
import urllib.request
import urllib.parse
import urllib.error
import ssl
import ast
import os

import json

from pathlib import Path
profiles_path = Path('profiles/')

from src.scraping import *


# ------------------------------- FLASK API ------------------------------- #

app = flask.Flask(__name__);
app.config["DEBUG"] = True;

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/docs', methods=['GET'])
def docs():
    return render_template('docs.html')


# ---------------------------------- V0.0 ---------------------------------- #

@app.route('/api/v0.0/create', methods=['GET'], defaults={'ticker': "AAPL"})
def create( ticker = "AAPL" ):
    """
    Scrapes the information from finance.yahoo and updates the JSON
    stock profile or creates the profile if it did not already exist
    in the database.
    """

    # Pass ticker arg locally
    if 'ticker' in request.args:
        ticker = request.args['ticker']

    # Form finance.yahoo query
    query = form_query(ticker)

    # Call for profile
    webpage = request_webpage(query)
    profile = parse_webpage(webpage)

    # Export profile as JSON
    export_profile(profiles_path, profile, ticker)

    # # Return query results
    return jsonify(profile)


@app.route('/api/v0.0/update', methods=['GET'], defaults={'ticker': "AAPL"})
def update(ticker):
    """
    Creating and updating a profile are ultimately the same function as
    they both overwrite the existing profile or create it if it does
    not exist. For this reason, update calls just function-forward to
    the create call.
    """

    # Pass ticker arg locally
    if 'ticker' in request.args:
        ticker = request.args['ticker']

    # Form finance.yahoo query
    query = form_query(ticker)

    # Call for profile
    webpage = request_webpage(query)
    profile = parse_webpage(webpage)

    # Export profile as JSON
    export_profile(profiles_path, profile, ticker)

    # # Return query results
    return "{} Profile Updated Successfully.".format(ticker)


@app.route('/api/v0.0/get', methods=['GET'], defaults={'ticker': "AAPL"})
def get(ticker):
    """
    This function finds the profile within the database and loads the
    function as a JSON. In verbose mode, this function will also
    return the dictionary version of the JSON file. In normal mode
    it returns the JSON string itself, assuming an API application.
    """

    # Pass ticker arg locally
    if 'ticker' in request.args:
        ticker = request.args['ticker']

    # Get stock profile
    return import_profile(profiles_path, ticker)


# ---------------------------------- MAIN ---------------------------------- #

if __name__ == '__main__':
    app.run()
