import tweepy
from tweepy import StreamListener, Stream
import gzip
import time
import datetime
import json

tweets = []
initial_time = time.time()

class StdOutListener(StreamListener):

    def on_data(self, raw_data):
        global tweets, initial_time
        elapsed_time = time.time () - initial_time #elapsed secons
        #save the status every 30 mins
        if elapsed_time >= 60 * 30:
            now = datetime.datetime.now()
            file_name = './corpus_new/tweets-%s-%s-%s-%s-%s.txt.gz' % (now.month, now.day, now.hour, now.minute, now.second)
            print 'Writing file:', file_name
            with gzip.open(file_name, 'w') as f:
                for tweet in tweets:
                    f.write(json.dumps(tweet) + '\n')
            print 'Writing finished'
            tweets = []
            initial_time = time.time()

        try:
            data = json.loads(raw_data)
            tweets.append(data)
        except:
            now = datetime.datetime.now()
            print '(%s %s:%s)Invalid json data: %s' % (now.day, now.hour, now.minute, raw_data)

        return True

    def on_error(self, status_code):
        now = datetime.datetime.now()
        print '(%s %s:%s)Got an error with status code: %s' % (now.day, now.hour, now.minute, status_code)
        #sleep 5 mins if an error occurs
        time.sleep(5 * 60)
        return True # To continue listening

    def on_timeout(self):
        print 'Timeout...'
        return True # To continue listening
if __name__ == '__main__':
    print 'Starting...'
    CONFIG_FILEPATH = './conf/'
    config_twitter = json.load(open(CONFIG_FILEPATH + 'conf.json', 'r'))
    CONSUMER_KEY = config_twitter['CONSUMER_KEY']
    CONSUMER_SECRET = config_twitter['CONSUMER_SECRET']
    USER_TOKEN = config_twitter['USER_TOKEN']
    USER_SECRET = config_twitter['USER_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(USER_TOKEN, USER_SECRET)
    #api = tweepy.API(auth)
    members_list = json.load(open('./twitter_ids.json','r'))
    print members_list
    listener = StdOutListener()
    stream = Stream(auth, listener)
    stream.filter(follow=members_list)
    print 'Done'
