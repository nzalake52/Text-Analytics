# Text-Analytics

Creation of Word2Vec model to get word embeddings using the Gensim package.<br>


Implementation of RNN LSTM for sentiment analysis using maxplooing, convolution and dropout to prevent overfitting.
Using word embeddings vector of size 150.

The input to LSTM will be a vector for each news article of fixed length 1000 words, which are padded if the articles
are less in length and restricted to 1000 words by removing the extra ones.
Thus for each article the size of vector is same which is then multipled with word embedding matrix.

So the output for an article is the vector of shape (1000, 150) given input to RNN.

RNN is implemented using KERAS implementation of Tensorflow.
Feel free to change the input data to any other text.

Instead of using Word2Vec you can also use any other pre trained models like GloVe for embedding matrix.
