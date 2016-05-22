#Uncomment below line if you are using virtual box, dev2 is the virtual environment name
#eval "$(docker-machine env dev2)"

docker build -f Dockerfile .

# builds the new docker image for spark using Dockerfile present in current directory
docker build -t jupyter/all-spark-notebook:v3 .

#brings the spark image present in docker-compose.yml up and links it with the kafka image running
docker-compose up -d

#brings the spark container up and executes below command(starts spark streaming application) inside container and ouputs to stdout
docker run -it jupyter/all-spark-notebook:v3 /usr/local/spark/bin/spark-submit  --packages org.apache.spark:spark-streaming-kafka_2.10:1.6.1  Twitter-Feeds-Stream-Clustering/pyspark-streaming-clustering/streaming_k_means.py