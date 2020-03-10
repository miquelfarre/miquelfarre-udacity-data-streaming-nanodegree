# SF Crime Statistics

## Introduction 

The aim of the project is to create an Streaming application with Spark that connects to a Kafka cluster, reads and process the data.

## How to use the application

1. Zookeeper:

`/usr/bin/zookeeper-server-start config/zookeeper.properties`

2. Kafka server:

`/usr/bin/kafka-server-start config/server.properties`

3. Insert data into topic:

`python kafka_server.py`

4. Kafka consumer:

`kafka-console-consumer --topic "police-calls" --from-beginning --bootstrap-server localhost:9092`

5. Run Spark job:

`spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py`

## Output files

See png files attached.

1. kafka_consumer_console_output.png

2. progress_reporter_output.png

3. result_output.png
