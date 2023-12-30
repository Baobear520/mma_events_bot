import requests
from bs4 import BeautifulSoup
import time
from promotion_links import DOMAIN, UFC



def form_url(promotion):
    url = DOMAIN + promotion
    return url

def fetch_page_content(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response

def extract_all_recent_events_link_suffixes(url):
    response = fetch_page_content(url)
    time.sleep(2)  # 2-second delay between requests
    soup = BeautifulSoup(response.content, features='html.parser')
    recent_tab_div = soup.find('div', class_='single_tab', id='recent_tab')
    links = []
    for item in recent_tab_div.find_all('a'):
        suffix = item.get('href')
        links.append(suffix)
    return links


def form_recent_event_link(url,num):
    try:
        events = extract_all_recent_events_link_suffixes(url)
        if events:
            link = DOMAIN + events[num]
            return link
        else:
            return url
    except Exception as e:
        print("Error:", e)


def extract_all_upcoming_events_link_suffixes(url):
    response = fetch_page_content(url)
    time.sleep(2)  # 2-second delay between requests
    soup = BeautifulSoup(response.content, features='html.parser')

    recent_tab_div = soup.find('div', class_='single_tab', id='upcoming_tab')
    if recent_tab_div:
        links = []
        for item in recent_tab_div.find_all('a'):
            suffix = item.get('href')
            links.append(suffix)
        return links
    else:
        return []


def form_upcoming_event_link(url,num):
    try:
        events = extract_all_upcoming_events_link_suffixes(url)
        if events:
            link = DOMAIN + events[num]
            return link
        
        else:
            return url
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    url = DOMAIN + UFC
    print(form_upcoming_event_link(url,0))










