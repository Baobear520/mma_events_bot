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

def extract_events_link_suffixes(url,action):
    """ Extracts all events dynamic links suffixes """

    #Fetching the html content of the page 
    content = fetch_page_content(url)
    time.sleep(2)  # 2-second delay between requests

    try:
        #Getting a soup object from the page
        soup = BeautifulSoup(content, features='html.parser')
        #Getting content within the tag
        logger.info(f"the value of 'action' is {action}")
        if action == "/last":
            div_obj = soup.find('div', class_='single_tab', id='recent_tab')
            logger.info("Scraped the 'recent' tab.")
        elif action == "/next":
            div_obj = soup.find('div', class_='single_tab', id='upcoming_tab')
            logger.info("Scraped the 'upcoming' tab.")

        #Getting a list of href attrs from the "a" tag 
        links = [item.get('href') for item in div_obj.find_all('a')] 
        logger.info(f"Got a list of event links ({len(links)}) .")

        return links
    
    except Exception as e:
        logger.error(e)


def form_event_links(url,action):
    """ Joins the domain name and the link suffixes to get the full url to events """
    try:
        link_suffixes = extract_events_link_suffixes(url,action)
        if link_suffixes:
            links = ["".join(DOMAIN + link) for link in link_suffixes]
            logger.info(f"Extracted {len(links)} objects like '{links[0]}'")
            #Returning only 3 most recent events
            return links
        else:
            logger.info(f"There are no events. Returning an empty list.")
            return []
        
    except Exception as e:
        logger.error(e)





