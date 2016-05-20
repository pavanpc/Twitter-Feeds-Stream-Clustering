from __future__ import print_function
import sys
from pyspark.streaming import StreamingContext
from pyspark import SparkContext,SparkConf
from pyspark.streaming.kafka import KafkaUtils
import json

import os
import sys
import ast
import json

import re
import string
import matplotlib.pyplot as plt
import threading
import Queue
import time
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np
import multiprocessing

from pyspark import SparkContext
from pyspark import SQLContext,Row
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.ml.feature import HashingTF,IDF, Tokenizer
from pyspark.mllib.linalg import Vectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.clustering import StreamingKMeans
from pyspark.mllib.feature import StandardScaler
from pyspark.mllib.feature import Word2Vec
from pyspark.mllib.feature import Word2VecModel

BATCH_INTERVAL = 15  # How frequently to update (seconds)
clusterNum=15
# Change the backend to TkAgg to plot - only for Mac users
plt.switch_backend('TkAgg')
def get_cordinates_from_event(twitter_feed):
    '''
            Method to get lat ,long coordinates from twitter feed event
            Args:
                twitter_feed: twitter_feed event as json
            Returns:
                coordinates: a tuple of coordinates as (lat,lng) 
        '''
    coordinates = tuple()
    try:
        # if coordinates key not found , get from place polygon key
        if twitter_feed['coordinates'] == None:
            coordinates = twitter_feed['place']['bounding_box']['coordinates']
            coordinates = reduce(lambda agg, nxt: [agg[0] + nxt[0], agg[1] + nxt[1]], coord[0])
            coordinates = tuple(map(lambda t: t / 4.0, coord))
        else:
            coordinates = tuple(twitter_feed['coordinates']['coordinates'])
    except TypeError:
        coordinates=(0,0)
    return coordinates


def get_json_from_string_from_string(jsonString):
    '''
            Methos to convert the twitter feed event read from kafka to json
            Args:
                jsonString: even data as string
            Returns:
                json: converted json 
        '''
    try:
        json_object = json.loads(myjson.encode('utf-8'))
    except ValueError, e:
        return False
    return json_object


def doc2vec(twitter_feed_document):
    '''
            Method to get the vectors for every feed text from word2vec model already built using Word2Vec spark mllib library
            Args:
                twitter_feed_document: tuple of feed words got after pre processing (remove stop words, stemming)
            Returns:
                vecor representation of words in the feed text
        '''
    doc_vector = np.zeros(100)
    total_words = 0

    for word in twitter_feed_document:
        try:
            vector = np.array(lookup_bd.value.get(word))
            if vec!= None:
                doc_vector +=  vector
                total_words += 1
        except:
            continue

    #return(total_words)
    return doc_vector / float(total_words)


# Reg ex to remove special characters from feed text
special_character_regex = re.compile('[%s]' % re.escape(string.punctuation)) 
# list of stop words to remove, extracted from nltk python library 
stopwords=[u'i', u'me', u'my', u'myself', u'we', u'our', u'ours', u'ourselves', u'you', u'your', u'yours', u'yourself', u'yourselves', u'he', u'him', u'his', u'himself', u'she', u'her', u'hers', u'herself', u'it', u'its', u'itself', u'they', u'them', u'their', u'theirs', u'themselves', u'what', u'which', u'who', u'whom', u'this', u'that', u'these', u'those', u'am', u'is', u'are', u'was', u'were', u'be', u'been', u'being', u'have', u'has', u'had', u'having', u'do', u'does', u'did', u'doing', u'a', u'an', u'the', u'and', u'but', u'if', u'or', u'because', u'as', u'until', u'while', u'of', u'at', u'by', u'for', u'with', u'about', u'against', u'between', u'into', u'through', u'during', u'before', u'after', u'above', u'below', u'to', u'from', u'up', u'down', u'in', u'out', u'on', u'off', u'over', u'under', u'again', u'further', u'then', u'once', u'here', u'there', u'when', u'where', u'why', u'how', u'all', u'any', u'both', u'each', u'few', u'more', u'most', u'other', u'some', u'such', u'no', u'nor', u'not', u'only', u'own', u'same', u'so', u'than', u'too', u'very', u's', u't', u'can', u'will', u'just', u'don', u'should', u'now']


def tokenize(text):
    '''
            Method to remove special characters, stop words from text and tokenize 
            Args:
                text: actual text to be tokenized
            Returns:
                list of tokens generated
        '''
    tokens = []
    text = text.encode('ascii', 'ignore') #to decode
    text=re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text) # to replace url with ''
    text = special_character_regex.sub(" ",text)  # Remove special characters
    text=text.lower()

    for word in text.split():
        if word not in stopwords \
            and word not in string.punctuation \
            and len(word)>1 \
            and word != '``':
                tokens.append(word)
    return tokens

from collections import Counter
def get_most_popular_words(terms):
    '''
            Method to get the most most_common/ frequently used/polular words from the tweeet after clustering
            Args:
                terms: list of terms of clusters
            Returns:
                most top 5 frequently used words.
            We can also pass frequency as parameter 
        '''
    count_all = Counter()
    count_all.update(terms_all)
    return count_all.most_common(5)

def plot_data(q):
    '''
            Method to plot the data / cluster points after applying clustering on test data.
            This is the target method of python mulitprocessing 
            Args:
                q: A queue which contains the coordinates for plotting.
            Returns:
        '''
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap
    import matplotlib.pyplot as plt
    from pylab import rcParams
    import numpy as np

    plt.ion() 
    llon = -130
    ulon = 100
    llat = -30
    ulat = 60
    rcParams['figure.figsize'] = (14,10)
    my_map = Basemap(projection='merc',
                resolution = 'l', area_thresh = 1000.0,
                llcrnrlon=llon, llcrnrlat=llat, #min longitude (llcrnrlon) and latitude (llcrnrlat)
                urcrnrlon=ulon, urcrnrlat=ulat) #max longitude (urcrnrlon) and latitude (urcrnrlat)

    my_map.drawcoastlines()
    my_map.drawcountries()
    my_map.drawmapboundary()
    my_map.fillcontinents(color = 'white', alpha = 0.3)
    my_map.shadedrelief()
    plt.pause(0.0001)
    plt.show()


    colors = plt.get_cmap('jet')(np.linspace(0.0, 1.0, clusterNum))

    while True:
        if q.empty():
            time.sleep(5)

        else:
            # when queue is not empty plot the results
            obj=q.get()
            d=[x[0][0] for x in obj]
            c=[x[1] for x in obj]
            data = np.array(d)
            pcolor=np.array(c)
            print("inside queue")
            #print(c)
            try:
                xs,ys = my_map(data[:, 0], data[:, 1])
                my_map.scatter(xs, ys,  marker='o', alpha = 0.5,color=colors[pcolor])
                plt.pause(0.0001)
                plt.draw()
                time.sleep(5)
            except IndexError: # Empty array
                pass

if __name__ == "__main__":
    '''
           Main method which does following
           1. Reads data from kafka topic - 'twitter-topic' in a BATCH_INTERVAL
           2. Reads the preivously build word2vec model using parquet
           3. Prepocesses(tokenize) feed data
           4. Prepares test and trainingData
           5. Runs streaming k-means model
           6. Clustering is based on geo location (using lat, long) and feeds text simliarity using word2vec.
           7. Plots the identified clusters and data using matplotlib. To achiece this I have used mulitprocessing with Queues as its a streaming system
           TODO: Persist the model to HDFS/ local files system for later use.
        '''
    # Multiprocessing
    q = multiprocessing.Queue()
    job_for_plotting = multiprocessing.Process(target=plot_data,args=(q,))
    job_for_plotting.daemon=True
    job_for_plotting.start()

    # Intialized Spark config
    conf = SparkConf().setAppName("Kafka-Spark-Twitter-Feed-Clustering")
    sc = SparkContext(conf=conf)
    # get streaming context of batch interval 10 seconds
    #  TODO:
    #  Change this based on number of kakfka partitions , time to process current batch.
    # The above point is very crucial in prouction systems to achieve better paralelism in spark and handle backpresure
    stream=StreamingContext(sc,10) #
    kafka_topic={'twitter-topic':1}
    # Read the stream into dstreams
    # Note : this is the loclahost mode
    kafkaStream = KafkaUtils.createStream(stream, 'localhost:2181', "name", kafka_topic) 

    # Read word2vector model built offline using parquet
    sqlContext=SQLContext(sc)
    word2vec_model = sqlContext.read.parquet("/Users/pavanpc/Documents/lovoo/spark/spark-1.6.0/streaming_k_means_model/data").alias("word2vec_model")
    #print(lookup.rdd.collectAsMap())
    print("Read Word2Vec model from parquet")
    # Boradcasting is used to avoid the copy of model in every machine/worker nodes
    word2vec_model_brooadcast = sc.broadcast(word2vec_model.rdd.collectAsMap())
    # The below code does folowing
    # Converts kafka event to json
    # Filters them based on created_at field in json. 
    # TODO: We can use Avro for schema management
    #Gets Coordinates lat,lng, and tokenize tweet text and append word2vect vector for every token
    print("Processing tweets....")
    processed_tweets= kafkaStream.map(lambda tweet : get_json_from_string(tweet[1]) ).filter(lambda tweet: tweet != False).filter(lambda tweet: 'created_at' in tweet).map(lambda tweet: (get_cordinates_from_event(tweet)[0],get_cordinates_from_event(tweet)[1],tweet["text"])).filter(lambda tpl: tpl[0] != 0).filter(lambda tpl: tpl[2] != '').map(lambda processed_tweet: (processed_tweet[0],processed_tweet[1],tokenize(processed_tweet[2]))).map(lambda processed_tweet:(processed_tweet[0],processed_tweet[1],processed_tweet[2],doc2vec(processed_tweet[2])))
    

    # Training data of the form (lat.long, word2vect list for feed text)
    # Training uses the offline built model ie, word2vec_model
    trainingData=processed_tweets.map(lambda processed_tweet: [processed_tweet[0],processed_tweet[1]]+processed_tweet[3].tolist())
    
    # test data
    # It includes lat , long , actual tokenized text and word2vector words
    testdata=processed_tweets.map(lambda processed_tweet: (([processed_tweet[0],processed_tweet[1]],processed_tweet[2]),[processed_tweet[0],processed_tweet[1]]+processed_tweet[3].tolist()))
    
    print("Training model using streaming-k means")
    # Streaming k means model
    # Using decayFactor of 0.6 - can be changed. This is for forgetfullness of data, ie importance to data in stram based on recency
    # refer to this blog for mode info - https://databricks.com/blog/2015/01/28/introducing-streaming-k-means-in-spark-1-2.html
    model = StreamingKMeans(k=clusterNum, decayFactor=0.6).setRandomCenters(102, 1.0, 3)
    model.trainOn(trainingData)

    print("Clustering feeds based on geo and word/topic simliarities....")
    clusters=model.predictOnValues(testdata)
    topic=clusters.map(lambda x: (x[1],x[0][1]))
    # Aggregate based on words used in clusters which forms a topic
    topicAgg = topic.reduceByKey(lambda x,y: x+y)
    print("topic aggregation")
    popular_words_for_clusters=topicAgg.map(lambda x: (x[0],get_most_popular_words(x[1])))
    print(popular_words_for_clusters.pprint())
    #clusters.foreachRDD(lambda time, rdd: q.put(rdd.collect()))
    processed_tweets.repartition(1).saveAsTextFiles("output.txt")
    stream.start()
    stream.awaitTermination()
