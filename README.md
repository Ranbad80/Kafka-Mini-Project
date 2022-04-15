# Kafka-Mini-Project
 use streaming data to create a fraud detection platform that flags suspicious activity as potentially fraudulent.
first we Firing up a local Kafka cluster :
1- $ docker-compose up
2-  $ docker-compose logs -f broker | grep started
broker_1 | INFO [KafkaServer id=1] started (kafka.server.KafkaServer)

Isolating the Kafka cluster
$ docker network create kafka-network

after making the detector and generator:
1- $ docker-compose up
2- create topic queueing.transactions
   $ bin/kafka-topics.sh --create --topic queueing.transactions --bootstrap-server localhost:9092
   
3-  docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic queueing.transactions --from-beginnin

![kafka2](https://user-images.githubusercontent.com/83798130/163633079-475e84f8-5bd7-4c6e-b570-f3ad243ce25c.png)

4- create topic streaming.transactions
$ bin/kafka-topics.sh --create --topic streaming.transactions --bootstrap-server localhost:9092

docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.legit


docker-compose -f docker-compose.kafka.yml exec broker kafka-console-consumer --bootstrap-server localhost:9092 --topic streaming.transactions.fraud![Kafka1](https://user-images.githubusercontent.com/83798130/163633623-4c477c48-7cd9-4094-b99a-a5f91a76db56.jpg)
