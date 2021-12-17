from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import datetime
import json

FILE_NAME = "raw_tweet_dump.jsonl"

ANALYZER = SentimentIntensityAnalyzer()

KEYWORDS = {
	'binay': ["@VPJojoBinay", "Binay", "Vice President Binay", "VP Binay", "Jojo Binay", "Jejomar Binay"],
	'santiago': ["@senmiriam", "MDS", "Miriam", "Senator Miriam", "Sen Miriam", "Santiago", "Defensor-Santiago", "Miriam Defensor-Santiago"],
	'duterte': ["@RRD_Davao", "Duterte", "Mayor Duterte", "Rodrigo Duterte", "Mayor Duterte"],
	'poe': ["@SenGracePOE", "Grace Poe ", "Poe", "Senator Poe"],
	'roxas': ["@MARoxas", "Mar", "Mar Roxas", "Senator Roxas", "Sen Mar"],
	'general_hashtags': ["#Eleksyon2016", "#Halalan2016", "#VotePH2016", "#PHVote"]
}

def extract_usernme(entry):
	return dict(entry)['username']

def read_output_file(file_name=FILE_NAME):
	tweet_df = pd.read_json(path_or_buf=FILE_NAME, lines=True)
	
	tweet_df = tweet_df[['id', 'created_at', 'author', 'lang', 'text']]
	tweet_df['id'] = tweet_df['id'].astype(str)
	tweet_df['author'] = tweet_df['author'].apply(extract_usernme)
	tweet_df['created_at'] = tweet_df['created_at'].dt.tz_convert('Asia/Manila')
	tweet_df['created_at'] = tweet_df['created_at'].apply(lambda a: datetime.datetime.strftime(a, "%Y-%m-%d %H:%M:%S"))
	tweet_df.rename(columns={'created_at': 'created_at_utc+8', 'id': 'tweet_id', 'author': 'userhandle'}, inplace=True)

	return tweet_df

def extract_sentiment(tweet_df):
	tweet_df['vader_compound'] = [ANALYZER.polarity_scores(x)['compound'] for x in tweet_df['text']]
	tweet_df['vader_neg'] = [ANALYZER.polarity_scores(x)['neg'] for x in tweet_df['text']]
	tweet_df['vader_neu'] = [ANALYZER.polarity_scores(x)['neu'] for x in tweet_df['text']]
	tweet_df['vader_pos'] = [ANALYZER.polarity_scores(x)['pos'] for x in tweet_df['text']]
	
	return tweet_df

def check_if_present(entry, keywords):
	for keyword in keywords:
		if entry.contains(keyword):
			return true
	return false

def extract_keyword_information(tweet_df):
	tweet_df['binay'] = tweet_df['text'].str.contains('Mel')

	for category, keywords in KEYWORDS.items():
		tweet_df[category] = tweet_df['text'].str.contains("|".join(keywords))
	tweet_df['category_count'] = tweet_df[[key for key in KEYWORDS]].astype(int).sum(axis=1)

	return tweet_df

def write_df_to_excel(tweet_df, file_name='output.xlsx'):
	if file_name[-4:] == 'xlsx':
		writer = pd.ExcelWriter('tweets.xlsx')
		tweet_df.to_excel(writer, 'Sentiments', index=False)
		writer.save()
	else:
		raise ValueError('Error with file name (%s). Please ensure file name ends with xlsx' % file_name)

def main():
	write_df_to_excel(
		tweet_df=extract_keyword_information(extract_sentiment(read_output_file())),
		file_name='tweets.xlsx')

if __name__ == "__main__":
	main()