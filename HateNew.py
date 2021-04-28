# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:08:29 2021

@author: peikk
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

##testing variables
name = "Ville"

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

def hateSearch(url):
    resp = requests.get(url)

    html_page = resp.content
    soup = BeautifulSoup(html_page, 'html.parser')
    ##TODO make a similar list or file where you can get the textFind contents
    textFind = soup.find_all(text=True)

    ##TODO to parse the data what we are looking for, either manual list or make url for it

    data = ''
    hatedata = ''

    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head',
        'input',
        'script',
        'style'
        ]

    for t in textFind:
        ##TODO go trought the wholelist somehow, now it only checks this one word
        if any(hateList):
            ##data += '{} '.format(t)
            hatedata  += '{} '.format(t)
            print('Found some hate elements')

        if t.parent.name not in blacklist:
            data += '{}'.format(t)
            ##print(data)

    print(hatedata, "hatedata")
    return hatedata

if __name__ == "__main__":
	if(len(sys.argv) != 2):
		print("Invalid amount of arguments. When running the program, input 1 url to search the hate speech from")
	else:
		hateSearch(sys.argv[1])
