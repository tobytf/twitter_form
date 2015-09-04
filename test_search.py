from TwitterSearch import TwitterSearchOrder, TwitterSearch
from CREDS import *

ts = TwitterSearch(
                  consumer_key = TWITTER_CONSUMER_KEY,
                  consumer_secret = TWITTER_CONSUMER_SECRET, 
                  access_token = TWITTER_ACCESS_TOKEN,
                  access_token_secret = TWITTER_ACCESS_TOKEN_SECRET,
                  )

try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['surveymonkey'])

    ts = TwitterSearch(
                      consumer_key = CONSUMER_KEY,
                      consumer_secret = CONSUMER_SECRET,
                      access_token = ACCESS_TOKEN,
                      access_token_secret = ACCESS_TOKEN_SECRET,
                      )

    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:
   print(e)
