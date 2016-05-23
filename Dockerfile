FROM jupyter/all-spark-notebook
RUN conda install basemap 
RUN git clone https://github.com/pavanpc/Twitter-Feeds-Stream-Clustering.git
CMD /usr/local/spark/bin/spark-submit  --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1  Twitter-Feeds-Stream-Clustering/pyspark-streaming-clustering/streaming_k_means.py 

