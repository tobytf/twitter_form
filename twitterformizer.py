from TwitterSearch import *
import re
import requests
import sys
import urlparse
import logging
import BeautifulSoup
from CREDS import *
import selenium.webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import typeformizer
logging.basicConfig(level=logging.WARN)

find_url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

tso = TwitterSearchOrder()
tso.set_keywords(['surveymonkey','docs.google.com/forms'],or_operator=True)
ts = TwitterSearch(
     consumer_key = TWITTER_CONSUMER_KEY,
     consumer_secret = TWITTER_CONSUMER_SECRET,
     access_token = TWITTER_ACCESS_TOKEN,
     access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
)

def main():
    webdriver_phantom = selenium.webdriver.PhantomJS()
    webdriver_chrome = selenium.webdriver.Chrome()
    try:
	for tweet in ts.search_tweets_iterable(tso):
	    logging.info( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

	    match = re.search(find_url,tweet['text'])
	    
	    if match:
		found_url = match.group(0)
                converted_url = typeformizer.convert(found_url)
                if converted_url is not None:
                    webdriver_phantom.get(converted_url)
                    webdriver_phantom.implicitly_wait(10) # seconds
                    wait = WebDriverWait(webdriver_phantom, 10)
                    try:
                        element = WebDriverWait(webdriver_phantom, 10).until(
                                            EC.invisibility_of_element_located((By.ID,'loader'))
                                                )
                        webdriver_phantom.get_screenshot_as_file('./typeform.png') 
                        webdriver_chrome.get('file:///Users/toby/development/twitter_form/typeform.png')
                    except Exception as e:
                        logging.warn("Couldn't get typeform screenshot form %s" % e)

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

if __name__ == '__main__':
    main()
