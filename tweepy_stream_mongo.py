#import the necesary dependacies
import tweepy
from pymongo import MongoClient
import dataset
import sys
import pymongo

#write a list of topics you want your streamer to collect
words = ['words','#hashtags']

# Twitter API keys
#go to http://apps.twitter.com and create an app.
CONSUMER_KEY = "your consumer key"
CONSUMER_SECRET = "your consumer secret"
ACCESS_TOKEN = "your access token"
ACCESS_TOKEN_SECRET = "your access token secret"

class StreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener,self).__init__()

        #.TwitterStream is the name of the databse
        #robomongo gives a live GUI view of the twitter data
        self.db = pymongo.MongoClient().TwitterStream

    #can choose to collect particular information from a tweet
    #visit https://dev.twitter.com/overview/api/tweets to see what information can be mined
    def on_status(self, status):
        if status.retweeted:
            return

        data = {}
        text = status.text #collect the text from a tweet
        data['text'] = status.text # import into column 'text'
        data['created_at'] = status.created_at # collect when tweet was created 'created_at'
        

        # .tweets is the name of the collection in mongodb
        #you can change this 
        self.db.tweets.insert(data)

    def on_error(self, status_code):
        print(sys.stderr, 'Status code error:', status_code)
        return True

    def on_timeout(self):
        print(sys.stderr, 'Timed out...')
        return True

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


sapi = tweepy.streaming.Stream(auth, StreamListener(api))
sapi.filter(track=words)