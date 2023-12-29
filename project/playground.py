import requests
from bs4 import BeautifulSoup
import time
from promotion_links import *


def fetch_page_content(url):
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text,'html.parser')
    '<div class="single_tab" id="recent_tab">'
    print(x)
   


fetch_page_content(DOMAIN+UFC)