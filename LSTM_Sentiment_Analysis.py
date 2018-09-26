import gensim
import pandas as pd
import numpy as np
from nltk import word_tokenize
from keras.layers import Dense, Dropout, Embedding, Conv1D, MaxPooling1D, LSTM
from keras import Sequential
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

#Implementation of lstm for sentiment analysis using maxplooing and convolution for feature selection
dataset = pd.read_csv("fake_or_real_news.csv")

list(dataset)

dataset['label'] = np.where(dataset['label'] == 'FAKE', 1, 0)

#To get embedding matrix of the vocabulary
text = list(dataset['text'])
text = [word_tokenize(line.lower()) for line in text]
model = gensim.models.Word2Vec(text, size=150, window=13, min_count=1, workers=12)
model.train(text, total_examples=len(text), epochs=13)

vocabLen = 30000
tokenizer = Tokenizer(num_words=vocabLen)
tokenizer.fit_on_texts(text)

sequences = tokenizer.texts_to_sequences(text)
X = pad_sequences(sequences, maxlen=1000)
y = np.array(dataset['label'])

embedding_matrix = np.zeros((vocabLen, 150))
for word, index in tokenizer.word_index.items():
    embedding_vector = model.wv.get_vector(word)
    if embedding_vector is not None:
        if index > vocabLen - 1:
            break
        embedding_matrix[index] = embedding_vector


lstmClassifier = Sequential()

#Embedding layer to get the embedding for every word of the sentence
lstmClassifier.add(Embedding(vocabLen, 150, input_length=1000, weights=[embedding_matrix], trainable=False))

lstmClassifier.add(Dropout(0.15))

#Used 1D maxpooling and conv layers
lstmClassifier.add(Conv1D(64, 3, activation='relu'))
lstmClassifier.add(MaxPooling1D(pool_size=4))

lstmClassifier.add(LSTM(100))
lstmClassifier.add(Dense(1, activation='sigmoid'))
lstmClassifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

lstmClassifier.fit(X, y, batch_size=300, epochs=11, validation_split=0.15)

#Nothing fancy for the rest of the model
