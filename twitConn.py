from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--proxy-server=%s' % proxy.http_proxy)

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://twitter.com/i/flow/login")

        username = os.getenv('TWITTER_USERNAME')
        password = os.getenv('TWITTER_PASSWORD')

        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
        ).send_keys(username + Keys.RETURN)

        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        ).send_keys(password + Keys.RETURN)

        trending_topics = WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']//span"))
        )

        top_trends = [trend.text for trend in trending_topics]
        print(f"Top trends: {top_trends}")

        trends = []
        i = 0
        while i < len(top_trends) - 1:
            if "Trending" in top_trends[i]:
                i += 1
                trends.append(top_trends[i])
            i += 1

        if len(trends) < 5:
            trends += ["No trending topics found"] * (5 - len(trends))

        unique_id = str(uuid.uuid4())
        data = {
            "_id": unique_id,
            "nameoftrend1": trends[0] if len(trends) > 0 else "No trending topics found",
            "nameoftrend2": trends[1] if len(trends) > 1 else "No trending topics found",
            "nameoftrend3": trends[2] if len(trends) > 2 else "No trending topics found",
            "nameoftrend4": trends[3] if len(trends) > 3 else "No trending topics found",
            "nameoftrend5": trends[4] if len(trends) > 4 else "No trending topics found",
            "datetime": datetime.now(),
            "ip_address": requests.get('https://api.ipify.org').text
        }
        collection.insert_one(data)

        return data
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    data = fetch_twitter_trends()
