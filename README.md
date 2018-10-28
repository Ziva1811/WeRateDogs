# WeRateDogs

Introduction:
WeRateDogs is a very popular Twitter account with over 4 million followers and has received international media coverage. WeRateDogs gained its popularity by rating people’s dogs with a good-natured comment about the dog.


About the data:

To analyze the tweets from WeRateDogs, three different sources has been used. The first source is an archive file of the past tweets from @dog_rates (https://twitter.com/dog_rates) in a CSV file

The second source is from the Twitter API used to retrieve more information about the tweets like number of tweets that were  retweeted.
 
The third data source provides us the predicted dog breed in each tweet's image programmatically determined from a neural network.

WeRateDogs downloaded their Twitter archive and sent it to Udacity via email exclusively for us.
Additional gathering, then assessing and cleaning was required to present this analyses and
Visualizations


Data Assessing:

Data was assessed visually as well as programmatically.  Through pandas info(), head(),describe() methods I was able to detect some quality and tideness issues like many tweets were retweeted, dataframe contained the faulty names,there were several empty values in in_reply_to_status, in_reply_to_user_id, retweeted_status_id, retweeted_status_user_id, retweeted_status_timestamp.



Data Cleaning:

The copy of all the data frame were created as “df_clean”, “img_pred_clean”, tweet_info_clean.
Retweets were removed and tweets which did not include images were also removed because
those tweets were not dog ratings.

dog_stage column was created which showed the type of dog(dog stages).
Duplicate jpg_url in “img_pred_clean” dataframe was dropped . The text in 'img_pred' was made consistent and pretty.

Incorrect dog names in “df_clean” were changed. tweet without rating was removed. The value for rating numerator and denominator was corrected. The column “source” was made in more readable categories.

Datatypes of timestamp,dog_stage and tweet_id, in_reply_to_status_id,in_reply_to_user_id  was changed to datetime, categorical, and to strings respectively.

After doing all the process of cleaning all the dataframe was merged in single data frame named “df_merge” and was stored in a csv file named “df_master.csv” and then dataset was visualized in different forms
