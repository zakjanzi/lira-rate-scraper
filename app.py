from flask import Flask, jsonify
from bs4 import BeautifulSoup
# A Python library used for web scraping to extract data from HTML and XML documents
import requests
# A Python library used for making HTTP requests
from pymongo import MongoClient
# Connecting to MongoDB
import re
# Regex is a built-in module in Python that provides support for regular expressions
from dotenv import load_dotenv
import os
import schedule
# A library to schedule the scraping task
import time



# Load the environment variables from .env file
load_dotenv()

# Initialize Mongo client and create a new collection within db
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.test
usd_lbp_collection = db.usd_lbp

app = Flask(__name__)

@app.route('/')
def scrape_lira_rate():
    # A proxy, since this website may not be available in your country
    # proxy = {'https': 'https://195.246.120.139:8443/'}

    # Scraper setup
    url = 'https://lirarate.org'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the buy value of the Lira
    buy_value = soup.find('div', {'class': 'wp-block-column'}).text.strip()
    # Extract the sell value of the Lira
    sell_value = soup.find_all('div', {'class': 'wp-block-column'})[1].text.strip()

    # Clean the scraped data (extract integers only from string)
    buy_value = re.findall(r'\d+,\d+', buy_value)[0]
    sell_value = re.findall(r'\d+,\d+', sell_value)[0]

    print(buy_value, sell_value)

    # Insert the data into the db
    if buy_value and sell_value:
        usd_lbp_collection.insert_one({
            'buy_value': buy_value,
            'sell_value': sell_value
        })

    # Return a message indicating status
        return jsonify({'message': 'Scraped and stored the Lira rate successfully'})
    else:
        return jsonify({'message': 'Error: could not scrape the Lira rate'})
    

def schedule_job():
    schedule.every(1).hour.do(scrape_lira_rate)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    # Starting the scheduler
    schedule_job()

    # Starting the Flask app
    app.run(debug=True)


# Notes:
# <p class="has-text-align-center inherit-font" id="latest-buy"><strong id="buy-value" data-value="97500">Buy</strong> 1 USD at 97,500 LBP</p>
# PIA VPN Ports:
#   tcp port: 8443, 853, 443, 80
#   VPN IP: 195.246.120.139