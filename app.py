# Flask: A micro web framework for Python used to build web applications.
# jsonify: A utility function from Flask used to serialize data to JSON format
from flask import Flask, jsonify
# A Python library used for web scraping to extract data from HTML and XML documents.
from bs4 import BeautifulSoup
# A Python library used for making HTTP requests.
import requests
# Connecting to MongoDB
from pymongo import MongoClient
# A module used to load environment variables from a .env file.
from dotenv import load_dotenv
import os
# To schedule the scraper
import schedule
import time


# Load the environment variables from .env file
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.test
usd_lbp_collection = db.usd_lbp

app = Flask(__name__)

@app.route('/')
def scrape_lira_rate():
    # A proxy, since this website may not be available in your country.
    # proxy = {'https': 'https://195.246.120.139:8443/'}

    # Scraper setup
    url = 'https://lirarate.org'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the buy value of the Lira
    buy_value = soup.find('div', {'class': 'wp-block-column'}).text.strip()
    # Extract the sell value of the Lira
    sell_value = soup.find_all('div', {'class': 'wp-block-column'})[1].text.strip()

    print(buy_value, sell_value)

    # Return a message indicating status

    if buy_value and sell_value:
        usd_lbp_collection.insert_one({
            'buy_value': buy_value,
            'sell_value': sell_value
        })
        return jsonify({'message': 'Scraped and stored the Lira rate successfully'})
    else:
        return jsonify({'message': 'Error: could not scrape the Lira rate'})

def schedule_job():
    schedule.every(1).minutes.do(scrape_lira_rate)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Starting the scheduler
    schedule_job()

    # Starting the Flask app
    app.run(debug=True)


# <p class="has-text-align-center inherit-font" id="latest-buy"><strong id="buy-value" data-value="97500">Buy</strong> 1 USD at 97,500 LBP</p>
# PIA VPN Ports:
#   tcp port: 8443, 853, 443, 80
#   VPN IP: 195.246.120.139