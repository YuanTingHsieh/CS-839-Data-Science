#coding=utf-8

import csv
import requests
from bs4 import BeautifulSoup
import sys
import pandas as pd
from lxml import etree
import time
import re

def parseTable(url, year):

	url = url + str(year)
	print "This is " + str(year)
	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser") 

	data = []
	table = soup.find('table', attrs={'class':'table'})
	# rows = table.find_all('tr')
	
	dataSet = table.find_all("a", class_ = "unstyled articleLink")
	for ele in dataSet:
		# print ele
		temp = str(ele.get("href"))
		data.append(temp)

	return data
	exit()


def dataReader(filename):
	inputfile = open(filename, "r")
	movie_name = []

	for line in inputfile:
		line = line.strip()
		line = line.replace(" ", "_")
		movie_name.append(line.lower())

	return movie_name

def writer(filename, count, text):
	outName = str(count) + ".txt"
	output = open(outName, "w")
	output.write(text)
	output.close()

	print "** " + filename + " is finished **\n"

def spider(name, num):

	url = "https://www.rottentomatoes.com" + name

	info = []
	for i in range(13):
		info.append("")

	info[0] = unicode(num)

	print "** " + name + " starts **"


	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "html.parser")
	# print soup
	pattern = re.compile(r'\(.*\)')
	
	title = soup.find(id = "movie-title")
	if title != None:
		title = title.get_text()# print title.get_text()
	
		year = pattern.findall(title)
		year = re.sub("[()]*","", year[0])

		title = re.sub(pattern, "", title).strip()
	
		info[1] = title
		info[2] = year


	# print info[1]
	# print info[2]

	# score = []
	# Tomatoter score
	scoreSet =soup.find_all("span", class_="meter-value superPageFontColor")
	
	try:
		if scoreSet != None:
			info[11] = (scoreSet[0].get_text())
			print info[11]
	except:
		print "scoreSet error!"		
		# print info[11]

	scoreSet =soup.find_all("span", class_="superPageFontColor")
	if scoreSet != None:
		for ele in scoreSet:
			if ele.string != None:
				text = ele.string.encode("utf-8")
				if (text[-1] == "%"):
					info[12] = text.decode("utf-8")

	# print info[12]

	# Collect attribute including "Rating", "Genre", "Director", "Writor", "Release", "Box Office", "Runtime", "Studio"
	feature = {}
	# labels = []
	dataSet = soup.find_all("div", class_="meta-value")

	if (dataSet != None):
		for link in dataSet:
			label = link.find_previous_sibling('div')
			text = link.get_text()
			
			text = re.sub(pattern, "", text)
			text = re.sub("[\n\r\t ]+", " ", text).strip()
			
			label = label.get_text().replace(":", "").strip()
			feature[label] = text

	else:
		print "!!! No." + str(name) + " WebPage is Error !!!\n"

	# print feature
	if "Rating" in feature:
		info[3] = feature["Rating"]
	if "Genre" in feature:
		info[5]= feature["Genre"]
	if "Directed By" in feature:
		info[8]= feature["Directed By"]
	if "Written By" in feature:
		info[10] = feature["Written By"]
	if "Runtime" in feature:
		info[4] = feature["Runtime"]
	if "Box Office" in feature:
		info[7] = feature["Box Office"]
	# info[14] = feature["Studio"]

    # Find all the cast
	pattern = re.compile(r'[.]*')

	# Only focus on castSection
	cast = ""
	castSet = soup.find("div", class_="castSection")
	if (castSet != None):
		castSet = castSet.find_all("span", attrs={"title": pattern})
		if (castSet != None):
			for index, star in enumerate(castSet):
				text = star.get_text().encode('utf-8').strip();
				if (text[0:2] != "as"):
					cast = cast + ", " + text
		else:
			print "!!! No." + str(name) + " WebPage is Error !!!\n"

	info[9] = cast[1:len(cast)].strip()
	# print info[9]

	return info

url = "https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page="

data = set()
# for i in range(100):
i = 0
while len(data) < 3000:
	print "Page: " + str(i)
	
	temp = url + str(i)
	source_code = requests.get(temp).json()
	
	for ele in source_code['results']:
		temp = ele['url']
		data.add(temp)
		# print (temp)
	i += 1

output = []
count = 3001
num = 0
# print data
# exit()

print "***"

# for ele in data:
# 	if ele[-4 :len(ele)] == "null":
# 		print ele
# 		continue;

for index, mv_url in enumerate(data):

	if mv_url == None:
		continue;
	if mv_url[-4 :len(mv_url)] == "null":
		continue;

	info = spider(mv_url, count)
	count += 1
	num += 1
	output.append(info)
	print "** Num: " + str(num) + " Pass **"

# print len(data)

# feature =  ["Rating", "Genre", "Director", "Writor", "Release", "Box Office", "Runtime", "Studio"]


# info = spider("/m/tomb_raider_2018",3001)
# output.append(info)

df = pd.DataFrame(output, columns=["movie_no", "movie_name", "movie_year", "movie_certificate", "movie_runtime", "movie_genre", "movie_score", "movie_gross", "movie_director","movie_star", "movie_writer", "tomatoter", "audience"])
df.to_csv('tomato.csv', index=False,  encoding='utf-8')

# spider("m/black_panther_2018")

