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
        if t.parent.name not in blacklist:
            data += '{} '.format(t)
            
            
    print(data)
    
    return data