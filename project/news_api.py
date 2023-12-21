import requests
from bs4 import BeautifulSoup


def get_ufcstat_response(url):
    response = requests.get(url)
    return response

def parse_links(response):
    soup = BeautifulSoup(response.content,features='html.parser')
    links_to_events = []
    for link in soup.find_all('a'):
        url = str(link.get('href'))
        if url.startswith('http://ufcstats.com/event-details/'):
            links_to_events.append(url)
    return links_to_events

def get_last_and_next():
    url = "http://ufcstats.com/statistics/events/completed"
    response = get_ufcstat_response(url)
    links_to_events = parse_links(response)
    next = links_to_events[0] 
    last = links_to_events[1]
   
    return next, last



if __name__ == "__main__":
    get_most_recent_and_upcoming()

    

    
    
    
            
            
    

        
    

    
