# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:08:29 2021

@author: peikk, Matti
"""

import sys
import json

import urllib.request
from urllib.request import urlopen
import re

from bs4 import BeautifulSoup
import requests

import nltk
from nltk import FreqDist
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer

##helpers
fuzzyLength = 3
compareOffset = 1 # offset to left & right
doubleOffset = compareOffset*2

def clearFormat(text, transformList):
	text = text.lower()
	for key in transformList:
		for matcher in transformList[key]:
			text = text.replace(matcher, key)
	text = re.sub("[^a-z]+", "", text)
	return text

def jaccardSimilarity(group1, group2):
	intersection = len(set(group1).intersection(set(group2)))
	union = len(set(group1)) + len(set(group2)) - intersection
	return float(intersection)/union

def makeFuzzy(text):
	return [text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1) if len(text[i:j]) == fuzzyLength]

##hateSearch starts from here
##Hate search is not working currectly, input works, but gives false positive everytime.
def hateSearch(url, hateList, transformList, hateTreshold):
	resp = requests.get(url)
	html_page = resp.content
	soup = BeautifulSoup(html_page, 'html.parser')
	# scan each html element with text
	for text in soup.stripped_strings:
		# skip short string, no need to scan them
		if len(text) < fuzzyLength:
			continue

		# remove possible text formatting
		clearedText = clearFormat(text, transformList)
		fuzzyText = makeFuzzy(clearedText)
		foundHate = set()

		for fuzzyHate in hateList:
			threshold = len(fuzzyHate)/(len(fuzzyHate)+doubleOffset) * hateTreshold

			if len(fuzzyText)+doubleOffset > len(fuzzyHate):
				for i in range(len(fuzzyHate)-doubleOffset):
					textSnippet = fuzzyText[i:i+len(fuzzyHate)+doubleOffset]
					if jaccardSimilarity(fuzzyHate, textSnippet) >= threshold:
						foundHate.add(clearedText[i:i+len(fuzzyHate)+doubleOffset])
			else:
				# use the text fully as its short
				if jaccardSimilarity(fuzzyHate, fuzzyText) >= threshold:
					foundHate.add(clearedText)
		if len(foundHate) > 0:
			print("Found hate in '{}': {}".format(text, list(foundHate)))


def readJsonFile(location):
	js = None
	with open(location, 'r', encoding="utf-8") as file:
		js = json.load(file)
	return js

if __name__ == "__main__":
	if(len(sys.argv) != 3):
		print("Invalid amount of arguments. When running the program, input 1st url to search the hate speech from and 2nd threshold to mark text as hate speech (0.0-1.0, 0.5 recommended)")
	else:
		transformList = readJsonFile('./format.json')
		hateList = readJsonFile('./hate.json')
		# remove formatting from hatelist
		hateList = [makeFuzzy(clearFormat(t, transformList)) for t in hateList]
		hateSearch(sys.argv[1], hateList, transformList, float(sys.argv[2]))
