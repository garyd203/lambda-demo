from garys_auth import get_garys_twitter_auth
from twitter import *
import json


def harvest(event, context):
    t = Twitter(auth=get_garys_twitter_auth())

    #TODO or refactor to perform the request dynamically, with a cache on dynamo?

    # NB: From https://dev.twitter.com/rest/public/search...
    # "The Search API is not complete index of all Tweets, but instead an
    #  index of recent Tweets. The index includes between 6-9 days of
    #  Tweets".
    #
    # If you care, use the streaming API instead :-)
    response = t.search.tweets(q='#sypy', result_type='recent', since_id=0)
    for tweet in response['statuses']:
        print tweet['text']
        print tweet['user']['screen_name']
        # Save in Dynamo
    # Store max_id in dynamo as new since_id

    return "Go SyPy"


def user_tally(event, context):
    t = Twitter(auth=get_garys_twitter_auth())
    response = t.search.tweets(q='#sypy', result_type='recent', since_id=0)

    for tweet in response['statuses']:
        print "@" + tweet['user']['screen_name'] + ": " + tweet['text']

    tallies = {}
    messages = []
    for tweet in response['statuses']:
        username = tweet['user']['screen_name']
        tallies[username] = tallies.get(username, 0) + 1

        messages.append(tweet['text'])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "messages": messages,
            "tweets": tallies,
        }),
    }


if __name__ == '__main__':
    print user_tally({}, {})