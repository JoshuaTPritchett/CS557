#Last update: 9/13 9pm

#imports
import sys
import stackexchange
import requests
from lxml import html  
from urllib.parse import urlparse  
import collections

#declare variables

#create StackOverflow object for use with the API
so = stackexchange.Site(stackexchange.StackOverflow)
so.impose_throttling = True
so.throttle_stop = False

#declare StackOverflow URL
STARTING_URL = "http://stackoverflow.com/questions/tagged/c"

#create queue and already-found URL set
urls_queue = collections.deque()  
urls_queue.append(STARTING_URL)  
found_urls = set()  
found_urls.add(STARTING_URL)

#process
while len(urls_queue):  
    url = urls_queue.popleft()

    response = requests.get(url)
    parsed_body = html.fromstring(response.content)

    # Prints the page title to console, checks if it is working
    print(parsed_body.xpath('//title/text()'))

    # Find all links
    links = {urllib.parse.urljoin(response.url, url) for url in parsed_body.xpath('//a/@href') if urllib.parse.urljoin(response.url, url).startswith('http')}

    # Set difference to find new URLs
    for link in (links - found_urls):
        #Only if it has the "C" tag (todo)
        found_urls.add(link)
        urls_queue.append(link)
#API calls here, just testing crawler for now