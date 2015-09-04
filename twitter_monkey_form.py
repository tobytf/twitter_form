import tweepy
from twitter import *
from TwitterSearch import *
import twitter
import re
import requests
import sys
import urlparse
import logging
import BeautifulSoup
from CREDS import *
import urllib3.contrib.pyopenssl
from typeformizer import convert_survey 
urllib3.contrib.pyopenssl.inject_into_urllib3()
logging.basicConfig(level=logging.WARN)


find_url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

monkey_check = re.compile('http[s]?://www.surveymonkey.com')
linkis_content = re.compile('longUrl: "(.*)"')
links = [
        {'function':'get_facebook', 'group':0 ,'re':re.compile('http[s]?://www\.facebook\.com/l\.php\?u=(.*)')},
        {'function':'get_tco', 'group':0, 're':re.compile('http[s]?://t.co/.*')},
        {'function':'get_linkis', 'group':0, 're':re.compile('http[s]?://linkis\.com/.*')},
        {'function':'get_google', 'group':0, 're':re.compile('https://www.google.com/url?(.*)')}
]

tso = TwitterSearchOrder()
tso.set_keywords(['surveymonkey'])
ts = TwitterSearch(
     consumer_key = TWITTER_CONSUMER_KEY,
     consumer_secret = TWITTER_CONSUMER_SECRET,
     access_token = TWITTER_ACCESS_TOKEN,
     access_token_secret = TWITTER_ACCESS_TOKEN_SECRET
)


def get_facebook(facebook_url):
    url_frags = urlparse.urlparse(facebook_url)
    query = urlparse.parse_qs(url_frags.query)
    url = query['u'][0]
    logging.debug('facebook %s ' % url)
    return url

def get_google(google_url):
    url_frags = urlparse.urlparse(google_url)
    orig_url = urlparse.parse_qs(url_frags.query)
    url = orig_url['url'][0]
    logging.debug('google %s ' % url)
    return url

def get_tco(tco_url):
    r = requests.get(tco_url)
    return r.url

def get_linkis(url):
    logging.debug('linkis url %s ' % url)
    r = requests.get(url)
    url_match = re.search(linkis_content,r.text)
    new_url =  url_match.group(1)
    return new_url

def check_url(url):
    logging.warn('got url %s' % url)

    for link_re in links:
        match = re.search(link_re['re'],url)
        if match:
            logging.info('found = %s' % link_re['function'])
            found_url = match.group(link_re['group'])
            new_url = getattr(sys.modules[__name__], link_re['function'])(found_url)
            break
    url = new_url

    return url

def main():

    surveys_hash = {}
    for tweet in ts.search_tweets_iterable(tso):
        logging.info( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )

        match = re.search(find_url,tweet['text'])
        
        if match:
            found_url = match.group(0)
            try:
                actual_url = check_url(found_url)
            except Exception as e:
                print 'bad url - %s' % found_url
                print e

            logging.warn("converting form ... %s " % actual_url)
            form = convert_survey(actual_url)
            typeform = form.submit()
            logging.warn("generated typeform ... %s " % typeform)
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
         

    for url in surveys_hash:
        print url

if __name__ == '__main__':
    main()
