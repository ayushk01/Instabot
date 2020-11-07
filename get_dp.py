from instabot import InstaBot

bot = InstaBot(driver_path='chromedriver.exe')

while True:
    username = input("Enter username : ")
    dp_url = bot.getDpURL(username)
    if dp_url != 'err':
        bot.download_img(dp_url, username+'.jpg')
