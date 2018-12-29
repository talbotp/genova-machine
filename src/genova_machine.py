################################################################################
#
# This file is used for scraping the most recent 3200 tweets from a user and for
# them to be stored in a MySQL database. Next, we will perform LSTM methods on
# them to create tweets with a high similarity to the scraped tweets.
#
#   Useful Links:
#   1)  https://tweepy.readthedocs.io/en/v3.5.0/index.html
#   2)  https://www.w3schools.com/python/python_mysql_getstarted.asp
#
# Author: P Talbot
#
################################################################################

from src.twitterator import Twitterator
from src.database_wrapper import DatabaseWrapper


# Get Database Connection.
db = DatabaseWrapper()

# Get Twitter iterator, to populate our database.
tw_iter = iter(Twitterator())

# At each iteration in the loop. We add the tweets to our database.
for tweets in tw_iter:
    for tweet in tweets:
        print(tweet.text.encode('utf-8'))
    db.insert_many_records(tweets)
