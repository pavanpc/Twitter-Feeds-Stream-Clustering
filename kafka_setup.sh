#add below line if you are using virtual box, dev2 is the virtual environment name
#eval "$(docker-machine env dev2)"

docker build -f Dockerfile_kafka .

#brings the kafka image present in docker_compose.yml up 
docker-compose up -d

# copies the fat jar and config required to publish twitter events to kafka
docker cp twitter-feed-0.0.1-SNAPSHOT-jar-with-dependencies.jar kafka:/home/twitter-feed-0.0.1-SNAPSHOT-jar-with-dependencies.jar
docker cp AppConfig.properties kafka:/home/AppConfig.properties

docker exec -it $(docker-compose ps -q kafka) bash -c " kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 2 --topic twitter-topic"

# executes below command inside the kafka running container and outputs the result to stdout. You can see twitter messages on console
docker exec -it $(docker-compose ps -q kafka) bash -c "cd /home/ && java -jar twitter-feed-0.0.1-SNAPSHOT-jar-with-dependencies.jar"
