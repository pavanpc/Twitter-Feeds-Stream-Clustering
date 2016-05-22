# Twiter Feeds clustring using kafka, Streaming spark and spark mllib


## Usage
The <b>kafka_setup.sh</b> script brings the kafka image present in <b>docker-compose.yml</b> up and running. Also, it starts publishing the twitter events from streaming api to kafka topic. Once the kafka_setup.sh starts running, you can see the twitter events read on console.

The <b>spark_setup.sh</b> script brings the spark image present in docker-compose.yml up and running. Also, it links the kafka container already created . Once the spark_setup.sh starts running, you can see the pysprk streaming application with streaing k-means clustering running .

Follow below steps as a <b>root user</b>

1. Open a terminal window.

2. git clone https://github.com/pavanpc/Twitter-Feeds-Stream-Clustering.git

3. cd Twitter-Feeds-Stream-Clustering

4. chmod 755 kafka_setup.sh

5. ./kafka_setup.sh

6. Open a new terminal window

7. cd to Twitter-Feeds-Stream-Clustering (the git project we have cloned in step 2)

8. chmod 755 spark_setup.sh

9. ./spark_setup.sh

 <b>--------------------Streaming k-means Output based on  Geo and Tweet words similarity-----------------------</b>
 <br/>Points with same color tend to have similar geo and word similarities
![Alt text](Clusters_plot_on_world_map.png?raw=true "Optional Title")
                                                  
## Design Details
### Producer
  1. A java client to publish messages to kafka using twitter hbc(https://github.com/twitter/hbc) streaming http client
  2. The twitter feeds are read coninuosly and published to a kakfka topic

### Consumer
  1. The events from kafka is read using spark streaing
  2. The events are prepocessed which involves removing stopwords(extracted from nltk library for english),stemming and tokenizing.
  3. The test data is prepared for the events read.
  4. To start with we should have some model which is already trained. So Googles'  <b>word2vector</b> model is used to train data offline and stored in parquet file.
  5. The model is read from in streaming conext and the clusters are obtained applying <b>streaming-kmeans</b> with decay factor.
  6. The clusters are formed based on geo and words similarities in twitter feeds. Read more about word2vector here.https://code.google.com/archive/p/word2vec/

### Spark configurations 
1. To achieve better parallelism and stable system,  consider Streaming batch interval, Processing time and Median streaming rate.
2. Start with a batch window size of 5-10 seconds and observe processing time.Try to alter the time interval  and observe processing time.
3. Limit the stream receiver using spark.streaming.receiver.maxRate option for given time window.
4. After having above stable system, increase parallelism using by increasing the amount of Spark workers and Partitioning  Kafka messages and creating a Stream for each partition and Repartitioning these Streams again.
5. The current application runs in a local mode with a batch interval of 15 seconds and one kafka parition.



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
