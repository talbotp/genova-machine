# genova-machine #

Here, we create a tool that can be used to scrape the last 3200 tweets created 
by a single user, which will then be stored in a MySQL database. We will then 
perform machine learning techniques to generate tweets that have a high
similarity score to those in the database.

## Usage ##

The file which is used to drive this program is genova_machine.py. In order for 
this to run correctly, you must follow the instructions in config.py to set up 
your local MySQL database credentials and Twitter API OAuth and Access Tokens.

We must run the following:

    pip3 install mysql-connector
    
    pip3 install tweepy

Finally, we run the driver for the program using the following.

    python3 genova_machine.py
