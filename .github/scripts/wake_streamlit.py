# Opens the dashboard in a headless browser. If the app is asleep, clicks the wake-up button.
import os
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

URL = os.environ["STREAMLIT_URL"]
WAKE_BUTTON = "//button[contains(., 'get this app back up')]"

opts = Options()
for arg in ("--headless=new", "--no-sandbox", "--disable-dev-shm-usage", "--window-size=1280,900"):
    opts.add_argument(arg)
driver = webdriver.Chrome(options=opts)


def find_wake_button():
    # look on the page first, then inside any iframes
    try:
        return WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, WAKE_BUTTON)))
    except TimeoutException:
        pass
    for frame in driver.find_elements(By.TAG_NAME, "iframe"):
        driver.switch_to.frame(frame)
        found = driver.find_elements(By.XPATH, WAKE_BUTTON)
        if found:
            return found[0]
        driver.switch_to.default_content()
    return None


try:
    driver.get(URL)
    print("Opened", URL)
    button = find_wake_button()
    if button is None:
        print("Dashboard is awake - visit recorded.")
    else:
        button.click()
        print("Dashboard was asleep - clicked the wake-up button.")
        time.sleep(60)
finally:
    driver.quit()
