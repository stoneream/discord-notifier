from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
from discord_webhook_client import DiscordWebHookClient
from selenium.webdriver.support import expected_conditions as EC
import time

class TenkiJpMode:
    def __init__(
        self,
        chromedriver_path: str,
        dry_run: bool,
        discord_webhook_url: str,
    ):
        self.chromedriver_path = chromedriver_path
        self.dry_run = dry_run

        CHROMEDRIVER_PATH = self.chromedriver_path
        options = webdriver.ChromeOptions()
        options.add_argument("--incognito")
        options.add_argument("--hide-scrollbars")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")
        options.add_argument("--window-size=2560,1440")

        service = Service(CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=options)

        self.discrod_webhook_client = DiscordWebHookClient(
            webhook_url=discord_webhook_url
        )

        self.screenshot_path = "screenshot.png"

        pass

    def execute(self):
        urls = []

        with open("tenki-jp-urls.txt", "r") as f:
            for line in f:
                if line.strip() != "":
                    urls.append(line)

        try:
            for url in urls:
                self.screenshot(url)

                if self.dry_run:
                    print("Dry run mode, skip sending discord")
                else:
                    self.send_discord(url)
        finally:
            self.driver.quit()

    def is_element_position_stable(self, element_xpath: str) -> bool:
        # 要素の位置が1秒後に変化していないか確認
        element = self.driver.find_element(By.XPATH, element_xpath)
        rect1 = element.rect
        time.sleep(1)
        rect2 = element.rect
        return rect1 == rect2
    
    def wait_for_element_stable(self, element_xpath: str):
        # 要素の位置が安定するまで待機し、安定したあとに要素を返す
        timeout = 30
        wait = WebDriverWait(self.driver, timeout)
        # 要素がDOM上に存在するまで待機する
        wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))

        # 座標・サイズが変化しなくなるまでループ
        end_time = time.time() + timeout
        while time.time() < end_time:
            if self.is_element_position_stable(element_xpath):
                return self.driver.find_element(By.XPATH, element_xpath)
        raise TimeoutError("Element '{element_xpath}' is not stable".format(element_xpath=element_xpath))

    def screenshot(self, url: str):
        print("Start capturing screenshot:", url)

        self.driver.get(url)

        # すべての要素が読み込まれるまで待機
        WebDriverWait(self.driver, 15).until(EC.presence_of_all_elements_located)

        # 始点のエレメント (市区町村名)
        start_element_xpath = '//*[@id="main-column"]/section/h2'
        stable_start_element = self.wait_for_element_stable(start_element_xpath)
        # 終点のエレメント
        end_element_xpath = '//*[@id="start-stop-box"]'
        stable_end_element = self.wait_for_element_stable(end_element_xpath)
        # それぞれの要素が対角になるように領域を指定
        start_xy = stable_start_element.location
        end_xy = stable_end_element.location
        left = start_xy["x"]
        top = start_xy["y"]
        right = end_xy["x"] + stable_end_element.size["width"]
        bottom = end_xy["y"] + stable_end_element.size["height"]

        # スクリーンショットを撮影し、切り取り処理
        self.driver.save_screenshot(self.screenshot_path)
        image = Image.open(self.screenshot_path)
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image.save(self.screenshot_path)

        print("Finish capturing screenshot, url:", url)

    def send_discord(self, url: str):
        # content = "from {url}".format(url=url)
        content = ""
        self.discrod_webhook_client.send_message(
            content=content,
            username="お天気情報",
            image_filepath=self.screenshot_path,
        )
