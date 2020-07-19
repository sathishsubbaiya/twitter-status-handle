# Local Import
import os

try:
    import requests
    import json
    import tweepy
except ImportError:
    os.system("pip install requests")
    os.system("pip install json")
    os.system("pip install tweepy")


quote_api_url = 'https://programming-quotes-api.herokuapp.com/quotes/random'
random_jokes_api = 'https://official-joke-api.appspot.com/jokes/random'


def create_api():
    auth = tweepy.OAuthHandler(os.getenv("CONSUMER_KEY"),
                               os.getenv("CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("ACCESS_TOKEN"),
                          os.getenv("ACCESS_TOKEN_SECRET"))
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print ("Error creating API")
        raise e
    print ("API created")
    return api


def get_random_quote():
    response = requests.get(quote_api_url)
    if response.status_code == 200:
        out_json = response.content
        dict_json = json.loads(out_json)
        random_quote = dict_json.get("en")
        author = dict_json.get("author")
        quote = random_quote + '\n- ' + author
        if len(quote) >= 280:
            get_random_quote()
        return quote


def get_random_joke():
    response = requests.get(random_jokes_api)
    if response.status_code == 200:
        out_json = response.content
        dict_json = json.loads(out_json)
        setup = dict_json.get("setup")
        punchline = dict_json.get("punchline")
        joke = setup + '\n' + punchline
        if len(joke) >= 280:
            get_random_joke()
        return joke


def joke_or_quote_tweet(option):
    joke_quote_dict = {
        'joke': 'get_random_joke()',
        'quote': 'get_random_quote()'
    }
    if option.lower() in joke_quote_dict.keys():
        return_val = eval(joke_quote_dict.get(option.lower()))
        return return_val


def update_tweet(twitter_api, tweet):
    # Create a tweet
    twitter_api.update_status(tweet)


if __name__ == '__main__':
    return_api = create_api()
    tweet_data = joke_or_quote_tweet('joke')                                    # Pass the argument(joke, quote) to be posted in twitter wall
    update_tweet(return_api, tweet_data)
