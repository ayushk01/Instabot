import time
from instabot import InstaBot

username = "de.code07"
password = 'decodepass'

bot = InstaBot()

count = 0

bot.login(username, password)

while True:
    bot.change_bio('Times changed : {}'.format(count))
    count += 1
    time.sleep(1)
