import tweepy
import os
from dotenv import load_dotenv()

class Tweet:
    # Visit https://developer.twitter.com/en/apps/ to get your keys
    api_key = ""
    api_secret = ""
    access_token = ""
    access_secret = ""
    username = ""

    def __init__(self, username):
        self.username = username

    def fetch(self, max):      
        # Twitter only allows access to a users most recent 3240 tweets with this method
        
        # Authorize twitter, initialize tweepy
            auth = tweepy.OAuthHandler(api_key, api_secret)
            auth.set_access_token(access_token, access_secret)
            api = tweepy.API(auth)
        
        # Initialize a list to hold all the tweepy Tweets
            alltweets = []
        
        # Remove '@' sign if present
        if(screen_name[0] == "@"):
                screen_name = screen_name[1:]
        # Make initial request for most recent tweets (200 is the maximum allowed count)
            new_tweets = api.user_timeline(screen_name, count=200)
        
        # Save most recent tweets
            alltweets.extend(new_tweets)
        
        # Save the id of the oldest tweet
            oldest = alltweets[-1].id - 1
        
        # Keep fetching tweets until there are no tweets left to grab or until we reach 3240 tweets
        whilelen(new_tweets) > 0:
        # print("\tFetching tweets before %s" % (oldest))

        # All subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name, count=200, max_id=oldest)

        # Save most recent tweets
                alltweets.extend(new_tweets)
        
        # Update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

        print("\t...%s tweets downloaded so far" % (len(alltweets)))
        
        # Transform the tweepy tweets into a 2D array that will populate the csv
        # To-do: fix missing keys error !if retweet
        # outtweets = [[tweet.id, tweet.created_at, emoji.demojize(tweet.text), tweet.text, tweet.source, tweet.retweet_count, tweet.favorite_count, tweet.retweeted, tweet.retweeted_status.user.screen_name, tweet.retweeted_status.user.id, tweet.retweeted_status.id, tweet.lang, "" ] for tweet in alltweets]
            outtweets = [[tweet.id_str, tweet.created_at, emoji.demojize(tweet.text), tweet.text, tweet.source, tweet.retweet_count, tweet.favorite_count, tweet.retweeted, tweet.user.id, tweet.user.name, tweet.user.screen_name, tweet.user.description, tweet.lang,""]for tweet in alltweets]



    def save(self, tweets):
        # Save tweets
