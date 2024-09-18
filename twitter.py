from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os

PROMISED_UP = 50
PROMISED_DOWN = 35
USERNAME = os.environ.get("USERNAME")
PASSWORD = os.environ.get("PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self):
        self.upload = PROMISED_UP
        self.download = PROMISED_DOWN
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get("https://www.speedtest.net")
            time.sleep(5)

            try:
                continue_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                continue_button.click()
            except Exception as e:
                print(f"No cookies button found: {e}")

            time.sleep(5)
            go_button = driver.find_element(By.CLASS_NAME, "start-text")
            go_button.click()

            time.sleep(70)  # Wait for speed test to complete

            download_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div[2]/span')
            self.down = float(download_speed.text)

            upload_speed = driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/span')
            self.up = float(upload_speed.text)

        except Exception as e:
            print(f"Error in get_internet_speed: {e}")

        finally:
            driver.quit()

    def tweet_at_provider(self):
        if self.down < PROMISED_DOWN or self.up < PROMISED_UP:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option("detach", True)
            driver = webdriver.Chrome(options=chrome_options)

            try:
                driver.get("https://x.com/i/flow/login")

                time.sleep(5)

                username_field = driver.find_element(By.NAME, "text")
                username_field.send_keys(USERNAME)
                username_field.send_keys(Keys.RETURN)

                time.sleep(5)

                password_field = driver.find_element(By.NAME, "password")
                password_field.send_keys(PASSWORD)
                password_field.send_keys(Keys.RETURN)

                time.sleep(5)

                tweet_box = driver.find_element(By.CSS_SELECTOR, "div[aria-label='Tweet text']")
                tweet_box.click()
                tweet_box.send_keys(f"My ISP provider Excitel has failed to provide the promised upload speed of {self.upload} Mbps and download speed of {self.download} Mbps. Actual speeds: {self.up} Mbps upload, {self.down} Mbps download.")

                tweet_button = driver.find_element(By.XPATH, "//div[@data-testid='tweetButtonInline']")
                tweet_button.click()

                time.sleep(5)

            except Exception as e:
                print(f"Error in tweet_at_provider: {e}")

            finally:
                driver.quit()
