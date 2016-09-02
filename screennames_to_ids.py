import tweepy,json
def get_ids(candidates):
    ids = []
    for screen_name in candidates:
        print ' - %s' % screen_name
        try:
            user = api.get_user(screen_name.strip())
            ids.append(user.id_str)
        except:
            print 'Error recovering the id'
    return ids
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
basque_candidates = json.load(open('basque_elections.json', 'r'))
galician_candidates = json.load(open('galician_elections.json','r'))
basque_ids = get_ids(basque_candidates)
galician_ids = get_ids(galician_candidates)
with open('basque_ids.json', 'w') as outfile:
    json.dump(basque_ids, outfile)
with open('galician_ids.json', 'w') as outfile:
    json.dump(galician_ids, outfile)
print 'The end.'
