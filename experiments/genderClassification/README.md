# Gender Classification

# Data

* [Blogger Dataset ](https://s3-us-west-1.amazonaws.com/nextml/blogger_data_2.csv.tar.gz)

# Model

* Three-layer RNN with LSTM and Dropout units.
* Optimization: Adam

# Experimental Result

## Testing Accuracy

* 72.2%

## Reddit User Gender Prediction

* Comments were randomly selected from two subreddits(femalefashionadvice and Battlefield).
* Only comments with 50~800 words were used for predictions.
* 10000 comments were used to make predictions for each subreddit.

![My image](https://cloud.githubusercontent.com/assets/5894018/8758878/dc180f4a-2cb7-11e5-81a0-88ed21c305c8.png)