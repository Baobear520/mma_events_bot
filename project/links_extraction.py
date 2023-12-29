import requests
from bs4 import BeautifulSoup
import time
from promotion_links import *


def fetch_page_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response

def extract_all_events_link_suffixes(url):
    response = fetch_page_content(url)
    time.sleep(2)  # 2-second delay between requests
    soup = BeautifulSoup(response.content, features='html.parser')

    # Find the content of <tr> tag
    occurences= soup.find_all('tr')
    link_suffixes = []
    for item in occurences:
        # grab all the links suffixes that are available on click and strip extra characters
        suffix = str(item.get('onclick')).removeprefix("document.location=").removeprefix("'").removesuffix("';") 
        link_suffixes.append(suffix)
    link_suffixes.remove('None')
    return link_suffixes
    
def recent_events_link_suffix(url):
    events = extract_all_events_link_suffixes(url)
    separator_index = events.index('None') + 1 #find index of fist "None" and grab the next value
    events = events[separator_index:(separator_index+5)] #grab 5 most recent events
    return events
    
def recent_event_link(url,num):
    try:
        events = recent_events_link_suffix(url)
        url_domain = url.removesuffix("/organizations/Ultimate-Fighting-Championship-UFC-2")
        link = url_domain + events[num]
        return link
    except Exception as e:
        print("Error:", e)

def upcoming_events_link_suffix(url):
    events = extract_all_events_link_suffixes(url)
    events = events[:5] #grab 5 upcoming events
    return events

def upcoming_event_link(url,domain,num):
    try:
        events = upcoming_events_link_suffix(url)
        print(events)
        if events is not []:
            link = domain + events[num]
            return link
        else:
            print('No upcoming events found')
            return url
    except Exception as e:
        print("Error:", e)
    
url = DOMAIN + PFL
print(upcoming_event_link(url,DOMAIN,0))











