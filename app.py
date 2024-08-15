from datetime import datetime
import time
import schedule
from constants.crawler_url import ZHUBEI_GOLF_STORE_URL, OTHER_GOLF_STORE_URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



def check_latest_golfstore_info():
    formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"start at: {formatted_now}--------")
    get_golf_data(ZHUBEI_GOLF_STORE_URL)
    print(f"end--------\n")

    # get_golf_data(OTHER_GOLF_STORE_URL)


def get_golf_data(url):
    browser = webdriver.Chrome()
    browser.get(url)
    reserved_days = browser.find_elements(By.CLASS_NAME, 'show-bar')
    for reserved_day in reserved_days:
        try:
            reserved_day.click()

            calendar = browser.find_element(By.CLASS_NAME, 'calendar-detail')
            calender_header = calendar.find_element(
                By.CLASS_NAME, 'calender-header')
            reserved_header = calendar.find_element(By.CLASS_NAME, 'block')
            print('\n')
            print(f'{calender_header.text}:{reserved_header.text}')
            print(reserved_header.text)

            reserved_timespans = calendar.find_elements(
                By.CLASS_NAME, 'truncate')
            for reserved_timespan in reserved_timespans:
                print(f'{reserved_timespan.text}')

        except Exception as e:
            pass

    browser.quit()


formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"start web crawler job at {formatted_now}\n")

schedule.every().day.at("09:00:00", "Asia/Taipei").do(check_latest_golfstore_info)
schedule.every().day.at("12:00:00", "Asia/Singapore").do(check_latest_golfstore_info)
schedule.every().day.at("15:00:00", "Asia/Singapore").do(check_latest_golfstore_info)
schedule.every().day.at("18:00:00", "Asia/Singapore").do(check_latest_golfstore_info)
schedule.every().day.at("23:31:00", "Asia/Singapore").do(check_latest_golfstore_info)

while True:
    schedule.run_pending()
    time.sleep(1)
