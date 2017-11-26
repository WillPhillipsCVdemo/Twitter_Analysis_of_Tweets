import tweepy
# assuming twitter_authentication.py contains each of the 4 oauth elements (1 per line)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from textblob import TextBlob


consumer_key ='Your consumer key'
consumer_secret = 'Your consumer secret'

access_token ='your access token'
access_token_secret = 'your token secret'


def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'


def get_pie_chart(positive, negative, neutral):
    # Data to plot
    labels = 'Positve', 'Negative', 'Neutral'
    sizes = [positive, negative, neutral]
    colors = ['Green', 'Red', 'lightskyblue']
    patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    #plt.savefig(str(search_term)+'_chart.png')
    #plt.show()

    fig = plt.figure()
    plt.plot(range(10))
    fig.savefig(str(search_term)+'_chart.png', dpi=fig.dpi)


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True)

search_term = input('Please enter a term to search for; ')
print("Searching for {}, stand by ........................".format(search_term))
max_tweets = 10000
searched_tweets = [status for status in tweepy.Cursor(api.search, q=("#"+str(search_term))).items(max_tweets)]


searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=("#"+str(search_term)), count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

print("Number of tweets extracted: {}.\n".format(len(searched_tweets)))
# We print the most recent 5 tweets:
print('\n')
print("5 recent tweets:\n")
for tweet in searched_tweets[:5]:
    print(tweet.text)
    print('\n')


data1=[tweet.text for tweet in searched_tweets]


data = pd.DataFrame(data1, columns=['Tweets'])

###Write to Text file
thefile = open(str(search_term)+'_tweets.txt', 'w')

for tweet_text in data1:
  thefile.write("%s\n" % tweet_text)

# We add relevant data:
data['len']  = np.array([len(tweet.text) for tweet in searched_tweets])
data['ID']   = np.array([tweet.id for tweet in searched_tweets])
data['Username'] = np.array([tweet.user.screen_name for tweet in searched_tweets])
data['Date'] = np.array([tweet.created_at for tweet in searched_tweets])
data['Source'] = np.array([tweet.source for tweet in searched_tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in searched_tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in searched_tweets])
data['sentiment'] = np.array([get_tweet_sentiment(tweet.text) for tweet in searched_tweets])


#############################################################
###Positive and Negative Tweets

# picking positive tweets from tweets
ptweets = [tweet for tweet in searched_tweets if get_tweet_sentiment(tweet.text) == 'positive']
# percentage of positive tweets
print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(searched_tweets)))
# picking negative tweets from tweets
ntweets = [tweet for tweet in searched_tweets if get_tweet_sentiment(tweet.text) == 'negative']
# percentage of negative tweets
print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(searched_tweets)))
# percentage of neutral tweets
neutral_tweets = (100 * (len(searched_tweets) - len(ntweets) - len(ptweets) ) / len(searched_tweets))
print("Neutral tweets percentage: {} % ".format(neutral_tweets))


#Open new data file
f = open(str(search_term)+"_data.txt", "w")
f.write(str(100 * len(ptweets) / len(searched_tweets))+'\n')     # str() converts to string
f.write(str(100 * len(ntweets) / len(searched_tweets))+'\n')
f.write(str(neutral_tweets)+'\n')
f.close()




data.to_csv(str(search_term)+'_Tweets.csv')
#print(type(searched_tweets))