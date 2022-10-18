from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests


class MyBot:
    def __init__(self):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument(f'user-agent={user_agent}')
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--allow-running-insecure-content')
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--proxy-server='direct://'")
        self.options.add_argument("--proxy-bypass-list=*")
        self.options.add_argument("--start-maximized")
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--log-level=3')

        self.driver = webdriver.Chrome(
            options=self.options)

        # åbner tiktok.com
        self.driver.get("https://tiktok.com")

        # finder den første video i feed og klikker
        searchButton = self.driver.find_element(
            By.XPATH, '//*[@id="app"]/div[2]/div[2]/div[1]/div[1]/div/div[2]/div[1]')
        searchButton.click()

        time.sleep(3)

        counter = 0

        main = []
        final = []

        # tjekker om "næste video knappen" findes
        while counter < 10 and self.driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[1]/button[3]').is_displayed() == True:

            # får link til video
            linkBox = self.driver.find_element(
                By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/p').get_attribute("innerHTML")

            # før antal likes
            likes = self.driver.find_element(
                By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/button[1]/strong').get_attribute("innerHTML")

            counter += 1

            # likes str til float
            if likes[-1] == 'K' or likes[-1] == 'M':
                if likes[-1] == 'K':
                    likes = likes.rstrip(likes[-1])
                    likes = float(likes)
                    likes *= 1000
                else:
                    likes = likes.rstrip(likes[-1])
                    likes = float(likes)
                    likes *= 1000000
            else:
                likes = float(likes)

            post = [counter, likes, linkBox]

            main.append(post)

            # næste video
            self.driver.find_element(
                By.XPATH, '//*[@id="app"]/div[2]/div[3]/div[1]/button[3]').click()

            time.sleep(0.5)

        # sorterer array efter flest likes
        main.sort(key=lambda x: x[1])

        # nyt array med top 4
        final.append(main[-1])
        final.append(main[-2])
        final.append(main[-3])
        final.append(main[-4])

        newC = 0

        # går igennem top 4 og downloader med hvert link
        for i in final:
            print(i[2])

            newC += 1

            fileName = str(newC) + '.mp4'

            # åbner snaptik.com
            self.driver.get("https://snaptik.app/en")

            # finder searchBox
            searchBox = self.driver.find_element(By.XPATH, '//*[@id="url"]')

            tikLink = i[2]

            # kopier link til searchBox
            searchBox.send_keys(tikLink)

            # laver download
            searchButton = self.driver.find_element(
                By.XPATH, '//*[@id="submiturl"]')
            searchButton.click()

            time.sleep(3)

            # finder download
            elems = self.driver.find_element(
                By.XPATH, '//*[@id="download-block"]/div/a[1]')

            # download
            link = elems.get_attribute('href')
            self.driver.get(link)

            # gemmer download som video i samme mappe
            response = requests.get(link)
            with open(fileName, "wb") as out_file:
                out_file.write(response.content)


MyBot()
