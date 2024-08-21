from datetime import datetime, timedelta
import time
import schedule
from constants.crawler_url import ZHUBEI_GOLF_STORE_URL, ZHUBEI_HSR_GOLF_STORE_URL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from golfstoreDb import GolfStoreDb, GolfStoreInfo

URL = "http://selenium-chrome:4444/wd/hub"

# URL = "http://127.0.0.1:4444/wd/hub"



db_session = GolfStoreDb()

def check_latest_golfstore_info():

    now = datetime.now()
    now_at_hour_level = now.replace(minute=0, second=0, microsecond=0)

    today6am = now.replace(hour=6, minute=0, second=0, microsecond=0)

    tomorrow0am = (now + timedelta(days=1)).replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    try:
        if today6am <= now_at_hour_level and now_at_hour_level <= tomorrow0am:
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            print(f"start at: {formatted_now}--------")

            # browser = webdriver.Chrome()

            golf_store_urls = [ZHUBEI_GOLF_STORE_URL,
                               ZHUBEI_HSR_GOLF_STORE_URL]
            result = []

            for golf_store_url in golf_store_urls:
                golf_store = {}
                print(f"\n--------")
                time.sleep(15)

                options = webdriver.ChromeOptions()
                options.add_argument('--ignore-ssl-errors=yes')
                options.add_argument('--ignore-certificate-errors')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--no-sandbox')
                options.add_argument('--headless')
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-extensions")
                options.add_argument("--window-size=1920x1080")

                browser = webdriver.Remote(
                    command_executor=URL,
                    options=options
                )

                browser.implicitly_wait(5)  # seconds

                browser.get(golf_store_url)
                wait = WebDriverWait(browser, timeout=20)
                revealed = browser.find_element(By.ID, "app")
                wait.until(lambda d: revealed.is_displayed())

                golf_store_data = get_golf_data(browser)
                golf_store["data"] = golf_store_data
                golf_store["url"] = golf_store_url

                result.append(golf_store)
                print(f"--------\n")
            browser.quit()

            # insert result to db
            print(result)
            
            db = next(db_session.get_db())
            entities=[]
            for item in result:
                 golf_store_entity = GolfStoreInfo(url=item['url'], data=item['data'])
                 entities.append(golf_store_entity)
            db.add_all(entities)
            db.commit()
            print(f"end--------\n")
    except Exception as e:
        print(e)
        pass


def get_golf_data(browser):

    print(f"store name: {browser.title}")

    golfstore = {"store_name": browser.title, "reserved_dates": []}

    calendar = browser.find_element(By.CLASS_NAME, "calendar-detail")

    reserved_days = browser.find_elements(By.CLASS_NAME, "show-bar")

    for reserved_day in reserved_days:
        reserved_date = get_timespans(calendar, reserved_day)
        golfstore["reserved_dates"].append(reserved_date)

    return golfstore


def get_timespans(calendar, reserved_day):

    try:
        reserved_day.click()
    except Exception as e:
        pass

    calender_header = calendar.find_element(By.CLASS_NAME, "calender-header")
    reserved_header = calendar.find_element(By.CLASS_NAME, "block")
    print(f"\n{calender_header.text}:{reserved_header.text}")

    reserved_date = {"date": calender_header.text, "timespan": []}

    reserved_timespans = calendar.find_elements(By.CLASS_NAME, "truncate")
    for reserved_timespan in reserved_timespans:
        reserved_date["timespan"].append(reserved_timespan.text)
        print(f"{reserved_timespan.text}")

    return reserved_date


formatted_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(f"start web crawler job at {formatted_now}\n")

check_latest_golfstore_info()

# schedule.every().hours.at("20:00").do(check_latest_golfstore_info)
# schedule.every().hours.at("50:00").do(check_latest_golfstore_info)


while True:
    schedule.run_pending()
    time.sleep(1)

input("Press Enter to continue...")
