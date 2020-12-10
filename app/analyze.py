import re, string, random, csv, nltk, emoji
from nltk import FreqDist
from nltk import classify
from nltk.tag import pos_tag
from nltk.corpus import stopwords
from nltk import NaiveBayesClassifier
from nltk.corpus import twitter_samples
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer

# Download the sample tweets from the NLTK package - done only once
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.download('twitter_samples')
# nltk.download('averaged_perceptron_tagger')
class Analyze:

    tweets = None
    username = None
    scores = []
    clean_tokens_list = []
    classifier = None

    def __init__(self, user):
        self.username = user
        positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
        negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    def analyze(self):
        print("Starting engines 🏭\n")

        self.train()
        self.ReadTweets()
        self.parseTweets()
        self.aggregate()

    def aggregate(self):

        avg = sum(self.scores)/len(self.scores)
        res = ""
        if avg < 0:
            res = "a Pessimist"
        elif avg > 0:
            res = "an Optimist"
        else:
            res = "Neutral"
        print('-------------------------------------------------------')
        print(f'- The gods say @{self.username} is mostly {res} -'  )
        print('-------------------------------------------------------')
        return

    def get_tweets_for_model(self, cleaned_tokens_list):
        for tweet_tokens in cleaned_tokens_list:
            yield dict([token, True] for token in tweet_tokens)

    def get_all_words(self, cleaned_tokens_list):
        for tokens in self.clean_tokens_list:
            for token in tokens:
                yield token

    def remove_noise(self, tweet_tokens, stop_words = ()):
        cleaned_tokens = []

        for token, tag in pos_tag(tweet_tokens):
            token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
            # token = re.sub('https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*', '', token)
            token = re.sub("(@[A-Za-z0-9_]+)","", token)
            token = re.sub("RT", "", token)

            if tag.startswith("NN"):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'

            lemmatizer = WordNetLemmatizer()
            token = lemmatizer.lemmatize(token, pos)

            if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
                cleaned_tokens.append(token.lower())
        return cleaned_tokens

    def lemmatize_sentence(self, tokens):
        print("Normalizing data ...")
        lemmatizer = WordNetLemmatizer()
        lemmatized_sentence = []
        for word, tag in pos_tag(tokens):
            if tag.startswith('NN'):
                pos = 'n'
            elif tag.startswith('VB'):
                pos = 'v'
            else:
                pos = 'a'
            lemmatized_sentence.append(lemmatizer.lemmatize(word, pos))
        return lemmatized_sentence

    def analyzeTweet(self, text):
        tweet_tokens = self.remove_noise(word_tokenize(text))

        result = self.classifier.classify(dict([token, True] for token in tweet_tokens))
        return result
        # print("")
        # print("Tokenizing data ...")
        # tokenized_tweet = word_tokenize(text)
        # print(tokenized_tweet)
        # print("")
        # normalized_tokens = self.lemmatize_sentence(tokenized_tweet)
        # print(normalized_tokens)
        # print("")
        # cleaned_tokens = self.remove_noise(normalized_tokens, stopwords.words('english'))
        # self.clean_tokens_list.append(cleaned_tokens)
        # print(cleaned_tokens)
        # print("")
        # all_tweet_words = self.get_all_words(cleaned_tokens)
        # freq_dist_pos = FreqDist(all_tweet_words)
        # print("Most common")
        # print(freq_dist_pos.most_common(20))

    def parseTweets(self):
        tweets = self.tweets
        if(len(tweets) < 1):
            print('Empty tweets array')
            return

        for tweet in tweets:
            if(tweet[0:2].lower() == "b'" or tweet[0:2] == "b\""):
                tweet = tweet[2:len(tweet) - 1]

            result = self.analyzeTweet(tweet)

            if(result == 'Positive'):
                self.scores.append(1)
            elif result == "Negative":
                self.scores.append(-1)
            else:
                self.scores.append(0)
        print("\nCalculating score🥁🥁🥁\n")
        return

    def ReadTweets(self):
        print("\n\n----------------------------")
        print("-------Analyzing data-------")
        print("----------------------------\n")

        readTweets = []

        with open(f"tweets/{self.username}.csv") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 1:
                    line_count += 1
                    # if(int(csv_reader) > 1):
                    #     if(row[1] != ""):
                    #         readTweets.append(row[1])
                    continue
                else:
                    if(row[2] == 'en'):
                        readTweets.append(emoji.demojize(row[0]))
                    line_count += 1
            print(f'Processed {line_count} tweets.')

        self.tweets = readTweets
        return

    def train(self):
        print("----------------------------")
        print("-------Training Model-------")
        print("----------------------------\n")

        print('Gathering data...')
        positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
        negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

        positive_cleaned_tokens_list = []
        negative_cleaned_tokens_list = []

        print("Removing noise ...")
        for tokens in positive_tweet_tokens:
            positive_cleaned_tokens_list.append(self.remove_noise(tokens, stopwords.words('english')))
        for tokens in negative_tweet_tokens:
            negative_cleaned_tokens_list.append(self.remove_noise(tokens, stopwords.words('english')))

        positive_tokens_for_model = self.get_tweets_for_model(positive_cleaned_tokens_list)
        negative_tokens_for_model = self.get_tweets_for_model(negative_cleaned_tokens_list)

        print('Creating test/split datasets')
        positive_dataset = [(tweet_dict, "Positive") for tweet_dict in positive_tokens_for_model]

        negative_dataset = [(tweet_dict, "Negative") for tweet_dict in negative_tokens_for_model]

        dataset = positive_dataset + negative_dataset

        random.shuffle(dataset)

        train_data = dataset[:7000]
        test_data = dataset[7000:]

        print("Lift off🚀")
        self.classifier = NaiveBayesClassifier.train(train_data)

        print("Traing complete. Accuracy:", classify.accuracy(self.classifier, test_data))

        print(self.classifier.show_most_informative_features(10))

        return
