from TwitterSearch import *
import re
import requests
import sys
import urlparse
import logging
import BeautifulSoup
from CREDS import *
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

    try:
	for tweet in ts.search_tweets_iterable(tso):
	    logging.info( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

	    match = re.search(find_url,tweet['text'])
	    
	    if match:
		found_url = match.group(0)
                typeformizer.convert(found_url)

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

if __name__ == '__main__':
    main()
