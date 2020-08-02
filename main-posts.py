
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import numpy as np
import requests
import json
import pandas as pd
from datetime import datetime

class InstagramBot:

	def __init__(self, username, password):

		self.username = username
		self.password = password
		self.driver = webdriver.Chrome()

	def closeBrowser(self):
		self.driver.close()

	def login(self):

		driver = self.driver
		driver.get("https://www.instagram.com/accounts/login/")
		time.sleep(3)
		user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
		user_name_elem.clear()
		user_name_elem.send_keys(self.username)
		passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
		passworword_elem.clear()
		passworword_elem.send_keys(self.password)
		passworword_elem.send_keys(Keys.RETURN)
		time.sleep(3)


	def recent_post_links(self, username, post_count):

		driver = self.driver
		url = "https://www.instagram.com/" + username + "/"
		driver.get(url)
		post = 'https://www.instagram.com/p/'

		post_links = []
		while len(post_links) < post_count:
			links = [a.get_attribute('href') 
					for a in driver.find_elements_by_tag_name('a')]

			for link in links:

				if post in link and link not in post_links:
					post_links.append(link)

			scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
			driver.execute_script(scroll_down)
			time.sleep(3)

		driver.quit()

		return post_links[:post_count]

	def insta_details_json(self, url):

	   
		url_final = url + '?__a=1'
		res = requests.get(url_final)

		try: 
			likes = res.json()['graphql']['shortcode_media']['edge_media_preview_like']['count']
			post_type='photo'
			age = 'indefinido'

			post_details = {'link':url, 'type':post_type, 'likes/views':likes, 'age':age}

			return post_details

		except Exception as e:
			print(e)
			return None

	def percentil(self, info_posts, percentil_post):

		array_likes = []

		for dic in info_posts:
			if dic['type']=='photo':
				array_likes.append(dic['likes/views'])

		try :
			percentil_likes = np.percentile(array_likes, percentil_post)
			print("El percentil {} de los post es: {}".format(percentil_post, percentil_likes))
			return percentil_likes

		except: 
			print("{} no ha publicado videos".format(username_URL))
			return None
	

	def choose_post(self, info_posts, percentil_likes):

		username_post = []

		for dic in info_posts:
			if dic['type']=='photo' and dic['likes/views'] >= percentil_likes:
				username_post.append(dic) 

		return username_post


	def export_info(self, username_posts, instagramUser):

		date = datetime.now()

		name_archive = instagramUser + '(' + str(date.day) + '-' + str(date.month) + '-' + str(date.year) + ')'
		dataFrame_post = pd.DataFrame(username_posts) 
		dataFrame_post.drop(['type'], axis='columns', inplace=True)
		dataFrame_post.to_csv('posts/' + name_archive + '.csv') 


if __name__ == "__main__":

	#------------------------------------------
	#------------------------------------------
	#------------------------------------------
	#VARIABLES A USAR:

	print(".................................................")
	print(".................................................")
	print("..................BIENVENIDO.....................")
	print('\n')

	username = "userNameExample"
	password = "passwordExample"

	instagramUser = input("¿Qué página quieres evaluar? ")
	post = int(input("¿Cuántos posts? "))
	percentil_post = int(input("Tomar posts por encima del percentil: "))
	
	print('\n')
	print(".................................................")
	print(".................................................")

	#------------------------------------------
	#------------------------------------------
	#------------------------------------------

	t0 = time.time()
	print ("Tiempo 0: {} segundos".format(t0))

	ig = InstagramBot(username, password)
	ig.login()

	t1 = time.time()-t0
	print ("Ya ingrese a Instagram, llevo: {} segundos".format(t1))

	list_urls = ig.recent_post_links(instagramUser, post)
	print(list_urls)

	t2 = time.time()-t0
	print ("Ya tome los links, llevo: {} segundos".format(t2))

	dict_post = [ig.insta_details_json(url) for url in list_urls]

	t3 = time.time()-t0
	print ("Ya tome los detalles, llevo: {} segundos".format(t3))

	percentil_value = ig.percentil(dict_post, percentil_post)

	t4 = time.time() - t0
	print ("Ya calcule el percentil, llevo: {} segundos".format(t4))

	chosen_posts = ig.choose_post(dict_post, percentil_value)

	t5 = time.time() - t0
	print ("Ya recupere los post de interes, llevo: {} segundos".format(t5))

	ig.export_info(chosen_posts, instagramUser)

	t6 = time.time() - t0
	print ("Tiempo final: {} segundos".format(t6))