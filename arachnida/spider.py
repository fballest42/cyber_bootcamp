#!/usr/bin/env python3.7

import sys
import requests
from bs4 import BeautifulSoup
 
url = sys.argv[1] 
reqs = requests.get(url)
soup = BeautifulSoup(reqs.text, 'html.parser')
 
urls = []
for link in soup.find_all('a'):
    print(link.get('href'))