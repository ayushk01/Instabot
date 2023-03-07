from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

class TwitterBot(object):
	"""docstring for TwitterBot"""
	def __init__(self):
		self.bot = webdriver.Chrome(executable_path='C:/Users/Ayush/Desktop/Automation/chromedriver.exe')

	def login(self, username, password):
		bot = self.bot
		self.username = username
		self.password = password
		bot.get('https://twitter.com/login')
		bot.implicitly_wait(6)
		email = bot.find_element_by_class_name('js-username-field')
		password = bot.find_element_by_class_name('js-password-field')
		email.clear()
		password.clear()

		email.send_keys(self.username)
		password.send_keys(self.password)

		password.send_keys(Keys.RETURN)
		bot.implicitly_wait(3)

	def find_tweet(self, hashtag):
		bot = self.bot
		bot.get('https://twitter.com/search?q=' + hashtag + '&src=typd')
		bot.implicitly_wait(5)
		for i in range(2):
			bot.execute_script('window.scrollTo(0, document.body.scrollHeight)')
			bot.implicitly_wait(2)
		soup = BeautifulSoup(bot.page_source, 'html.parser')
		tweets = [p.text for p in soup.findAll('p', class_ = 'tweet-text')]
		for tweet in tweets:
			print(tweet)
			

search = input('Enter search : ')
Bot = TwitterBot()
Bot.login('techX24672335', 'fake2TWITTER')
Bot.find_tweet(search)