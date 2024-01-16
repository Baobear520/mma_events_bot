import logging
import requests
from bs4 import BeautifulSoup
import time
from promotion_links import UFC, PFL,ONE_FC, DOMAIN


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

def form_url(user_response: str):

    if user_response == 'UFC':
        promotion = UFC
    elif user_response == 'PFL':
        promotion = PFL
    elif user_response == 'ONE_FC':
        promotion = ONE_FC
    else:
        promotion = ''

    url = DOMAIN + promotion
    return url


def fetch_page_content(url):
    try:
        #Adding headers imitate requests from a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        if response:
            content = response.content
            logger.info(f"Got the content from {url}.")
            return content
        
        #Raise HTTPError if one occured
        response.raise_for_status()

    except Exception as e:
        logger.error(e)

def extract_all_recent_events_link_suffixes(url):
    """ Extracts all recent events dynamic links suffixes """

    #Fetching the html content of the page 
    content = fetch_page_content(url)
    time.sleep(2)  # 2-second delay between requests

    try:
        #Getting a soup object from the page
        soup = BeautifulSoup(content, features='html.parser')
        #Getting content within the tag
        recent_tab_div = soup.find('div', class_='single_tab', id='recent_tab')
        logger.info(f"Got the object.")

        #Getting a list of href attrs from the "a" tag 
        links = [item.get('href') for item in recent_tab_div.find_all('a')] 
        logger.info(f"Got a list of recent events links ({len(links)}) .")

        return links
    
    except Exception as e:
        logger.error(e)


def form_recent_event_links(url):
    """ Joins the domain name and the link suffixes to get the full url to events """
    try:
        events = extract_all_recent_events_link_suffixes(url)
        if events and len(events) >= 3:
            logger.info(f"There are more than 3 recent events. Extracting the links...")
            links = ["".join(DOMAIN + link) for link in events]
            logger.info(f"Extracted {len(links)} objects like '{links[0]}'")
            #Returning only 3 most recent events
            return links[:3]
        
        elif events and len(events) < 3:
            logger.info(f"There are fewer than 3 recent events. Extracting the links...")
            links = ["".join(DOMAIN + link) for link in events]
            logger.info(f"Extracted {links}")
            #Returning all the existing events 
            return links
        
        else:
            logger.info(f"There are no recent events. Returning an empty list.")
            return []
        
    except Exception as e:
        print("Error:", e)


def extract_all_upcoming_events_link_suffixes(url):
    """ Extracts all upcoming events dynamic links suffixes """ 

    #Fetching the html content of the page 
    content = fetch_page_content(url)
    time.sleep(2)  # 2-second delay between requests

     #Getting a soup object from the page
    soup = BeautifulSoup(content, features='html.parser')

    try:
        #Getting a soup object from the page
        soup = BeautifulSoup(content, features='html.parser')
        #Getting content within the tag
        upcoming_tab_div = soup.find('div', class_='single_tab', id='upcoming_tab')
        logger.info(f"Got the object.")

        #Getting a list of href attrs from the "a" tag 
        links = [item.get('href') for item in upcoming_tab_div.find_all('a')] 
        logger.info(f"Got a list of upcoming events links ({len(links)}).")

        return links
    
    except Exception as e:
        logger.error(e)
    


def form_upcoming_event_links(url):
    """ Joins the domain name and the link suffixes to get the full url to events """
    try:
        events = extract_all_upcoming_events_link_suffixes(url)
        if events and len(events) >= 3:
            logger.info(f"There are more than 3 upcoming events. Extracting the links...")
            links = ["".join(DOMAIN + link) for link in events]
            #Returning only 3 most recent events
            return links[:3]
        
        elif events and len(events) < 3:
            logger.info(f"There are fewer than 3 upcoming events. Extracting the links...")
            links = ["".join(DOMAIN + link) for link in events]
            #Returning all the existing events 
            return links
        
        else:
            logger.info(f"There are no upcoming events. Returning an empty list")
            return []
        
    except Exception as e:
        print("Error:", e)













