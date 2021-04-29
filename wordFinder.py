# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 21:19:33 2021

@author: peikk

This is the manual
word finder, or the one that finds the words from list but
does not count nothing else but the finding and mount.
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

##parse hate terms from vocab
hateList = []
with open('./hate.json', 'r', encoding="utf-8") as file:
	hateList = json.load(file)

transformList = {}
with open('./format.json', 'r', encoding="utf-8") as file:
	transformList = json.load(file)

##helpers

def clearFormat(text):
	text = text.lower()
	for key in transformList:
		for matcher in transformList[key]:
			text = text.replace(matcher, key)
	return text


##hateSearch starts from here
##Hate search is not working currectly, input works, but gives false positive everytime.
def hateSearch(url):
    resp = requests.get(url)

    ##add input word spot
    
    ##testing with one word at the time
    ##if you wish to test with just one word you can change this to the word you want to find
    testi_sana = ("subhuman")
    
    html_page = resp.content
    soup = BeautifulSoup(html_page, 'html.parser')
    ##TODO make a similar list or file where you can get the textFind contents
    textFind = soup.find_all(text=True)
    
     ##Note,  use [] list as a finding stuff, but {} does not find any
    hateFound = soup.body.find_all(text=re.compile('.*{0}.*'.format(testi_sana)),recursive=True)
    
    print('Hate word found "{0}" {1} time\n'.format(testi_sana, len(hateFound)))
    
    
    for content in hateFound:
        words = content.split()
        for index, word in enumerate(words):
            if word == testi_sana:
                print('Found from: "{0}"'.format(content))
                before = None
                after = None
                if index != 0:
                    before = words[index -1] ##not sure is it index -1 or index-1
                if index != len(words) -1:
                    after = words[index +1]
                print('\word before: "{0}", word after: "{1}"').format(before, after)
                return 



if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print("Invalid amount of arguments. When running the program, input 1 url to search the hate speech from")
	else:
		hateSearch(sys.argv[1])
