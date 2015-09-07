from TwitterSearch import *
import re
import requests
import sys
import urlparse
import logging
import BeautifulSoup
from CREDS import *
typeformizer = __import__('typeformizer')
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
		try:
		    r = requests.get(found_url)
		    actual_url = r.url
		    logging.warn('got url %s' % actual_url)
		except Exception as e:
		    print "couldn't get url - %s" % found_url
		    print e

		# now see if we can convert this this url
		for link_re in typeformizer.forms_links:
		    match = re.search(link_re['re'],actual_url)
		    if match:
			logging.warn("converting form ... %s %s" % (actual_url,link_re['class']))

			converter = getattr(typeformizer,link_re['class'])(r.text)
			typeform = converter.to_typeform()
			typeform_url = typeform.submit()
			logging.warn("generated typeform ... %s " % typeform_url)
			break

    except TwitterSearchException as e: # take care of all those ugly errors if there are some
        print(e)

if __name__ == '__main__':
    main()
