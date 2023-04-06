# Flask: A micro web framework for Python used to build web applications.
# jsonify: A utility function from Flask used to serialize data to JSON format
from flask import Flask, jsonify

# A Python library used for web scraping to extract data from HTML and XML documents.
from bs4 import BeautifulSoup

# A Python library used for making HTTP requests.
import requests

# A Python library used for accessing Google Sheets API
import gspread

# A module for loading Google Cloud Platform (GCP) credentials, used for authenticating with Google APIs.
from google.oauth2.service_account import Credentials

# A module used to load environment variables from a .env file.
from dotenv import load_dotenv

# A module used to access operating system functionalities like environment variables
import os


# Load the environment variables from .env file
load_dotenv()

# Define the credentials for accessing the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds_dict = {
    "type": os.getenv("TYPE"),
    "project_id": os.getenv("PROJECT_ID"),
    "private_key_id": os.getenv("PRIVATE_KEY_ID"),
    "private_key": os.getenv("PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("CLIENT_EMAIL"),
    "client_id": os.getenv("CLIENT_ID"),
    "auth_uri": os.getenv("AUTH_URI"),
    "token_uri": os.getenv("TOKEN_URI"),
    "auth_provider_x509_cert_url": os.getenv("AUTH_PROVIDER_X509_CERT_URL"),
    "client_x509_cert_url": os.getenv("CLIENT_X509_CERT_URL")
}

creds = Credentials.from_service_account_info(info=creds_dict, scopes=scope)

client = gspread.authorize(creds)
spreadsheet = client.create('lira-rate-scraper')

sheet = client.open('lira-rate-scraper').sheet1

app = Flask(__name__)

@app.route('/')
def scrape_lira_rate():
    # A proxy, since this website may not be available in your country.
    # proxy = {'https': 'https://195.246.120.139:8443/'}

    # Scraper setup
    url = 'https://lirarate.org'
    response = requests.get(url)
    # uncomment only if using proxy:
    # response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the buy value of the Lira
    buy_value = soup.find('div', {'class': 'wp-block-column'}).text.strip()

    # Extract the sell value of the Lira
    sell_value = soup.find('div', {'class': 'wp-block-column'}).text.strip()

    # Store the scraped data in a Google Sheet
    row = [buy_value, sell_value]
    sheet.insert_row(row, 2)

    print(buy_value, sell_value)

    # Return a message indicating status

    if buy_value and sell_value:
        return jsonify({'message': 'Scraped and stored the Lira rate successfully'})
    else:
        return jsonify({'message': 'Error: could not scrape the Lira rate'})



if __name__ == '__main__':
    app.run(debug=True)




# <p class="has-text-align-center inherit-font" id="latest-buy"><strong id="buy-value" data-value="97500">Buy</strong> 1 USD at 97,500 LBP</p>
# PIA VPN Ports:
#   tcp port: 8443, 853, 443, 80
#   VPN IP: 195.246.120.139