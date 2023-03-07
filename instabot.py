from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import requests
import shutil
import time
import os

# Wait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from logger import Logger

chrome_options = Options()
# chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
# chrome_options.add_argument("--headless")
# chrome_options.add_argument('--disable-dev-shm-usage')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--window-size=1920x1080')


class InstaBot:
    def __init__(self):
        self.bot = webdriver.Chrome(
            executable_path='chromedriver.exe', chrome_options=chrome_options)
        self.logger = Logger()
        self.username = ''
        self.password = ''

    def login(self, username, password):
        bot = self.bot
        logger = self.logger
        self.username = username
        self.password = password

        logger.info('Opening Instagram...')
        bot.get('https://www.instagram.com/')
        bot.implicitly_wait(3)

        logger.info('Typing username and password...')
        username_field = bot.find_element_by_name('username')
        password_field = bot.find_element_by_name('password')

        logger.info('Logging in...')
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        bot.implicitly_wait(5)

        try:

            WebDriverWait(bot, 5).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[1]/section/main/div/div')))
            logger.info('Save Info Btn Available')

            all_btns = bot.find_elements_by_tag_name('button')
            save_info_btn = list(
                filter(lambda x: x.get_attribute('innerText') == 'Save Info', all_btns))[0]
            save_info_btn.click()
            bot.implicitly_wait(3)

            not_now_btn = WebDriverWait(bot, 5).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[4]/div/div/div/div[3]/button[2]')))
            logger.info('Not now button found')

            all_btns = bot.find_elements_by_tag_name('button')
            now_now_btn = list(
                filter(lambda x: x.get_attribute('innerText') == 'Not Now', all_btns))[0]
            now_now_btn.click()
            bot.implicitly_wait(3)

        except TimeoutException:
            logger.error("Timeout occured while waiting in login function")
            exit(1)

    def change_bio(self, newBio):
        bot = self.bot
        logger = self.logger
        username = self.username
        password = self.password

        try:
            bot.get(url='https://www.instagram.com/accounts/edit/')
            WebDriverWait(bot, 8).until(EC.presence_of_element_located(
                (By.ID, 'pepBio')))
            logger.info('Bio Text Field Available')
            bio_text_field = bot.find_element_by_id('pepBio')
            bio_text_field.clear()
            bio_text_field.send_keys(newBio)

            all_btns = bot.find_elements_by_tag_name('button')
            submit_btn = list(
                filter(lambda x: x.get_attribute('innerText') == 'Submit', all_btns))[0]

            submit_btn.click()
        except TimeoutException:
            logger.error("Timeout occured while waiting for bio text field")

        bot.get('https://www.instagram.com/{}/'.format(username))

    def follow_back_likers(self, post):
        bot = self.bot
        logger = self.logger

        logger.info('Navigating to Post...')
        bot.get(post)
        bot.implicitly_wait(3)
        time.sleep(2)

        logger.info('Getting Likers...')
        try:
            bot.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button').click()
            bot.implicitly_wait(4)
            logger.info('Generating a screenshot likers.png...')
            time.sleep(4)
            # bot.get_screenshot_as_file('likers.png')
        except Exception as e:
            logger.log_to_file('Error getting likers list', str(e))
            logger.error(
                'Error getting likers list. Will try again in 10 mins.')
            return
        likers_window = bot.find_element_by_xpath(
            '/html/body/div[4]/div/div/div[2]/div')
        bot.execute_script(
            "arguments[0].scrollTop = {}".format(300), likers_window)

        count = 1   # 1 to 16 i.e. max of likers that could fix once on screen
        scroll = 1  # counts no of scroll
        while True:

            try:
                liker_name = bot.find_element_by_xpath(
                    '/html/body/div[4]/div/div/div[2]/div/div/div[{}]/div[2]/div[1]/div/span/a'.format(count)).get_attribute('innerText')
            except Exception as e:
                logger.log_to_file(
                    '[!] Either list is complete or Some error occured', str(e))
                logger.error(
                    'Either list is complete or Some error occured. Will try again in 10 mins')
                break

            try:
                follow_btn = bot.find_element_by_xpath(
                    '/html/body/div[4]/div/div/div[2]/div/div/div[{}]/div[3]/button'.format(count))
            except:
                logger.error(
                    'Error getting following button. You might also liked the post ;)')
                count += 1
                continue

            isFollowing = follow_btn.get_attribute('innerText') == 'Following'
            # print(' {}. {}'.format(count+16*(scroll-1), liker_name))
            if (not isFollowing):
                self.log_to_file('[+] Following :', liker_name)
                logger.info('Following {}'.format(liker_name))
                # follow_btn.click()
                time.sleep(2)
            count += 1

            if (count == 16):
                logger.info('Scrolling up')
                bot.execute_script("arguments[0].scrollTop = {}".format(
                    scroll*960), likers_window)
                count = 1
                scroll += 1
                time.sleep(2)

    def download_img(self, img_url, img_name):
        logger = self.logger

        if img_url == '':
            logger.error('Invalid image URL. Please try again')
            return

        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open('Downloads/'+img_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            logger.success('{} downloaded successfully'.format(img_name))
        else:
            logger.error('Error downloading {}'.format(img_url))

    def getDpURL(self, username):
        bot = self.bot
        logger = self.logger

        bot.get(
            'https://www.instadp.com/fullsize/{}'.format(username))
        res = bot.page_source
        soup = BeautifulSoup(res, 'html.parser')

        try:
            dp = soup.find_all('img', {'class': 'picture'})[0]
        except:
            logger.error(
                'Could not find user profile. Please make sure username is correct')
            return 'err'
        dp_url = dp['src']

        return dp_url
