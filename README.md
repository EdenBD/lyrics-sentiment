# LyricsAudioBoost 
## Combining BERT and Spotify Valence Feature For Track Sentiment Analysis

In [this notebook](https://github.com/EdenBD/lyrics-sentiment/blob/master/Tracks_Sentiment_Analysis.ipynb) I combine Spotify audio feature and BERT word embedding to predict tracks sentiments. 
I use [hugginface](https://github.com/huggingface/transformers) pre-trained BERT transformer as an embedding layer, and train an additional bidirectional GRU layer for the sentiment analysis regression task (point prediction in range [0-1]). 
To train the fine-tunning layer of the model I use Spotify valence attribute which I added to a lyrics dataset. 

### Motivation:

As the images above demonstrate, using strictly audio OR lyrics to measure a song positiveness might be inaccurate. 

### Steps to build model:

 1. **Database:** gathering songs lyrics, adding [Spotify valence attribute](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/) and [pre-processing](https://github.com/EdenBD/lyrics-sentiment/blob/master/Spotify_Dataset.ipynb).I uploaded to Kaggle the final [150K Lyrics Labeled with Spotify Valence Dataset](https://www.kaggle.com/edenbd/150k-lyrics-labeled-with-spotify-valence). 
 2. **Model Design:** Iteratively improved model capacity. 
 3. **Evaluation:** loss and accuracy metrics across 3 buckets - negative, neutral and positive sentiments. 
 4. **Interpretation:** Understanding what the model is learning using word clouds.
