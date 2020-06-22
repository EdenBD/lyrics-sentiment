# LyricsAudioBoost 
## Combining BERT and Spotify Valence Feature For Track Sentiment Analysis

Built to solve this problem:

As the images above demonstrate, using strictly audio OR lyrics to measure a song positiveness might be inaccurate. 

In [this notebook](https://github.com/EdenBD/lyrics-sentiment/blob/master/Tracks_Sentiment_Analysis.ipynb) I combine Spotify audio feature and BERT word embedding, to produce more realistic predictions of sentiment. 
I use [hugginface](https://github.com/huggingface/transformers) pre-trained BERT transformer as an embedding layer, and train an additional bidirectional GRU layer for the sentiment analysis, regression task (outputting a point prediction instead of a class). 
To train the fine-tunning layer of the model, I use Spotify valence attribute on which I added to a lyrics dataset. 

There are four main steps I too to build the final model:
    1. Database: gathering songs lyrics from [Kaggle dataset](https://www.kaggle.com/detkov/lyrics-dataset), adding [Spotify valence attribute](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/) and [pre-processing](https://github.com/EdenBD/lyrics-sentiment/blob/master/Spotify_Dataset.ipynb). Uploaded the pre-processed dataset to [Kaggle](https://www.kaggle.com/edenbd/150k-lyrics-labeled-with-spotify-valence). 
    2. Model Design: Iteratively improved model capacity. 
    3. Evaluation: loss and accuracy metrics across 3 buckets - negative, neutral and positive sentiments. 
    4. Interpretation: Understanding what the model is learning using word clouds.
\end{enumerate}
