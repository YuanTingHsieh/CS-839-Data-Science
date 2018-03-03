#coding=utf-8

import sys
import os
import re
import json
from instance import Instance

def keep(word, black_list ,ver=2):
	if ver == 1:
		if word.lower() in black_list:
			return False
		else:
			return True	
	else:
		for element in black_list:
			if word.lower() == element.lower():
				return False
			else:
				return True


def process(inFile, pathname):

	fp = open(pathname + inFile, "r")

	num_of_mark = 0
	tempList = []
	empty = True

	for line in fp:
		line = line.split("<>");

		line.pop(0);
		
		for element in line:
			
			element = element.split("<\\>")
			out = re.sub("([\"\'.,!:?*()-;#$^&@[\]{} ])+( )*", " ", element[0])
			out = out.strip()
			
			if out != "":
				# print out
				num_of_mark += 1

	fp.close()		

	return num_of_mark

def slide(names, fileNum, pathname, black_list):
	fp = open(pathname + names, "r")

	for line in fp:
		line = line.split()

	strList = []
	# Depends on how you count 0:vim, 1:sublime
	head = 1;
	tail = 0;

	for index, text in enumerate(line):
		
		count = 0
		valid = True;
		tranSet = ["(", ")", "[", "]", "!", "@", "^", "?", "#", "&", "$", "*", "~", ";", ":", "/", ",", "{", "}", "\""]

		while (count <= 4):
			temp = ""
			trim = ""
			num = 0
			# count = 4, range = [0,1,2,3]
			while num < count and valid:
				if (index + num <= len(line)-1):
					trim = line[index + num]
					trim = trim.strip()
					
					# if (not keep(trim, black_list[0], 1)):
					# 	valid = False
					
					for ill in tranSet:
						if (ill in trim or (not trim[0].isupper() and trim[0:2] != "<>")):
							valid = False

					temp += trim + " "

				num += 1
			

			if valid and (index + count <= len(line)):
				temp = temp.strip()

				if temp != "":
					size = len(temp)
					if ("<>" in temp):
						size -= 2
					if ("<\\>" in temp):
						size -= 3

					inst = Instance(fileNum, head, head + size - 1, temp)
					inst.check()
					strList.append(inst)

			count += 1
			valid = True
		
		if (text[0:2] == "<>"):
			head += len(text) + 1 - 2
		else:
			head += len(text) + 1

		if (text[-3:len(text)] == "<\\>"):
			head -= 3

	fp.close()

	return strList;

def main():	
	
	op = open("last_example.txt", "w")
	# fp = open('black_list.json', 'r')

	# black_list = json.load(fp)

	candList = []
	num_of_cand = 0
	num_of_mark = 0
	veri_num = 0
	pathname = "./last_movie/"

	for dirPath, dirNames, fileNames in os.walk(pathname):
		for names in fileNames:		
			check = names.split(".")

			if (check[1] == "txt"):
				check = check[0].split("_")
				fileNum = check[1]

				veri_num += process(names, pathname)
				temp = slide(names, fileNum, pathname, black_list)
				
				num_of_cand += len(temp)
				candList.append(temp)

	for i in range(len(candList)):
		for inst in candList[i]:
			if inst.label == 1:
				print inst.getText()
				num_of_mark += 1
			# print inst.printInfo()

	# print "Actual Num of Mark: " + str(veri_num)
	print "Number of Mark: " + str(num_of_mark)
	print "Number of Instance: " + str(num_of_cand)
	
	for sub in candList:
		for example in sub:
			op.write(example.printInfo())

	# fp.close()
	op.close()

if __name__ == "__main__":
	main()
	# main()