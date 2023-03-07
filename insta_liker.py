from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class TwitterBot(object):

	def __init__(self):
		self.bot = webdriver.Chrome(executable_path='C:/Users/Ayush/Desktop/Automation/chromedriver.exe')

	def login(self, username, password):
		bot = self.bot
		self.username = username
		self.password = password
		bot.get('https://www.instagram.com/accounts/login')
		bot.implicitly_wait(8)
		email = bot.find_element_by_name('username')
		password = bot.find_element_by_name('password')
		email.clear()
		password.clear()

		email.send_keys(self.username)
		password.send_keys(self.password)

		password.send_keys(Keys.RETURN)
		time.sleep(10)

	def auto_follow(self):
		bot = self.bot
		user_name = input('Enter username : ')
		bot.get('https://www.instagram.com/{}'.format(user_name))
		bot.implicitly_wait(2)

		n_posts = len(bot.find_elements_by_class_name('_9AhH0'))
		
		for i in range(n_posts):
			bot.execute_script('var posts = document.getElementsByClassName("_9AhH0"); posts[{}].click()'.format(i))
			time.sleep(3)
			bot.execute_script('document.getElementsByClassName("glyphsSpriteHeart__outline__24__grey_9")[0].click()')
			time.sleep(2)
			# bot.execute_script('document.getElementsByClassName("glyphsSpriteHeart__filled__24__red_5")[0].click()')
			# time.sleep(2)
		

Bot = TwitterBot()

Bot.login(username, password )
Bot.auto_follow()