
# coding: utf-8

# In[136]:


import pandas as pd
import numpy as np
import requests
import tweepy
import json
import re
import matplotlib.pyplot as plt
import warnings
import os
import time


# #Gather Data

# In[137]:


# Read in csv file as a Pandas DataFrame
df = pd.read_csv("twitter-archive-enhanced.csv")
df.head(2)


# In[138]:


# Programmatically download the dog image prediction files from 
# the Udacity server using Request library

url="https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv"
response = requests.get(url)

with open('image_predictions.tsv', 'wb') as file:
    file.write(response.content)



# In[60]:


# Read in tsv file as a Pandas DataFrame    
img_pred = pd.read_csv('image_predictions.tsv', sep='\t')


# In[ ]:


import tweepy
from tweepy import OAuthHandler
import json
from timeit import default_timer as timer

# Query Twitter API for each tweet in the Twitter archive and save JSON in a text file
# Instructions for registering Twitter app and generating access tokens:
# https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/
# These are hidden to comply with Twitter's API terms and conditions
consumer_key = 'HIDDEN'
consumer_secret = 'HIDDEN'
access_token = 'HIDDEN'
access_secret = 'HIDDEN'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

# NOTE TO STUDENT WITH MOBILE VERIFICATION ISSUES:
# df_1 is a DataFrame with the twitter_archive_enhanced.csv file. You may have to
# change line 17 to match the name of your DataFrame with twitter_archive_enhanced.csv
# NOTE TO REVIEWER: this student had mobile verification issues so the following
# Twitter API code was sent to this student from a Udacity instructor
# Tweet IDs for which to gather additional data via Twitter's API
tweet_ids = df.tweet_id.values
len(tweet_ids)

# Query Twitter's API for JSON data for each tweet ID in the Twitter archive
count = 0
fails_dict = {}
start = timer()
# Save each tweet's returned JSON as a new line in a .txt file
with open('tweet_json.txt', 'w') as outfile:
    # This loop will likely take 20-30 minutes to run because of Twitter's rate limit
    for tweet_id in tweet_ids:
        count += 1
        print(str(count) + ": " + str(tweet_id))        
        try:
            tweet = api.get_status(tweet_id, tweet_mode='extended')
            print("Success")
            json.dump(tweet._json, outfile)
            outfile.write('\n')
        except tweepy.TweepError as e:
            print("Fail")
            fails_dict[tweet_id] = e
            pass
end = timer()
print(end - astart) 
print(fails_dict)


# In[139]:


#For loop to append each tweet into a list
tweets_data = []

tweet_file = open('tweet_json.txt', "r")

for line in tweet_file:
    try:
        tweet = json.loads(line)
        tweets_data.append(tweet)
    except:
        continue
        
tweet_file.close()


# In[140]:


# Create tweet_info DataFrame
tweet_info = pd.DataFrame()


# In[141]:


# Add selected variables to tweet_info DataFrame
tweet_info['id'] = list(map(lambda tweet: tweet['id'], tweets_data))
tweet_info['retweet_count'] = list(map(lambda tweet: tweet['retweet_count'], tweets_data))
tweet_info['favorite_count'] = list(map(lambda tweet: tweet['favorite_count'], tweets_data))


# Assess

# Visual Assessment
# Visual assessment was done by  opening csv files in Calc (Libre Office)

#  Programmatic Assessment

# In[142]:


# first 5 rows of df DataFrame
df.head()


# In[143]:


df.info()


# In[144]:


# View descriptive statistics of df DataFrame
df.describe()


# In[145]:


# View first 5 rows of image_predictions DataFrame
img_pred.head()


# In[146]:


# View info of image_predictions DataFrame
img_pred.info()


# In[147]:


# View descriptive statistics of image_predictions DataFrame
img_pred.describe()


# In[148]:


# View first 5 rows of tweet_info DataFrame
tweet_info.head()


# In[149]:


# View info of tweet_info DataFrame
tweet_info.info()


# In[150]:


# View descriptive statistics of tweet_info DataFrame# View d 
tweet_info.describe()


#  Quality Issues
#      Faulty names
#      Dataset contains retweets
#      Tweets with no images
#      Contents of 'text' cutoff
#      Incorrect dog names
#      Missing values in 'name' and dog stages showing as 'None'
#      Rating numerators with decimals not showing full float
#      Tweet with more than one #/# sometimes have the first occurence erroneously used for the rating numerators and                   denominators
#      Tweet ID 810984652412424192 doesn't contain a rating
#      Difficult to read sources
#      incorrect datatypes (timestamp, source, dog stages, tweet_id, in_reply_to_status_id,      in_reply_to_user_id)
# 

#  Tidness Issue
#     Dog "stage" variable in four columns: doggo, floofer, pupper, puppo
#     Merge 'tweet_info' and 'img_pred' to 'df'

# clean

# In[151]:


# Creating copies of original DataFrames
df_clean = df.copy()
img_pred_clean = img_pred.copy()
tweet_info_clean = tweet_info.copy()


#  Define
#  There are some faulty names in daat set

# In[152]:


# code
# replacing faulty names with None value or corrected Name
df_clean['name'].replace('the', 'None', inplace=True)
df_clean['name'].replace("light",'None', inplace=True)
df_clean['name'].replace("life",'None', inplace=True)
df_clean['name'].replace("an",'None', inplace=True)
df_clean['name'].replace("a",'None', inplace=True)
df_clean['name'].replace("by",'None', inplace=True)
df_clean['name'].replace("actually",'None', inplace=True)
df_clean['name'].replace("just",'None', inplace=True)
df_clean['name'].replace("getting",'None', inplace=True) 
df_clean['name'].replace("infuriating",'None', inplace=True) 
df_clean['name'].replace("old",'None', inplace=True) 
df_clean['name'].replace("all",'None', inplace=True) 
df_clean['name'].replace("this",'None', inplace=True) 
df_clean['name'].replace("very",'None', inplace=True) 
df_clean['name'].replace("mad",'None', inplace=True) 
df_clean['name'].replace("not",'None', inplace=True)
df_clean['name'].replace("one",'None', inplace=True)
df_clean['name'].replace("my",'None', inplace=True)
df_clean['name'].replace("O","O'Malley", inplace=True)
df_clean['name'].replace("quite","None", inplace=True)
df_clean['name'].replace("such","None", inplace=True)


# In[153]:


#test
df_clean.head()


#  define
#  remove tweets that are retweeted

# In[154]:


# Identify how many tweets are retweets by the "retweeted_status" columns
df_clean.info()


# In[155]:


#code
#excluding retweeted status because they are not needed
df_clean = df_clean[pd.isnull(df_clean.retweeted_status_id)]
# removing duplicates
df_clean = df_clean.drop_duplicates()

# Delete columns related to retweet we don't need anymore

df_clean = df_clean.drop('retweeted_status_id', 1)
df_clean = df_clean.drop('retweeted_status_user_id', 1)
df_clean = df_clean.drop('retweeted_status_timestamp', 1)




# In[156]:


# test
df_clean.head()


#  Define
#  Removinge rows where there are no images (expanded_urls).

# In[157]:


#code
df_clean = df_clean.dropna(subset=['expanded_urls'])


# In[158]:


#test
df_clean.head(2)


# Define
# Display full content of column 'text'

# In[159]:


# code
# Set column width to infinite so entire content of 'text' column is displayed
pd.set_option('display.max_colwidth', -1)


# In[160]:


#test
df_clean.head(2)


# # Define
# # creating 'dog_stage' variable and removing individual dog stage columns

# In[161]:


# code


# In[162]:


# Create 'dog_stage' variable which can be formed by extracting the dog stage variables from the text column when available 
df_clean['dog_stage'] = df_clean['text'].str.extract('(puppo|pupper|floofer|doggo)', expand=True)


# In[163]:


# Create variable of columns that are no longer needed and remove them from the DataFrame 
columns = ['doggo', 'floofer', 'pupper', 'puppo']
df_clean = df_clean.drop(columns, axis=1)


# In[164]:


#test
df_clean.head()


#  Define:
#  Delete duplicated jpg_url in img_pred data frame

# In[165]:


#CODE: Delete duplicated jpg_url
img_pred_clean = img_pred_clean.drop_duplicates(subset=['jpg_url'], keep='last')

#TEST
sum(img_pred_clean['jpg_url'].duplicated())


# Define
# making the text in 'img_pred' consistent and pretty

# In[166]:


#code
img_pred_clean['p1'] = img_pred_clean['p1'].str.title()
img_pred_clean['p2'] = img_pred_clean['p2'].str.title()
img_pred_clean['p3'] = img_pred_clean['p3'].str.title()


# In[167]:


#test
#displaying image predicion data
img_pred_clean.head()


# Define:
# changing incorrect dog names

# In[168]:


# code


# In[169]:


# Save locations where 'name' column is lowercase, lowercase and 'text' column contains 'named' and lowercase and 'text'
# column contains the words 'name is'
named_to_replace = df_clean.loc[(df_clean['name'].str.islower()) & (df_clean['text'].str.contains('named'))]
name_is_to_replace = df_clean.loc[(df_clean['name'].str.islower()) & (df_clean['text'].str.contains('name is'))]
not_named_to_replace = df_clean.loc[(df_clean['name'].str.islower())]

# Save these locations as lists
named_to_replace_list = named_to_replace['text'].tolist()
name_is_to_replace_list = name_is_to_replace['text'].tolist()
not_named_to_replace_list = not_named_to_replace['text'].tolist()


# In[170]:


# For loop to iterate through locations where name is lowercase and the words 'named' appear in 'text' and set the 'name' 
# value to be the word that appears after 'named'
for entry in named_to_replace_list:
    mask = df_clean.text == entry
    name_column = 'name'
    df_clean.loc[mask, name_column] = re.findall(r"named\s(\w+)", entry)


# In[171]:


#For loop to iterate through locations where name is lowercase and the words 'name is' appear in 'text' and set the 'name' 
# value to be the word that appears after 'name is'    
for entry in name_is_to_replace_list:
    mask = df_clean.text == entry
    name_column = 'name'
    df_clean.loc[mask, name_column] = re.findall(r"name is\s(\w+)", entry)    


# In[172]:


# For loop to iterate through locations where name is lowercase and replace the name value with the word "None"
for entry in not_named_to_replace_list:
    mask = df_clean.text == entry
    name_column = 'name'
    df_clean.loc[mask, name_column] = "None"


# In[173]:


# Replace the occurence of "O" with "O'Malley"
df.name = df_clean.name.replace("O", "O'Malley")


# In[174]:


# test
df_clean.name.sort_values()


# In[175]:


df_clean.loc[(df_clean['name'].str.islower())]


# In[176]:


df_clean[df_clean.name == "O'Malley"]


# Define
# Fix rating numerator and denominator that are not actually ratings

# In[177]:


# code


# In[178]:


# Viewing all occurences where there are more than one #/# in 'text' column
df_clean[df_clean.text.str.contains( r"(\d+\.?\d*\/\d+\.?\d*\D+\d+\.?\d*\/\d+\.?\d*)")]


# In[179]:


# Save the text where the rating numerator and denominators were incorrectly extracted
fix_ratings = ['After so many requests, this is Bretagne. She was the last surviving 9/11 search dog, and our second ever 14/10. RIP https://t.co/XAVDNDaVgQ', 
 'Happy 4/20 from the squad! 13/10 for all https://t.co/eV1diwds8a', 
 'This is Bluebert. He just saw that both #FinalFur match ups are split 50/50. Amazed af. 11/10 https://t.co/Kky1DPG4iq', 
 'This is Darrel. He just robbed a 7/11 and is in a high speed police chase. Was just spotted by the helicopter 10/10 https://t.co/7EsP8LmSp5',
 'This is an Albanian 3 1/2 legged  Episcopalian. Loves well-polished hardwood flooring. Penis on the collar. 9/10 https://t.co/d9NcXFKwLv']


# In[180]:


# Loop through the list of fix ratings and extract the second occurence of #/ to save as the rating numerator. As all the
# occurences of the actual ratings in the fix ratings list have a denominator of 10, we will set that value for each 
#entry instead of extracting it.
for entry in fix_ratings:
    mask = df_clean.text == entry
    column_name1 = 'rating_numerator'
    column_name2 = 'rating_denominator'
    df_clean.loc[mask, column_name1] = re.findall(r"\d+\.?\d*\/\d+\.?\d*\D+(\d+\.?\d*)\/\d+\.?\d*", entry)
    df_clean.loc[mask, column_name2] = 10


# In[181]:


#test
df_clean[df_clean.text.isin(fix_ratings)]


# define
# Fix rating numerator that have decimals

# In[182]:


# View tweets with decimals in rating in 'text' column
rating = df_clean.text.str.extract('((?:\d+\.)?\d+)\/(\d+)', expand=True)
df_clean['rating_numerator']=rating.iloc[:,0]
df_clean['rating_numerator']=rating.iloc[:,1]


# In[183]:


# Change datatype of rating_numerator and denominator from int  to float
df_clean['rating_numerator'] = df_clean['rating_numerator'].astype('float')
df_clean['rating_denominator'] = df_clean['rating_denominator'].astype('float')


# In[184]:


#Set correct numerators for specific tweets
df_clean.loc[(df_clean['tweet_id'] == 883482846933004288) & (df_clean['rating_numerator'] == 5), ['rating_numerator']] = 13.5
df_clean.loc[(df_clean['tweet_id'] == 786709082849828864) & (df_clean['rating_numerator'] == 75), ['rating_numerator']] = 9.75
df_clean.loc[(df_clean['tweet_id'] == 778027034220126208) & (df_clean['rating_numerator'] == 27), ['rating_numerator']] = 11.27
df_clean.loc[(df_clean['tweet_id'] == 680494726643068929) & (df_clean['rating_numerator'] == 26), ['rating_numerator']] = 11.26


# In[185]:


#test
df_clean.head()


# define
# Remove tweet without rating.
# 

# In[186]:


# code
df_clean = df_clean[df_clean.tweet_id != 810984652412424192]


# In[187]:


#test
df_clean[df_clean.tweet_id == 810984652412424192]


# Define
# Remove extra characters after '&' in df_clean['text'].

# In[188]:


df_clean['text'] = df_clean['text'].str.replace('&amp;', '&')


# Define
# change sources to more readable categories.
# 

# In[189]:


#code
# Remove url from sources
df_clean['source'] = df_clean['source'].str.replace('<a href="http://twitter.com/download/iphone" rel="nofollow">Twitter for iPhone</a>', 'Twitter for iPhone')
df_clean['source'] = df_clean['source'].str.replace('<a href="http://vine.co" rel="nofollow">Vine - Make a Scene</a>', 'Vine')
df_clean['source'] = df_clean['source'].str.replace('<a href="http://twitter.com" rel="nofollow">Twitter Web Client</a>', 'Twitter Web Client')
df_clean['source'] = df_clean['source'].str.replace('<a href="https://about.twitter.com/products/tweetdeck" rel="nofollow">TweetDeck</a>', 'TweetDeck')


# In[190]:


# Change datatype to category
df_clean['source'] = df_clean['source'].astype('category')


# In[191]:


#test
df_clean.source.value_counts()


# In[192]:


df_clean.info()


# Define
# Change datatypes of timestamp to datetime, dog_stage to categorical, and tweet_id, in_reply_to_status_id, and in_reply_to_user_id to strings.

# In[193]:


#code
df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])
df_clean['dog_stage'] = df_clean['dog_stage'].astype('category')
df_clean['tweet_id'] = df_clean['tweet_id'].astype('str')
df_clean['in_reply_to_status_id'] = df_clean['in_reply_to_status_id'].astype('str')
df_clean['in_reply_to_user_id'] = df_clean['in_reply_to_user_id'].astype('str')


# In[194]:


#test
df_clean.head()


# Define
# Merging all the gathered data set into one final data set 'df_merge

# In[195]:


# code


# In[196]:


df_merge = pd.concat([df_clean, tweet_info_clean], axis=1)


# In[197]:


df_merge=pd.concat([df_merge,img_pred_clean], axis=1)


# In[198]:


# test
df_merge.retweet_count


# In[199]:


# Storing


# In[200]:


# Save clean DataFrame to csv file
df_merge.to_csv('df_master.csv')


# Analyzing and Visualisation

# In[201]:


#Favorites vs Retweets Among Dog Stages
# Lets observe how retweets relate to the number of favorites a tweet recieves. There should be a relationship but it will be interesting to see how this differs with the different dog stages (pupper, floofer, etc.)


# In[202]:


from scipy import stats
import matplotlib.patches as mpatches
# Create a (sub)database of only attributes I care about 
df = df_merge[['retweet_count', 'favorite_count', 'dog_stage']]

# limit number for testing
# df=df.iloc[0:1000]

# Create linear line of best fit of all data points
y, x = df.retweet_count, df.favorite_count
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
line = slope*x+intercept
plt.plot(x, y, 'o', x, line, color='gray')

print('Line Equation: retweets = ({})*favorites + {}'.format(slope,intercept))
print('Correlation of line of best fit: {}'.format(r_value))

#####


# Create separate databases for each dog stage (don't count mutliple classifications)
df_puppers = df[df['dog_stage'] == 'pupper']
df_puppo = df[df['dog_stage'] == 'puppo']
df_doggo = df[df['dog_stage'] == 'doggo']
df_floofer = df[df['dog_stage'] == 'floofer']
df_none = df[df['dog_stage'] == 'None']



# Plot all data to see general shape
bx = df_puppers.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Orange', alpha=0.3)
df_doggo.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Blue', ax=bx, alpha=0.3)
df_puppo.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Green', ax=bx, alpha=0.3)
df_floofer.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Red', ax=bx, alpha=0.3)


# Legend
puppers = mpatches.Patch(label='pupper', color = 'Orange')
doggo = mpatches.Patch(label='doggo', color = 'Blue')
puppo = mpatches.Patch(label='puppo', color = 'Green')
floofer = mpatches.Patch(label='floofer', color = 'Red')

plt.legend(handles=[puppers, doggo, puppo, floofer])
plt.plot(x, line, color='gray')

plt.show()
plt.savefig("data_visual.png")


# In[203]:



# Zoom into where most data resides# Zoom in 
xlim = (0, 25000)
ylim = (0, 10000)

# Recreate the same plot (but now it will be zoomed in)
ax = df_puppers.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Orange', alpha=0.3, ylim=ylim, xlim=xlim)
df_doggo.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Blue', ax=ax, alpha=0.3, ylim=ylim, xlim=xlim)
df_puppo.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Green', ax=ax, alpha=0.3, ylim=ylim, xlim=xlim)
df_floofer.plot(kind = 'scatter', x='favorite_count', y='retweet_count', color='Red', ax=ax, alpha=0.3, ylim=ylim, xlim=xlim)


plt.legend(handles=[puppers, doggo, puppo, floofer])
plt.plot(x, line, color='gray')

plt.show()
plt.savefig("zoom.png")


# In[204]:


# Most common dog breeds


# In[205]:


# Geting features before determinig dog breed
features = ['retweet_count', 'favorite_count', 'rating_denominator', 'rating_numerator']
df_dog_breeds = df_merge[features].copy()

# Create rating column
def percent_rating(row):
    if row['rating_denominator'] == 0:
        return 0
    return row['rating_numerator']/row['rating_denominator']


df_dog_breeds['rating'] = df_dog_breeds.apply(percent_rating, axis=1)


# In[206]:


# Geting needed attributes for possible dog
attributes = ['p1', 'p1_dog', 'p1_conf', 'p2', 'p2_dog', 'p2_conf', 'p3', 'p3_dog', 'p3_conf']
df_possible_breeds = df_merge[attributes].copy()

# Create default for breeds and confidence
df_possible_breeds['breed'] = ''
df_possible_breeds['breed_conf'] = 1


# In[207]:


# check which is the most likely breed for each entry
def breed_match(row):
    
    # Defaults to compare against
    breed = 'not_dog'
    confidence = 0
    
    # keep only if it is a possible dog
    dog_preds = [(row[['p1', 'p1_dog', 'p1_conf']]), (row[['p2', 'p2_dog', 'p2_conf']]), (row[['p3', 'p3_dog', 'p3_conf']])]
    
    # Use this for easy reference
    index_breed, index_isDog, index_conf = 0,1,2
    
    
    for pred in dog_preds:
        # If it's a dog breed, check if it's max confidence seen
        if pred[index_isDog]:
            # save breed and confidence if higher confidence
            if pred[index_conf] >= confidence:
                breed = pred[index_breed]
                confidence = pred[index_conf]
    # Update breed list
    row['breed'] = breed
    row['breed_conf'] = confidence
    return row
        
    breeds = [row['p1'], row['p2'], row['p3']]
    
    
df_possible_breeds = df_possible_breeds.apply(breed_match, axis=1)

  


# In[208]:


# Save info into dog breed dataframe
df_dog_breeds['breed'] = df_possible_breeds['breed']

df_dog_breeds['breed_conf'] = df_possible_breeds['breed_conf']


# In[209]:


# show 20 most common dog breeds
df_dog_breeds.breed.value_counts()[:20] # keep not_dog out of plot as it is most common


# In[210]:


# Plot the 15 most common dog breeds in bar chart
only_dogs = df_dog_breeds['breed'] != 'not_dog'
df_dog_breeds[only_dogs].breed.value_counts()[15::-1].plot(kind='barh')
plt.savefig("common_dog_breeds.png")


# In[211]:


# Plot the data partitioned by dog stages

dog_stage_count = list(df_merge[df_merge['dog_stage'] != 'None']['dog_stage'].value_counts())[0:4]
dog_stages = df_merge[df_merge['dog_stage'] != 'None']['dog_stage'].value_counts().index.tolist()[0:4]
explode = (0.2, 0.1, 0.1, 0.1) 

fig1, ax1 = plt.subplots()
ax1.pie(dog_stage_count, explode = explode, labels = dog_stages, shadow = True, startangle = 90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.savefig("data_partitioned.png")

