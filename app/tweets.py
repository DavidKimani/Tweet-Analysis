import tweepy # https://github.com/tweepy/tweepy
from dotenv import load_dotenv
import os
import csv
import json
load_dotenv()
class Tweet:
    # Visit https://developer.twitter.com/en/apps/ to get your keys
    api_key = ""
    api_secret = ""
    access_token = ""
    access_secret = ""
    username = ''
    tweets = None

    def __init__(self, username):
        if username == "":
            print('Supply a correct username')
        else:
            self.api_key = os.getenv("api_key")
            self.api_secret = os.getenv("api_secret")
            self.access_token = os.getenv("access_token")
            self.access_secret = os.getenv("access_secret")
            self.username = username

    def fetch(self):
        print(f"Summoning @{self.username}'s tweets... 🔮🧙‍♂️")
        # Twitter only allows access to a users most recent 3240 tweets with this method

        # Authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)
        auth.set_access_token(self.access_token, self.access_secret)
        api = tweepy.API(auth)

        # Initialize a list to hold all the tweepy Tweets
        alltweets = []

        # Remove '@' sign if present
        if(self.username[0] == "@"):
            self.username = self.username[1:]

        # Make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(self.username, count=200)

        # Save most recent tweets
        alltweets.extend(new_tweets)

        # Save the id of the oldest tweet
        oldest = alltweets[-1].id - 1

        # Keep fetching tweets until there are no tweets left to grab or until we reach 3240 tweets
        while len(new_tweets) > 0:
            # print("\tFetching tweets before %s" % (oldest))

            # All subsequent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(self.username, count=200, max_id=oldest)

            # Save most recent tweets
            alltweets.extend(new_tweets)

            # Update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1

            print("\t...%s tweets downloaded so far" % (len(alltweets)))

        self.tweets = alltweets

        print("Done.\n")
        return self.processTweets()

    def processTweets(self):
        print('Processing tweets...')

        # Transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.text, tweet.user.description, tweet.lang ] for tweet in self.tweets]

        print(f"\tSaving @{self.username}'s\n")

        with open(f"tweets/{self.username}.csv", 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)

            # Write CSV Header
            writer.writerow(["tweet", "bio", "language"])

            # Populate CSV with tweets
            writer.writerows(outtweets)
        print("Done!")