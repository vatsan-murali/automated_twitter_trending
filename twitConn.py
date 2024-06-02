from dotenv import load_dotenv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pymongo import MongoClient
from datetime import datetime
import uuid
import requests

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.twitter_trends  
collection = db.trends

def fetch_twitter_trends():
    proxy = Proxy({
        'proxyType': ProxyType.PAC,
        'proxyAutoconfigUrl': './us-ca.pac'
    })

    chrome_options = Options()
    chrome_options.add_argument('--proxy-server=%s' % proxy.http_proxy)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://twitter.com/i/flow/login")

    username = os.getenv('TWITTER_USERNAME')
    password = os.getenv('TWITTER_PASSWORD')

    time.sleep(7)
    driver.find_element(By.XPATH, "//input").send_keys(username + Keys.RETURN)

    time.sleep(7)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password + Keys.RETURN)
    time.sleep(10)

    response = requests.get('https://api.ipify.org')
    ip_address = response.text

    trending_topics = driver.find_elements(By.XPATH, "//div[@aria-label='Timeline: Trending now']//span")
    top_trends = [trend.text for trend in trending_topics]
    trends = []
    i = 0
    while i < len(top_trends) - 1:
        if "Trending" in top_trends[i]:
            i += 1
            trends.append(top_trends[i])
        i += 1
    if len(trends) < 5:
        trends.append("No trending topics found")

    unique_id = str(uuid.uuid4())
    data = {
        "_id": unique_id,
        "nameoftrend1": trends[0],
        "nameoftrend2": trends[1],
        "nameoftrend3": trends[2],
        "nameoftrend4": trends[3],
        "nameoftrend5": trends[4],
        "datetime": datetime.now(),
        "ip_address": ip_address
    }
    collection.insert_one(data)

    driver.quit()

    return data
