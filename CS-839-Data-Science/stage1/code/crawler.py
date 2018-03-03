#coding=utf-8

import csv
import requests
from bs4 import BeautifulSoup

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

def spider(name, count):

	url = "https://www.rottentomatoes.com/m/" + name

	print "** " + name + " starts **"

	source_code = requests.get(url)
	plain_text = source_code.text
	soup = BeautifulSoup(plain_text, "lxml") 

	dataSet = soup.find(id = "movieSynopsis")

	if (dataSet != None):
		for link in dataSet:
			text = link.encode('utf-8').strip()
	else: 
		text = ""

		print ""
		print "!!! No." + str(count) + " WebPage is Error !!!\n"

	return text

count = 1	
nameList = dataReader("movie.txt")

for name in nameList:
	text =  spider(name, count)
	writer(name, count, text)
	count += 1



