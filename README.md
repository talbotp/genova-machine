# genova-machine #

Here, we will perform LSTM on the most recent 3200 tweets from a single user (3200 is max set by Twitter API), in order to generate text with a high similarity to the data provided.

## Idea ## 

We will scrape users Instagram and Twitter and store their posts and captions in a database.
We will then perform LSTM methods on this data to generate new tweets.

## Technologies ##

* MySQL -> I havn't touched databases in a while so this could be useful for me.
* tweepy -> Python Twitter API https://github.com/tweepy/tweepy