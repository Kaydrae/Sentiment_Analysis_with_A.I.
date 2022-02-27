# Expectations:
# You get the approval to proceed to make a proof of concept AI sentiment analysis program.
#
# Use Python 3x.
# Create a twitter account if you do not have one.
# Create a AI sentiment analysis program that will go through 100 tweets on a hard coded subject of your choice and mark the intent as positive or negative.
# Create a header explaining what this program is and what it does and how to use it.
# Create a UI for a user.
# Prove that it is working by taking a screen shot of a the output.
# Create a readme.txt file with meta data about your program.
# Place your finished code in github.
# Take a screen shot of your files / code in github.
# Deliverables:
# Submit the output screenshot  of github for this assignment.
# Submit the zipped python project for this assignment.
# Submit the readme.txt file for this assignment
# Submit a video of all functionality and code review.  Live video of you running this.
import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'UYURRkoPhc2FUD3aDL81s2pL2'
        consumer_secret = 'F6zPnMrcjUHenaZebZoS6gfTl7fApJb3O4hNOstdR17NeCTZ4h'
        access_token = '1497097734033055751-BRQJXFFbM0S49s2og89aDQAN2zvGfL'
        access_token_secret = 'MRNxGsdDFh8nnE1GcQAcIdSZgmhUGK4HIaRDAFcJQLBeV'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.errors.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))



def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get  for the topic of space
    tweets = api.get_tweets(query='Space', count=100)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets: {} %".format(100 * len(ptweets) / len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets: {} %".format(100 * len(ntweets) / len(tweets)))
    # percentage of neutral tweets
    print("Neutral tweets: {} % \
        ".format(100 * (len(tweets) - (len(ntweets) + len(ptweets))) / len(tweets)))
    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

if __name__ == "__main__":
    print("Welcome to the Tweet extractor for the topic of space.\n")
    print("Here I will be breaking down the positive, negative, and neutral tweets by percentage.\n ")
    # calling main function
    main()