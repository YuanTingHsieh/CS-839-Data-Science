import sys
import csv
import os 
import re

# Special class for dealing with document and position

class Instance():
	
	def __init__(self, doc, head, tail, text):
		self.doc = doc
		self.head = head
		self.tail = tail
		self.text = text
		self.label = 0	
	
	def getText(self):
		return self.text

	def setPos(self):
		self.label = 1;

	def printInfo(self):
		return self.text + "," + self.doc + "," + str(self.head) + "," + str(self.tail) + "," + str(self.label) + "\n"

	def check(self):
		temp = self.text
		if (temp.count("<>") >= 2):
			
			temp = temp.replace("<>", "")
			temp = temp.replace("<\\>", "")
			self.tail = self.head + len(temp) -1
			self.text = temp

		elif (temp.count("<\\>") >= 2):
			
			temp = temp.replace("<>", "")
			temp = temp.replace("<\\>", "")
			self.tail = self.head + len(temp) -1
			self.text = temp

		elif (temp[0:2] == "<>" and temp[-3:len(temp)] == "<\\>"):
			self.label = 1

		temp = temp.replace("<>", "")
		temp = temp.replace("<\\>", "")
		self.text = temp			



		