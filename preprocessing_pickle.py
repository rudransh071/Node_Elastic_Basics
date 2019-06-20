from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
import pafy as pf
import pandas as pd
import pandas as pd
import numpy as np
import enchant

eng_checker = enchant.Dict('en_US')
pattern = re.compile(r'\/watch\?v=')
pattern_playlist = re.compile(r'list=')
inverse_categ_dict = {}

#get all URLs for particular channel
def get_urls():
	urls = []
	driver = webdriver.Chrome()
	driver.get("https://www.youtube.com/channel/UC0PTktRYpZXb6On0_zFKWIg/videos")
	for i in range(45):
		source = driver.page_source
		driver.find_element_by_tag_name('html').send_keys(Keys.END)
		soup = BeautifulSoup(source, 'html.parser')
		for link in soup.find_all('a'):
			urls.append(link.get('href'))
	
	tmp_url = []
	for url in urls:
		if(re.match(pattern, str(url)) and len(re.findall(pattern_playlist, str(url))) == 0):
			tmp_url.append(url)
	urls = tmp_url
	urls = [url for url in urls if len(url) > 0]
	urls = list(set(urls))
	urls = [('www.youtube.com'+url) for url in urls]
	urls = urls[: max(len(urls), 2000)]
	return urls

def preprocess(text):
	text = " ".join(re.findall("[a-zA-Z]+", text))
	text = " ".join(word for word in text.split() if len(word) > 2)
	text = " ".join(word for word in text.split() if eng_checker.check(word))
	return text

#how I calculate trending score
def trend_score(row):
	return (((row['Likes'] + row['Dislikes'])*20)/row['Total_time']) + (row['Views']/row['Total_time'])

def dump_database():
	urls = get_urls()
	print("Extracted all URLs. Scraping data now", end = '\n')
	creation_date = []
	video_id = []
	likes = []
	length = []
	views = []
	text = []
	dislikes = []
	for url in urls:
		try:
			vid = pf.new(str(url))
			text.append(str(vid.title) + " " +str(vid.description))
			video_id.append(vid.videoid)
			creation_date.append(vid.published)
			views.append(vid.viewcount)
			likes.append(vid.likes)
			dislikes.append(vid.dislikes)
			length.append(vid.length)
		except (OSError,IndexError) as e:
			pass
	print("Scraping finished")

	train_data = pd.DataFrame(columns = ['Video_Id', 'Text', 'Views', 'Likes', 'Dislikes'
											'Length', 'Creation_Date'])
	for i in range(len(length)):
		print(i)
		train_data.loc[i] = [str(video_id[i]), str(text[i]), str(views[i]), str(likes[i]), str(dislikes[i]), str(length[i]), str(creation_date[i])]
	
 	train_data['Text'] = train_data['Text'].map(preprocess)
	train_data['Creation_Date'] = pd.to_datetime(train_data['Creation_Date'], format = '%Y-%m-%d %H:%M:%S')
 	train_data['Creation_Date'] = pd.datetime.now() - train_data['Creation_Date']
 	train_data['Total_time'] = train_data['Creation_Date'].dt.total_seconds()
 	train_data = train_data.fillna(0)
 	train_data['Trend_Score'] = train_data.apply (lambda row: trend_score(row), axis=1)
 	train_data.to_pickle('dataframe.pkl')
