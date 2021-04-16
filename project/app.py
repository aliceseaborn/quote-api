# ------------------------- CONFIGURE ENVIRONMENT ------------------------- #

# Load API tools
import flask
from flask import request, jsonify, render_template, send_from_directory

# Libraries for scraping
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

# JSON Support
import json

# Configure paths
from pathlib import Path
data_path = Path('profiles/')

# Import engine
from src.scraping import *


# ------------------------- CREATE FLASK API ------------------------- #

# Instantiate the app
app = flask.Flask(__name__);
app.config["DEBUG"] = True;

# ---------- HOME PAGE ---------- #
@app.route('/', methods=['GET'])
def Home():
    return render_template('home.html')

# ---------- DOCS PAGE ---------- #
@app.route('/docs', methods=['GET'])
def Docs():
    return render_template('EngineDocumentation.html')

# ------------------------- CREATE PROFILE ------------------------- #
# Scrapes the information from finance.yahoo and updates the JSON
#   stock profile or creates the profile if it did not already exist
#   in the database.
#

# ---------- BETA V0 API ---------- #
@app.route('/api/versions/beta-v0', methods=['GET'], defaults={'ticker': "AAPL"})
def CreateProfile( ticker = "AAPL" ):
    
    # Pass ticker arg locally
    if 'ticker' in request.args:
        ticker = request.args['ticker']
    
    # Form finance.yahoo query
    query = FormQuery(ticker)

    # Call for profile
    profile = ParseHTML(query)

    # Export profile as JSON
    ExportJSON(profile, ticker)
    
    # Return query results
    return jsonify(profile)


# # ------------------------- UPDATE PROFILE ------------------------- #
# # Creating and updating a profile are ultimately the same function as
# #   they both overwrite the existing profile or create it if it does
# #   not exist. For this reason, update calls just function-forward to
# #   the create call.
# #

# def UpdateProfile(ticker):
#     CreateProfile(ticker)
    
    
# # ------------------------- GET PROFILE ------------------------- #
# # This function finds the profile within the database and loads the
# #   function as a JSON. In verbose mode, this function will also
# #   return the dictionary version of the JSON file. In normal mode
# #   it returns the JSON string itself, assuming an API application.
# #

# def GetProfile(ticker):
#     return ImportJSON(ticker)




# ------------------------- MAIN ------------------------- #
# Activates the API at init.
#

if __name__ == '__main__':
    app.run()
