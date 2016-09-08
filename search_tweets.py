#for tweet in tweepy.Cursor(api.search,q=user, since='2016-09-02',until='2016-09-09').items():
import tweepy,json, time
print 'Starting...'
CONFIG_FILEPATH = './conf/'
config_twitter = json.load(open(CONFIG_FILEPATH + 'conf.json', 'r'))
CONSUMER_KEY = config_twitter['CONSUMER_KEY']
CONSUMER_SECRET = config_twitter['CONSUMER_SECRET']
USER_TOKEN = config_twitter['USER_TOKEN']
USER_SECRET = config_twitter['USER_SECRET']
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(USER_TOKEN, USER_SECRET)
api = tweepy.API(auth)
users = json.load(open('basque_elections.json','r'))
print users
max_tweets = 5000
for user in users:
    searched_tweets = []
    last_id = -1
    while len(searched_tweets) < max_tweets:
        count = max_tweets - len(searched_tweets)
        try:
            new_tweets = api.search(q=user, count=count, since_id=str(last_id - 1))
            if not new_tweets:
                break
            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id
            print "asda"
        except tweepy.TweepError as e:
            print "Limit..."
            time.sleep(15 * 60)
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            break
    file_name = './corpus_new/tweets' + user + '.txt.gz'
    print 'Writing file:', file_name
    with gzip.open(file_name, 'w') as f:
        for tweet in tweets:
            f.write(json.dumps(tweet) + '\n')
    print 'Writing finished'
