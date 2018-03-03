import sys
import csv
import os 
import re

num = 1

for dirPath, dirNames, fileNames in os.walk("./last_label"):
	for names in fileNames:
		temp = names.split(".")

		if (temp[1] != "txt"):
			continue


		fp = open("./last_label/" + names, "r")

		# Modefied raw file
		# op = open("./last_pos_movie/last_" + names, "w")
		op = open("./last_movie/not_" + str(num) + ".txt", "w")
		
		for line in fp:

			tranSet = ["(", ")", "[", "]", "!", "@", "^", "?", "#", "&", "$", "*", "~", ";", ":", "/", ",", "{", "}","\""]
			
			for element in tranSet:
				line = line.replace(element, " " + element + " ")

			line = re.sub("([-\'. ])+( )*", " ", line)

			# For generating non-marked file
			# line = line.replace("<>", "") 
			# line = line.replace("<\\>", "")

			# out = re.sub("([\"\'.,!:?*-;#$^&@ ])+( )*", " ", out)		
			op.write(line)
		
		op.close()
		fp.close()

		num += 1
