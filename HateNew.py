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

import numpy
import Levenshtein
from deep_translator import GoogleTranslator

import nltk
from nltk import FreqDist
from nltk.util import ngrams
from nltk.stem.snowball import SnowballStemmer

##helpers
fuzzyLength = 3
compareOffset = 1 # offset to left & right
doubleOffset = compareOffset*2
hateListLanguage = "en"

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

# don't use nltk as it will give a generator which doesn't have a length which is needed
def makeFuzzy(text):
	return [text[i:j] for i in range(len(text)) for j in range(i + 1, len(text) + 1) if len(text[i:j]) == fuzzyLength]

def translateToEnglish(text):
	if len(text) > 5000:
		print("Received a text over 5000 characters long, which cannot be processed by FREE google translate api")
		return text
	if len(text) <= 2:
		return text
	try:
		res = GoogleTranslator(target=hateListLanguage).translate(text)
		if res is not None:
			return res
	except Exception as e:
		print("Failed to translate text. Your google translator daily limit might be full or given text input may be invalid")
		pass
	return text

# url: url where to search hate from
# hateList: list of different hatewords to be searched
# searchThreshold: threshold used to search words for matching
# verifyThreshold: threshold used to determine if speech is hate speech
# useTranslation: if true, forces the method to translate all texts. otherwise no translation is done
def hateSearch(url, hateList, transformList, searchThreshold, verifyThreshold, useTranslation):
	resp = requests.get(url)
	html_page = resp.content
	soup = BeautifulSoup(html_page, 'html.parser')
	fuzzyHateList = [makeFuzzy(clearFormat(t, transformList)) for t in hateList]

	# scan each html element with text
	for text in soup.stripped_strings:
		# skip short string, no need to scan them
		if(useTranslation):
			text = translateToEnglish(text)
		if text is None or len(text) < fuzzyLength:
			continue

		# remove possible text formatting
		clearedText = clearFormat(text, transformList)
		fuzzyText = makeFuzzy(clearedText)
		foundHate = set()
		originalHate = set()

		for fuzzyHateIndex in range(len(fuzzyHateList)):
			fuzzyHate = fuzzyHateList[fuzzyHateIndex]
			clearHate = hateList[fuzzyHateIndex]
			fuzzyHateLen = len(fuzzyHate)
			threshold = fuzzyHateLen/(fuzzyHateLen+doubleOffset) * searchThreshold

			if len(fuzzyText)+doubleOffset > fuzzyHateLen:
				for i in range(fuzzyHateLen-doubleOffset):
					textSnippet = fuzzyText[i:i+fuzzyHateLen+doubleOffset]
					jaccard = jaccardSimilarity(fuzzyHate, textSnippet)
					if jaccard >= threshold:
						matchedPiece = clearedText[i:i+fuzzyHateLen+doubleOffset]
						if Levenshtein.ratio(matchedPiece, clearHate) >= verifyThreshold:
							foundHate.add(matchedPiece)
							originalHate.add(clearHate)
			else:
				# use the text fully as its short
				jaccard = jaccardSimilarity(fuzzyHate, fuzzyText)
				if jaccard >= threshold:
					if Levenshtein.ratio(clearedText, clearHate) >= verifyThreshold:
						foundHate.add(clearedText)
						originalHate.add(clearHate)
		if len(foundHate) > 0:
			print("Found hate in '{}': {} matching terms {}".format(text, list(foundHate), list(originalHate)))


def readJsonFile(location):
	js = None
	with open(location, 'r', encoding="utf-8") as file:
		js = json.load(file)
	return js

if __name__ == "__main__":
	if(len(sys.argv) != 5):
		print("Invalid amount of arguments. When running the program, input 1st url to search the hate speech from and 2nd threshold (fuzzy search, jaccard similarity) to mark text to be checked (0.0-1.0, 0.4 recommended) and 3rd argument to mark the threshold (0.0-1.0, 0.6 recommended) for test (edit distance). The last argument must be a boolean determining wether or not the text sould be translated")
	else:
		transformList = readJsonFile('./format.json')
		hateList = readJsonFile('./hate.json')
		hateList = [clearFormat(t, transformList) for t in hateList]
		translate = sys.argv[4].lower() in ["true", "t", "y", "yes"]
		if translate:
			print("Starting to process given URL. Note that the processing may be very slow due to the translation of texts")
		hateSearch(sys.argv[1], hateList, transformList, float(sys.argv[2]), float(sys.argv[3]), translate)
