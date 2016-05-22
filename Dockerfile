FROM jupyter/all-spark-notebook
RUN conda install basemap 
ADD ./streaming_k_means.py /usr/local/spark/examples/src/main/python/twitter_streaming_k_means.py
COPY ./streaming_k_means.py /usr/local/spark/examples/src/main/python/twitter_streaming_k_means.py
RUN git clone https://github.com/pavanpc/Twitter-Feeds-Stream-Clustering.git
CMD /usr/local/spark/bin/spark-submit  --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1  Twitter-Feeds-Stream-Clustering/pyspark-streaming-clustering/streaming_k_means.py 

