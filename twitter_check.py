import tweepy
from TYPEFORMIZER_TWITTER_SETUP import *

auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

direct_messages = api.direct_messages()
for tweet in direct_messages:
        print tweet.text
