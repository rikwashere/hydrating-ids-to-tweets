# -*- coding: utf-8 -*-

from twython import Twython, TwythonAuthError, TwythonRateLimitError
from config import get_keys
import os.path
import pickle
import time
import json
import sys

APP_KEY, APP_SECRET = get_keys()

def loadIds(f):
    ids = []
    print '\nLoading IDs from %s...' % f
    pickled_f = f + '.p'
    json_f = f + '-hydrated.json'
    if not os.path.isfile(pickled_f):
        with open(f, 'r') as twiqs:
            for tweet_id in twiqs:
                ids.append(tweet_id.split()[1])
        ids = ids[1:]
        print '* Loaded %i ids from %s.' % (len(ids), f)
        print '\nCreating pickled list...'
        with open(pickled_f, 'wb') as pickle_out:
            pickle.dump(ids, pickle_out)
        print '* Dumped %i ids to %s.' % (len(ids) - 1, pickled_f)
    else:
        print '* Found pickled list. Loading...'
        with open(pickled_f, 'rb') as pickle_in:
            ids = pickle.load(pickle_in)
        print '* Loaded %i ids from %s.' % (len(ids), pickle_in)
        if os.path.isfile(json_f):
            print '* Found existing output file:', json_f
            loaded_ids = []
            with open(json_f, 'r') as json_tweet:
                print '\nComparing input/output...'
                for json_obj in json_tweet:
                    tweet = json.loads(json_obj)
                    loaded_ids.append(tweet['id_str'])
                print '* Already hydrated %i tweets.' % len(loaded_ids)
                
        else:
            print '* No existing output exists yet.'
        time.sleep(5.0)
    return ids

def hydrate(request):
	try:
		tweet_json = twitter.lookup_status(id=request, map=False)
	except TwythonRateLimitError:
		time.sleep(5)
		return
	    
	if tweet_json:
            if type(tweet_json) == list:
                return tweet_json[0]
            else:
                return tweet_json
        else:
            return request

def remove_tweet_id(tweet_id_list, f):
    print '\nUpdating source files...'
    pickled_f = f + '.p'
    with open(pickled_f, 'rb') as pickle_in:
        p_tweet_id_list = pickle.load(pickle_in)
    for tweet_id in tweet_id_list:
        if tweet_id in p_tweet_id_list:
            p_tweet_id_list.remove(tweet_id)
    print '* Removed %i IDs from tweet ID list.' % len(tweet_id_list)
    print '* %i tweet IDs remaining in source.' % len(p_tweet_id_list)
    with open(pickled_f, 'wb') as pickle_out:
        print '* Storing pickled file at:', pickle_out
        pickle.dump(p_tweet_id_list, pickle_out)
    
    
if __name__ == "__main__":
    t0 = time.time()
    files = ['yourfilesgohere']
    print '\nAuthorizing with Twitter...'
    # building Twitter client
    twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
    ACCESS_TOKEN = twitter.obtain_access_token()
    try:
        twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
        print '* Cleared!'
    except TwythonAuthError:
        sys.exit("Authorization failed.")
    for f in files:
        ids = loadIds(f)
        json_f = f + '-hydrated.json'
        removals = []
        for tweet_id in ids:
            t1 = time.time()
            print '\nHydrating tweet %i/%i.' % (ids.index(tweet_id), len(ids))
            tweet_json = hydrate(tweet_id)
            if tweet_json == tweet_id:
                removals.append(tweet_id)
                with open('error.log', 'a') as errors:
                    errors.write(tweet_id)
                    errors.write('\n')
            else:
                removals.append(tweet_json['id_str'])
                with open(json_f, 'a') as json_out:
                    json.dump(tweet_json, json_out)
                    json_out.write('\n')
            print 'Hydrating took %.2f seconds.' % (time.time() - t1)
            print 'Total time elapsed: %.2f seconds.' % (time.time() - t0)
            if len(removals) > 999:
                remove_tweet_id(removals, f)
                removals = []

