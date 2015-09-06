from TwitterSearch import *
import re
import requests
import sys
import urlparse
import logging
import BeautifulSoup
from CREDS import *
from convert_monkey import monkey_to_typeform
logging.basicConfig(level=logging.WARN)


find_url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

monkey_check = re.compile('http[s]?://www.surveymonkey.com')
google_forms_check = re.compile('http[s]?://docs.google.com/forms')
forms_links = [
        {'class':'monkey_to_typeform', 'group':0 ,'re':monkey_check},
        {'class':'google_forms_to_typeform', 'group':0, 're':google_forms_check}

]

tso = TwitterSearchOrder()
#tso.set_keywords(['docs.google.com/forms'])
tso.set_keywords(['surveymonkey'])
ts = TwitterSearch(
     consumer_key = TWITTER_CONSUMER_KEY,
     consumer_secret = TWITTER_CONSUMER_SECRET,
     access_token = TWITTER_ACCESS_TOKEN,
     access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
)

def main():

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
	    for link_re in forms_links:
		match = re.search(link_re['re'],actual_url)
		if match:
                    logging.warn("converting form ... %s %s" % (actual_url,link_re['class']))
		    converter = getattr(sys.modules[__name__], link_re['class'])(r.text)
                    typeform = converter.to_typeform()
                    typeform_url = typeform.submit()
		    logging.warn("generated typeform ... %s " % typeform_url)
		    break

            '''
            # get page
            req = requests.get(actual_url)
            soup = BeautifulSoup.BeautifulSoup(req.text.lower())
            if 'powered bysurveymonkey' not in soup.text.lower():
                print 'orig url: %s, actual url: %s, is a PAID site' % (found_url,actual_url)
            else:
                print 'orig url: %s, actual url: %s, is a FREE site' % (found_url,actual_url)
            if found_url not in surveys_hash:
                surveys_hash[found_url] = ''
            '''

if __name__ == '__main__':
    main()
