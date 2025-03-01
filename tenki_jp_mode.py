from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import logging
from selenium.webdriver.support.ui import WebDriverWait


class TenkiJpMode:
    def __init__(self):
        pass

    def execute(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        CHROMEDRIVER_PATH = "/opt/homebrew/bin/chromedriver"
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100"

        options = webdriver.ChromeOptions()
        options.add_argument("--user-agent={user_agent}".format(user_agent=USER_AGENT))
        options.add_argument("--incognito")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-dev-shm-usage")

        # options.add_argument("--headless")
        # options.add_argument("--no-sandbox")
        service = Service(CHROMEDRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        URL = "https://tenki.jp/forecast/3/16/4410/13112/"

        try:
            driver.get(URL)
            element = driver.find_element(
                By.XPATH,
                '//*[@id="main-column"]/section/div[3]',
            )
            png_bytes = element.screenshot_as_png

            with open("screenshot.png", "wb") as f:
                f.write(png_bytes)

        finally:
            driver.quit()
