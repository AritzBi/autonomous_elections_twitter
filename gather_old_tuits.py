import tweepy, json, gzip, time, sys
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
members_list = json.load(open('./basque_ids.json','r'))
loops = 2
WAIT_MINS = 5
for id_str in members_list:
    print 'Checking the timeline of %s' % (id_str)
    new_tweets = []
    i = 0
    repeat = True
    while repeat:
        try:
            for i in range(loops):
                if len(new_tweets) > 0:
                    new_tweets.extend(api.user_timeline(user_id=id_str, max_id=new_tweets[-1].id_str, count=200))
                else:
                    new_tweets.extend(api.user_timeline(user_id=id_str, count=200))
            repeat = False
        except tweepy.error.TweepError as e:
            repeat = True
            print '(%s) Time limit exceeded. Waiting %s mins' % (time.ctime(), WAIT_MINS)
            print '\t', e
            sys.stdout.flush()
            try:
                if e.args[0][0]['code'] == 88:
                    print i
                    i -= 1
                    time.sleep(WAIT_MINS * 60)
                else:
                    repeat = False
            except:
                repeat = False
    print '%s tweets have been recovered from %s timeline' % (len(new_tweets), id_str)
    print len(new_tweets)
    file_name = './corpus_new/tweets-%s.txt.gz' % (id_str)
    print 'Writing file:', file_name
    with gzip.open(file_name, 'w') as f:
        for tweet in new_tweets:
            f.write(json.dumps(tweet._json) + '\n')
    print 'Writing finished'
