################################################################################
#
# Here we define a class that can be used to iterate through a persons last 3200
# tweets. We use that to get all tweets so that they can be stored in our
# database.
#
# The amount of tweets gotten per iteration depends on the RUNTIME_CONFIG dict
# in the config.py file.
#
# Based off of the following file: https://gist.github.com/yanofsky/5436496
#
# Author: P Talbot
#
################################################################################

import tweepy

from src import config


class Twitterator:

    # This constructor is not necessary for our program to run correctly.
    # However, we do this for readability so we know all of the fields.
    def __init__(self):
        self.api        = None
        self.first      = None      # First iteration is treated differently.
        self.handle     = None
        self.size       = None

    # Actually initialize all variables here, only when the iterator is needed.
    def __iter__(self):
        self.set_api()
        self.first = True
        self.handle = config.RUNTIME_CONFIG['twitter-handle']
        self.size = config.RUNTIME_CONFIG['tweets-per-iter']
        return self

    def __next__(self):
        if self.first is True:
            new_tweets = self.api.user_timeline(screen_name=self.handle,
                                                count=self.size)

            # No longer on first iteration so we set to False.
            self.first = False
        else:
            new_tweets = self.api.user_timeline(screen_name=self.handle,
                                                count=self.size,
                                                max_id=self.oldest_id)

        if len(new_tweets) == 0:
            raise StopIteration

        # Update the oldest id, so that we can
        self.oldest_id = new_tweets[-1].id - 1

        return new_tweets

    # Set the API using the Tweepy and OAuth given by a Twitter Apps
    def set_api(self):
        auth = tweepy.OAuthHandler(config.TWITTER_API_CONFIG['key'],
                                   config.TWITTER_API_CONFIG['key-secret'])
        auth.set_access_token(config.TWITTER_API_CONFIG['access-token'],
                              config.TWITTER_API_CONFIG['access-token-secret'])
        self.api = tweepy.API(auth)
        return None
