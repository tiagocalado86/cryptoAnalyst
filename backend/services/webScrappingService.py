from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import json
import shutil
import os
import time
from dotenv import load_dotenv


class WebScrappingService:

    @staticmethod
    def getNews(url):
        try:
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            driver = webdriver.Firefox(
                service=Service(GeckoDriverManager().install()),
                options=options
            )
            driver.get(url)

            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept')]"))
            )
            cookie_button.click()

            time.sleep(3)

            for _ in range(20):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                element = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='More stories']"))
                )
                element.click()

            soup = BeautifulSoup(driver.page_source, "html.parser")

            driver.quit()

            titles = soup.find_all("a", class_="font-title text-charcoal-600 uppercase")
            mainContent = soup.find_all("h2", class_="font-headline-xs font-normal")
            secondContent = soup.find_all("p", class_="font-body text-charcoal-600 mb-4")
            timePosted = soup.find_all("span", class_="font-metadata text-color-charcoal-600 uppercase")

            newsList = []
            for title, main, second, timePosted in zip(titles, mainContent, secondContent, timePosted):
                newsList.append({
                    "title": title.text.strip(),
                    "mainContent": main.text.strip(),
                    "secondContent": second.text.strip(),
                    "timePosted": timePosted.text.strip()
                })

            with open("cryptoNews.json", "w") as file:
                json.dump(newsList, file, indent=4)

            WebScrappingService.__moveJson()
        except Exception as e:
            print("An error occurred while fetching news:", e)


    @staticmethod
    def __moveJson():
        load_dotenv()
        try:
            shutil.move(os.getenv("SRC_FILE_PATH_NEWS"), os.getenv("DEST_FILE_PATH"))
        except:
            os.remove(os.getenv("DEST_FILE_PATH_REMOVE_NEWS"))
            shutil.move(os.getenv("SRC_FILE_PATH_NEWS"), os.getenv("DEST_FILE_PATH"))
