from instabot import InstaBot
import time
import os
from creds import username, password

# bot = InstaBot(driver_path=os.environ.get('CHROMEDRIVER_PATH'))
# bot.login(os.environ.get('INSTA_USERNAME'), os.environ.get('INSTA_SECRET'))

# while True:
#     bot.follow_back_likers(
#         post=os.environ.get('INSTA_POST'))
#     time.sleep(600)

bot = InstaBot(driver_path='chromedriver.exe')
bot.login(username, password)

while True:
    bot.follow_back_likers(
        post='https://www.instagram.com/p/B6QZyM8nhEI1aGnFtHkhnipAXqRF3CbLdZ8gkc0/')
    time.sleep(600)
