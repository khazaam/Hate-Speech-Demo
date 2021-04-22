# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 13:08:29 2021

@author: peikk
"""

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

##hateSearch starts from here

def hateSearch():
    url = input("Enter a website url: ")
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
    ##TODO This is just hardcoded list, might be used url instead
    hateList = [
        'Anonymous'
        'allah akbar',
        'blacks',
        'chink',
        'chinks',
        'dykes',
        'faggot',
        'faggot',
        'fags',
        'gay',
        'gay.',
        'GAY',
        'homo',
        'inbred',
        'nigger',
        'nigger.',
        'niggers',
        'queers',
        'raped',
        'savages',
        'slave',
        'spic',
        'wetback',
        'wetbacks',
        'whites',
        'a dirty',
        'a nigger',
        'all niggers',
        'all white',
        'always fuck',
        'ass white',
        'be killed',
        'beat him',
        'biggest faggot',
        'blame the',
        'butt ugly',
        'chink eyed',
        'chinks in',
        'coon shit',
        'dumb monkey',
        'dumb nigger',
        'fag and',
        'fag but',
        'Faggots',
        'faggot',
        'Faggot',
        'faggot a',
        'faggot and',
        'faggot ass',
        'faggot bitch',
        'faggot for',
        'faggot smh',
        'faggot that',
        'faggots and',
        'faggots like',
        'faggots usually',
        'faggots who',
        'fags are',
        'fuckin faggot',
        'fucking faggot',
        'fucking gay',
        'fucking hate',
        'fucking nigger',
        'fucking queer',
        'gay ass',
        'get raped',
        'hate all',
        'hate faggot',
        'hate fat',
        'hate you',
        'here faggot',
        'is white',
        'jungle bunny',
        'kill all',
        'kill yourself',
        'little faggot',
        'many niggers',
        'married to',
        'me faggot',
        'my coon',
        'nigga ask',
        'niggas like',
        'nigger ass',
        'nigger is',
        'nigger music',
        'niggers are',
        'of fags',
        'of white',
        'raped and',
        'raped by',
        'sand nigger',
        'savages that',
        'shorty bitch',
        'spear chucker',
        'spic cop',
        'stupid nigger',
        'that fag',
        'that faggot',
        'that nigger',
        'the faggots',
        'the female',
        'the niggers',
        'their heads',
        'them white',
        'then faggot',
        'this nigger',
        'to rape',
        'trailer park',
        'trash with',
        'u fuckin',
        'ugly dyke',
        'up nigger',
        'white ass',
        'white boy',
        'white person',
        'white trash',
        'with niggas',
        'you fag',
        'you nigger',
        'you niggers',
        'your faggot',
        'your nigger',
        'a bitch made',
        'a fag and',
        'a fag but',
        'a faggot and',
        'a faggot for',
        'a fucking queer',
        'a nigga ask',
        'a white person',
        'a white trash',
        'all these fucking',
        'are all white',
        'be killed for',
        'bitch made nigga',
        'faggots like you',
        'faggots usually have',
        'fuck outta here',
        'fuck u talking',
        'fuck you too',
        'fucking hate you',
        'full of white',
        'him a nigga',
        'his shorty bitch',
        'how many niggers',
        'is a fag',
        'is a faggot',
        'is a fuckin',
        'is a fucking',
        'is a nigger',
        'like a faggot',
        'like da colored',
        'many niggers are',
        'nigga and his',
        'niggers are in',
        'of white trash',
        'shut up nigger',
        'still a faggot',
        'the biggest faggot',
        'the faggots who',
        'the fuck do',
        'they all look',
        'what a fag',
        'white bitch in',
        'white trash and',
        'you a fag',
        'you a lame',
        'you a nigger',
        'you fuck wit',
        'you fucking faggot',
        'your a cunt',
        'your a dirty',
        'your bitch in',
        'a bitch made nigga',
        'a lame nigga you',
        'faggot if you ever',
        'full of white trash',
        'how many niggers are',
        'is full of white',
        'lame nigga you a',
        'many niggers are in',
        'nigga you a lame',
        'niggers are in my',
        'wit a lame nigga',
        'you a lame bitch',
        'you fuck wit a',
        'Wikipedia is not a place for hate speech, and such bigotry'
        ]
    
    for t in textFind:
        ##TODO go trought the wholelist somehow, now it only checks this one word
        if "faggot" in hateList:
            ##data += '{} '.format(t)
            hatedata  += '{} '.format(t)
            print('Found some hate elements')

        if t.parent.name not in blacklist:
            data += '{}'.format(t)
            ##print(data)

    print(hatedata, "hatedata")
    return hatedata