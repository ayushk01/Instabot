from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import shutil
import time
import os

chrome_options = Options()
chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
chrome_options.add_argument("--headless")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920x1080')


class InstaBot:
    def __init__(self, driver_path):
        self.bot = webdriver.Chrome(
            executable_path=driver_path, chrome_options=chrome_options)

    def log_to_file(self, msg, log):
        with open('logs.txt', 'a') as f:
            f.write('\n\n')
            f.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            f.write('\n')
            f.write(msg)
            f.write('\n')
            f.write(log)

    def login(self, username, password):
        bot = self.bot
        print('[*] Opening Instagram...')
        bot.get('https://www.instagram.com/')
        bot.implicitly_wait(3)

        print('[*] Typing username and password...')
        username_field = bot.find_element_by_name('username')
        password_field = bot.find_element_by_name('password')

        print('[*] Logging in...')
        username_field.send_keys(username)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
        bot.implicitly_wait(5)
        print('[+] Generating a screenshot login.png...')
        time.sleep(5)
        # bot.get_screenshot_as_file('login.png')

    def follow_back_likers(self, post):
        bot = self.bot
        print('[*] Navigating to Post...')
        bot.get(post)
        bot.implicitly_wait(3)
        time.sleep(2)

        print('[*] Getting Likers...')
        try:
            bot.find_element_by_xpath(
                '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button').click()
            bot.implicitly_wait(4)
            print('Generating a screenshot likers.png...')
            time.sleep(4)
            # bot.get_screenshot_as_file('likers.png')
        except Exception as e:
            self.log_to_file('[!] Error getting likers list', str(e))
            print('[!] Error getting likers list. Will try again in 10 mins.')
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
                self.log_to_file(
                    '[!] Either list is complete or Some error occured', str(e))
                print(
                    '[!] Either list is complete or Some error occured. Will try again in 10 mins')
                break

            try:
                follow_btn = bot.find_element_by_xpath(
                    '/html/body/div[4]/div/div/div[2]/div/div/div[{}]/div[3]/button'.format(count))
            except:
                print(
                    '[!] Error getting following button. You might also liked the post ;)')
                count += 1
                continue

            isFollowing = follow_btn.get_attribute('innerText') == 'Following'
            # print(' [*] {}. {}'.format(count+16*(scroll-1), liker_name))
            if (not isFollowing):
                self.log_to_file('[+] Following :', liker_name)
                print(' [*] Following {}'.format(liker_name))
                # follow_btn.click()
                time.sleep(2)
            count += 1

            if (count == 16):
                print(' [*] Scrolling up')
                bot.execute_script("arguments[0].scrollTop = {}".format(
                    scroll*960), likers_window)
                count = 1
                scroll += 1
                time.sleep(2)

    def download_img(self, img_url, img_name):
        if img_url == '':
            print('[!] Invalid image URL. Please try again')
            return

        r = requests.get(img_url, stream=True)
        if r.status_code == 200:
            with open('Downloads/'+img_name, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
            print('[+] {} downloaded successfully'.format(img_name))
        else:
            print('[!] Error downloading {}'.format(img_url))

    def getDpURL(self, username):
        bot = self.bot
        bot.get(
            'https://www.instadp.com/fullsize/{}'.format(username))
        res = bot.page_source
        soup = BeautifulSoup(res, 'html.parser')

        try:
            dp = soup.find_all('img', {'class': 'picture'})[0]
        except:
            print(
                '[!] Could not find user profile. Please make sure username is correct')
            return 'err'
        dp_url = dp['src']

        return dp_url
