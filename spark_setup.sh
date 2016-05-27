#Uncomment below line if you are using virtual box, dev2 is the virtual environment name
#eval "$(docker-machine env dev2)"

docker build -f Dockerfile .

# builds the new docker image for spark using Dockerfile present in current directory
docker build --no-cache -t jupyter/all-spark-notebook:v3 .

# Create network named  twitterfeedsstreamclustering_default to link with kafka
docker network create twitterfeedsstreamclustering_default

# Verify the network details and id
docker network ls | grep twitterfeedsstreamclustering_default

#brings the spark image present in docker-compose.yml up and links it with the kafka image running
docker-compose up -d

#brings the spark container up and executes below command(starts spark streaming application) inside container and ouputs to stdout
docker run -it --link kafka  --net twitterfeedsstreamclustering_default jupyter/all-spark-notebook:v3 /usr/local/spark/bin/spark-submit  --jars Twitter-Feeds-Stream-Clustering/dependencies/spark-streaming-kafka-assembly_2.10-1.6.1.jar  Twitter-Feeds-Stream-Clustering/pyspark-streaming-clustering/streaming_k_means.py
