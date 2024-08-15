from datetime import datetime
import time
from bs4 import BeautifulSoup
import requests
import schedule
from constants.crawler_url import ZHUBEI_GOLF_STORE_URL, OTHER_GOLF_STORE_URL
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def check_latest_golfstore_info():
    formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"now: {formatted_now}")
    # get_golf_data(GOLF_STORE_URL)
    get_golf_data(OTHER_GOLF_STORE_URL)


def get_golf_data(url):
    browser = webdriver.Chrome()
    browser.get(url)
    reserved_days = browser.find_elements(By.CLASS_NAME, 'show-bar')
    for reserved_day in reserved_days:
        reserved_day.click()
        calendar = browser.find_element(By.CLASS_NAME, 'calendar-detail')
        calender_header = calendar.find_element(By.CLASS_NAME, 'calender-header')
        reserved_header = calendar.find_element(By.CLASS_NAME, 'block')
        print(f'{calender_header.text}:{reserved_header.text}')
        print(reserved_header.text)

        reserved_timespans = calendar.find_elements(By.CLASS_NAME, 'truncate')
        for reserved_timespan in reserved_timespans:
            print(f'{reserved_timespan.text}')

    browser.quit()


def set_header_user_agent():
    user_agent = UserAgent()
    return user_agent.random


formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"start products web crawler job at {formatted_now}")

schedule.every(2).seconds.do(check_latest_golfstore_info)


while True:
    schedule.run_pending()
    time.sleep(1)
