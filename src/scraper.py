import snscrape.modules.twitter as sntwitter
import pandas as pd

# TODO: this scraper is not working with likes

def scrape(id, debug = False):
    if(debug):
        return pd.read_json('thread.json')
    print("conversation_id:%s (filter:safe OR -filter:safe)" % id)
    tweets_list2 = []
    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper("conversation_id:%s (filter:safe OR -filter:safe)" % id).get_items()):
        tweets_list2.append([tweet.date, tweet.id, tweet.content, tweet.username])
        
    return pd.DataFrame(tweets_list2, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])
