from Configurations import BEARER_TOEKN_POLSCI_PROJECT
from twarc import Twarc2, expansions

import json
import pytz
import datetime

"""
Tweets from 5 media outlets: GMA, ABSCBN, Phil Inquirer, Rappler, Yahoo News
Duration: Oct 12 to May 7, 2016

List of Media Outlets   
    1. GMA Network Online   
    2. ABS-CBN News Online  
    3. Philippine Daily Inquirer Online     
    4. Rappler  
    5. Yahoo! News  

List of 2016 Presidential Candidate (Refer to email regarding the keywords per candidate)
    1. Jejomar Binay (United Nationalist Alliance)  @VPJojoBinay
    2. Miriam Defensor-Santiago (Nacionalista Party)    @senmiriam
    3. Rodrigo Duterte (PDP-Laban)  @RRD_Davao
    4. Grace Poe (Independent)  @SenGracePOE
    5. Mar Roxas (Liberal Party)    @MARoxas

2016 National Elections Campaign Period     October 12, 2015 to May 7, 2016

Data to extract: Text, Date, Userhandle (who it came from), 
specify which candidate is being talked about
Repeated content still needed, sentiment, language 
"""

# Keyword searches
SEARCH_KEYWORDS = [
	"@VPJojoBinay",
	"Binay",
	"Vice President Binay",
	"VP Binay",
	"Jojo Binay",
	"Jejomar Binay",
	"@senmiriam",
	"MDS",
	"Miriam",
	"Senator Miriam",
	"Sen Miriam",
	"Santiago",
	"Defensor-Santiago",
	"Miriam Defensor-Santiago",
	"@RRD_Davao",
	"Duterte",
	"Mayor Duterte",
	"Rodrigo Duterte",
	"Mayor Duterte",
	"@SenGracePOE",
	"Grace Poe ",
	"Poe",
	"Senator Poe",
	"@MARoxas",
	"Mar",
	"Mar Roxas",
	"Senator Roxas",
	"Sen Mar",
	"#Eleksyon2016",
	"#Halalan2016",
	"#VotePH2016",
	"#PHVote"
]
KEYWORD_QUERY = "("
for keyword in SEARCH_KEYWORDS[:-1]:
	KEYWORD_QUERY = KEYWORD_QUERY + '"' +  keyword + '"' +  " OR "
KEYWORD_QUERY = KEYWORD_QUERY + SEARCH_KEYWORDS[-1] + ")"

# Current account to search
ACCOUNTS = [
	#"gmanews",
	#"ABSCBNNews",
	"inquirerdotnet",
	"rapplerdotcom",
	"YahooPH"
]

OUTPUT_FILE_NAME = "raw_tweet_dump.jsonl"

# Client information
client = Twarc2(bearer_token=BEARER_TOEKN_POLSCI_PROJECT)

def main():
	# Prints when the program starts
	print("Time script started:", datetime.datetime.now())

	# Start: first microsecond of October 12, 2015 UTC+8
	start_time = datetime.datetime(2015, 10, 12, 0, 0, 0, 0, pytz.timezone("Asia/Manila"))
	# End: last microsecond of May 7, 2016 UTC+8
	end_time = datetime.datetime(2016, 5, 7, 23, 59, 59, 59, pytz.timezone("Asia/Manila"))

	for account in ACCOUNTS:
		# Search for non-retweet tweets from the selected Twitter account using the keyword query
		full_query = KEYWORD_QUERY + " from:" + account + " -is:retweet"

		# Ready the client using the specified attributes
		search_results = client.search_all(
			query=full_query, 
			start_time=start_time, 
			end_time=end_time, 
			max_results=100)

		# Writes the results to a JSONL file for later processing
		for page in search_results:
			result = expansions.flatten(page)
			with open(OUTPUT_FILE_NAME, "a+" ) as f:
				for tweet in result:
					f.write(json.dumps(tweet) + "\n")

if __name__ == "__main__":
    main()