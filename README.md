# Twiter Feeds clustring using kafka, Streaming spark and spark mllib

## Design Details
### Producer
  1. A java client to publish messages to kafka using twitter hbc(https://github.com/twitter/hbc) streaming http client
  2. The twitter feeds are read coninuosly and published to a kakfka topic

### Consumer
  1. The events from kafka is read using spark streaing
  2. The events are prepocessed which involves removing stopwords(extracted from nltk library for english),stemming and tokenizing.
  3. The test data is prepared for the events read.
  4. To start with we should have some model to already trained. So Googles'  word2vector model is used to train data offline and stored in parquet file.
  5. The model is read from in streaming conext and the clusters are obtained applying streaming-kmeans with decay factor.
  6. The clusters are formed based on geo and words similarities in twitter feeds. Read more about word2vector here.https://code.google.com/archive/p/word2vec/
##Technology Used
  1. Python 2.7.6
  2. kafka 0.9.0
  3. pyspark -1.6
  4. spark mllib
  5. matplotib
  6. numpy,scipy
  7. java 7
  8. twitter hbc java client
  9. java kafka client
