# LyricsAudioBoost 
## Combining BERT and Spotify Valence Feature For Track Sentiment Analysis

In [this notebook](https://github.com/EdenBD/lyrics-sentiment/blob/master/Tracks_Sentiment_Analysis.ipynb) I combine Spotify audio feature and BERT word embedding to predict tracks sentiments. 
I use [hugginface](https://github.com/huggingface/transformers) pre-trained BERT transformer as an embedding layer, and train an additional bidirectional GRU layer for the sentiment analysis regression task (point prediction in range [0-1]). 
To train the fine-tunning layer of the model I use Spotify valence attribute which I added to a lyrics dataset. 

### Motivation:

The examples below use [NLTK demo](https://text-processing.com/demo/sentiment/) and [Spotify valence](https://developer.spotify.com/console/get-audio-features-track/?id=06AKEBrKUckW0KREUWRnvT) to measure a track's positivenesss. They demonstrate that using strictly audio OR lyrics might be inaccurate. 
  1. [Baz Luhrmann - Everybody's Free To Wear Sunscreen](https://www.youtube.com/watch?v=sTJ7AzBIJoI&t=33s)
     * NLTK sentiment classification: Negative 
     * Spotify Valence: 0.8  **CORRECT**
  2. [Otis Redding- Mr. pitiful](https://www.youtube.com/watch?v=Alo7U0S_VPU)
     * NLTK sentiment classification: Negative **CORRECT** 
     * Spotify Valence: 0.9

### Steps to build model:

 1. **Database:** gathering songs lyrics, adding [Spotify valence attribute](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/) and [pre-processing](https://github.com/EdenBD/lyrics-sentiment/blob/master/Spotify_Dataset.ipynb). I uploaded to Kaggle the final [150K Lyrics Labeled with Spotify Valence Dataset](https://www.kaggle.com/edenbd/150k-lyrics-labeled-with-spotify-valence). 
 2. **Model Design:** Iteratively improved model capacity. 
 3. **Evaluation:** loss and accuracy metrics across 3 buckets - negative, neutral and positive sentiments. 
 4. **Interpretation:** Understanding what the model is learning using word clouds.
 
 ### Example:
Words in the word cloud are sized by their respective difference on the model's prediction, and their positive (green) or negative (red) influence. 
 
  [Armin Van Buuren- Blah Blah Blah](https://www.youtube.com/watch?v=mfJhMfOPWdE):
     * NLTK sentiment classification: Negative
     * Spotify Valence: 0.18
     * LyricsAudioBoost Model: 0.76  **CORRECT** 

 ![Model interpretation - Word cloud](https://github.com/EdenBD/lyrics-sentiment/blob/master/blah_good.png)
 
