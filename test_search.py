from TwitterSearch import TwitterSearchOrder, TwitterSearch, TwitterSearchException
from CREDS import *

ts = TwitterSearch(
                  consumer_key = TWITTER_CONSUMER_KEY,
                  consumer_secret = TWITTER_CONSUMER_SECRET, 
                  access_token = TWITTER_ACCESS_TOKEN,
                  access_token_secret = TWITTER_ACCESS_TOKEN_SECRET,
                  )

try:
    tso = TwitterSearchOrder()
    tso.set_keywords(['surveymonkey','docs.google.com/forms'], or_operator=True)

    for tweet in ts.search_tweets_iterable(tso):
        print('@%s tweeted: %s' % (tweet['user']['screen_name'], tweet['text']))

except TwitterSearchException as e:
   print(e)
