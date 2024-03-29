# ------------------------- CONFIGURE ENVIRONMENT ------------------------- #

import flask
from flask import request, jsonify, render_template

from flask_flatpages import FlatPages, pygments_style_defs

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = ".md"
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite', 'tables', 'markdown_katex', 'footnotes']

from pathlib import Path
profiles_path = Path('profiles/')

from src.scraping import form_query, request_webpage, parse_webpage, export_profile, import_profile


# ------------------------------- FLASK API ------------------------------- #

app = flask.Flask(__name__);
app.config.from_object(__name__)
pages = FlatPages(app)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/docs')
def docs():
    return render_template('docs.html', pages=pages)

@app.route('/<path:path>')
def page(path):
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

@app.route('/pygments.css')
def pygments_css():
    return pygments_style_defs('tango'), 200, {'Content-Type': 'text/css'}


# ---------------------------------- V0.0 ---------------------------------- #

@app.route('/api/0/create', methods=['GET'], defaults={'ticker': "AAPL"})
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


@app.route('/api/0/update', methods=['GET'], defaults={'ticker': "AAPL"})
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
    return f"{ticker} Profile Updated Successfully."


@app.route('/api/0/get', methods=['GET'], defaults={'ticker': "AAPL"})
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
