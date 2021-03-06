from __future__ import print_function
import argparse
from twitter.stream import TwitterStream, Timeout, HeartbeatTimeout, Hangup
from twitter.oauth import OAuth
from twitter.util import printNicely
from logging import Formatter, FileHandler, getLogger, ERROR
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from rethinkdb import now
from passlib.hash import sha256_crypt
import json
import os, sys
sys.path.append(os.path.abspath(''))
import helpers.rethinkdb as db
from config import DATABASE, TWEETS_TABLE


def get_log(name):
    logger = getLogger('Stream')
    logger.setLevel(ERROR)
    file_handler = FileHandler('var/logs/stream.log')
    file_handler.setFormatter(Formatter("%(asctime)-15s %(name)s [%(levelname)s] - %(message)s"))
    logger.addHandler(file_handler)
    return logger

log = get_log(__name__)


def parse_arguments():

    parser = argparse.ArgumentParser(description=__doc__ or "")

    parser.add_argument('-t',  '--token', required=True, help='The Twitter Access Token.')
    parser.add_argument('-ts', '--token-secret', required=True, help='The Twitter Access Token Secret.')
    parser.add_argument('-ck', '--consumer-key', required=True, help='The Twitter Consumer Key.')
    parser.add_argument('-cs', '--consumer-secret', required=True, help='The Twitter Consumer Secret.')
    parser.add_argument('-us', '--user-stream', action='store_true', help='Connect to the user stream endpoint.')
    parser.add_argument('-ss', '--site-stream', action='store_true', help='Connect to the site stream endpoint.')
    parser.add_argument('-to', '--timeout', help='Timeout for the stream (seconds).')
    parser.add_argument('-ht', '--heartbeat-timeout', help='Set heartbeat timeout.', default=90)
    parser.add_argument('-nb', '--no-block', action='store_true', help='Set stream to non-blocking.')
    parser.add_argument('-tt', '--track-keywords', help='Search the stream for specific text.')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # When using twitter stream you must authorize.
    auth = OAuth(args.token, args.token_secret, args.consumer_key, args.consumer_secret)

    # These arguments are optional:
    stream_args = dict(
        timeout=args.timeout,
        block=not args.no_block,
        heartbeat_timeout=args.heartbeat_timeout)

    query_args = dict()
    if args.track_keywords:
        query_args['track'] = args.track_keywords

    if args.user_stream:
        stream = TwitterStream(auth=auth, domain='userstream.twitter.com', **stream_args)
        tweet_iter = stream.user(**query_args)
    elif args.site_stream:
        stream = TwitterStream(auth=auth, domain='sitestream.twitter.com', **stream_args)
        tweet_iter = stream.site(**query_args)
    else:
        stream = TwitterStream(auth=auth, **stream_args)
        if args.track_keywords:
            tweet_iter = stream.statuses.filter(**query_args)
        else:
            tweet_iter = stream.statuses.sample()

    # Connect to RethinkDB
    try:
        db.connect()
    except RqlDriverError:
        log.error('Couldn\'t connect to database.')

    # Iterate over the sample stream.
    for tweet in tweet_iter:
        # You must test that your tweet has text. It might be a delete or data message.
        if tweet is None:
            log.error('None')
        elif tweet is Timeout:
            log.error('Timeout')
        elif tweet is HeartbeatTimeout:
            log.error('Heartbeat Timeout')
        elif tweet is Hangup:
            log.error('Hangup')
        elif tweet.get('text'):
            tweet['stream_id'] = '1234567890'  # TODO: add that stream_id gets passed to open_stream.py
            db.insert(DATABASE, TWEETS_TABLE, tweet)
            printNicely(tweet['text'])
        else:
            log.error('Some data ' + str(tweet))


if __name__ == '__main__':
    main()
