# ------------------------- CONFIGURE ENVIRONMENT ------------------------- #

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


# ------------------------- FORM QUERY ------------------------- #

def form_query(ticker):
    """
    Takes a stock ticker as input and returns the full HTTP request
    for the yahoo finance query.
    """
    return f"https://finance.yahoo.com/quote/{ticker}"


# ------------------------- READ HTML ------------------------- #

def read_html(query):
    """
    Uses a query and returns the prettified HTML for reading.
    """
    response = requests.get(query)
    soup = BeautifulSoup(response.text, 'lxml')
    print(soup.prettify())


# ----------------------- REQUEST WEBPAGE ---------------------- #

def request_webpage(query):
    """
    Sends request against Yahoo Finance API using the provided
    query. Returns the raw webpage bytes.
    """

    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Making the website believe that you are accessing it using a Mozilla browser
    req = Request(query, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()

    return webpage


# ------------------------ PARSE WEBPAGE ------------------------ #

def parse_webpage(webpage):
    """
    Uses an HTML tree and searches for specific tags which house the
    stock information. This function utilizes try-catch methods
    for error handling of each data element. Returns empty for the
    missing values. The final return is a python dictionary.
    """

    # Creating a BeautifulSoup object of the HTML page for easy extraction of data.
    soup = BeautifulSoup(webpage, 'html.parser')
    html = soup.prettify('utf-8')
    profile = {}
    trading = {}
    fundamentals = {}
    
    # TRADING
    
    # Previous Close
    for td in soup.findAll('td', attrs={'data-test': 'PREV_CLOSE-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Previous Close'] = span.text.strip()
    
    # Open Value
    for td in soup.findAll('td', attrs={'data-test': 'OPEN-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Open'] = span.text.strip()

    # Present Value
    for span in soup.findAll('span', attrs={'class': 'Trsdu(0.3s) Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(b)'}):
        trading['Present Value'] = span.text.strip()
            
    # Bid
    for td in soup.findAll('td', attrs={'data-test': 'BID-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Bid'] = span.text.strip()

    # Ask
    for td in soup.findAll('td', attrs={'data-test': 'ASK-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Ask'] = span.text.strip()

    # Present Growth
    for div in soup.findAll('div', attrs={'class': 'D(ib) Va(t)'}):
        for span in div.findAll('span', recursive=False):
            profile['Present Growth'] = span.text.strip()

    # Day's Range
    for td in soup.findAll('td', attrs={'data-test': 'DAYS_RANGE-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Day Range'] = span.text.strip()

    # Fifty-two Week Range
    for td in soup.findAll('td', attrs={'data-test': 'FIFTY_TWO_WK_RANGE-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Fifty-Two Week Range'] = span.text.strip()

    # Trading Volume
    for td in soup.findAll('td', attrs={'data-test': 'TD_VOLUME-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Day Volume'] = span.text.strip()

    # Average 3M Volume
    for td in soup.findAll('td', attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'}):
        for span in td.findAll('span', recursive=False):
            trading['Average 3M Volume'] = span.text.strip()
            
    # FUNDAMENTALS

    # Market Capitalization
    for td in soup.findAll('td', attrs={'data-test': 'MARKET_CAP-value'}):
        for span in td.findAll('span', recursive=False):
            fundamentals['Market Capitalization'] = span.text.strip()

    # Beta 3Y
    for td in soup.findAll('td', attrs={'data-test': 'BETA_3Y-value'}):
        for span in td.findAll('span', recursive=False):
            fundamentals['Beta 3Y'] = span.text.strip()

    # PE Ratio
    for td in soup.findAll('td', attrs={'data-test': 'PE_RATIO-value'}):
        for span in td.findAll('span', recursive=False):
            fundamentals['PE Ratio'] = span.text.strip()

    # EPS Ratio
    for td in soup.findAll('td', attrs={'data-test': 'EPS_RATIO-value'}):
        for span in td.findAll('span', recursive=False):
            fundamentals['EPS Ratio'] = span.text.strip()

    # Earnings Date
    for td in soup.findAll('td', attrs={'data-test': 'EARNINGS_DATE-value'}):
        trading['Earnings Date'] = []
        for span in td.findAll('span', recursive=False):
            fundamentals['Earnings Date'] = span.text.strip()

    # Dividend and Yield
    for td in soup.findAll('td', attrs={'data-test': 'DIVIDEND_AND_YIELD-value'}):
        fundamentals['Dividend'] = td.text.strip().split()[0]
        fundamentals['Dividend Yield'] = td.text.strip().split()[1].translate({ord(i): None for i in '()%'})

    # Ex Dividend Date
    for td in soup.findAll('td', attrs={'data-test': 'EX_DIVIDEND_DATE-value'}):
        for span in td.findAll('span', recursive=False):
            fundamentals['Ex Dividend Rate'] = span.text.strip()

    # One Year Target Price
    for td in soup.findAll('td', attrs={'data-test': 'ONE_YEAR_TARGET_PRICE-value'}):
        for span in td.findAll('span', recursive=False):
            fundamentals['One Year Target Price'] = span.text.strip()

    # Other Details
    profile['Trading'] = trading
    profile['Fundamental'] = fundamentals
    
    # Return full profile
    return profile


# ----------------------- EXPORT PROFILE ----------------------- #

def export_profile(profiles_path, profile, ticker):
    """
    Exports a stock profile into the profiles folder as JSON.
    """
    file = profiles_path / f"{ticker}.json"
    with file.open("w") as fp:
        json.dump(profile, fp)


# ----------------------- IMPORT PROFILE ----------------------- #

def import_profile(profiles_path, ticker):
    """
    Imports a stock profile from the profiles folder.
    """
    file = profiles_path / f"{ticker}.json"
    raw = open(file).read()
    return json.loads(raw)
