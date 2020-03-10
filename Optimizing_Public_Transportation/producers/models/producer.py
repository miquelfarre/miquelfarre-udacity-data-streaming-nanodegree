"""Producer base-class providing common utilites and functionality"""
import logging
import time

from confluent_kafka import avro
from confluent_kafka.admin import AdminClient, NewTopic
from confluent_kafka.avro import AvroProducer

logger = logging.getLogger(__name__)


class Producer:
    """Defines and provides common functionality amongst Producers"""

    # Tracks existing topics across all Producer instances
    existing_topics = set([])

    def __init__(
        self,
        topic_name,
        key_schema,
        value_schema=None,
        num_partitions=1,
        num_replicas=1,
    ):
        """Initializes a Producer object with basic settings"""
        self.topic_name = topic_name
        self.key_schema = key_schema
        self.value_schema = value_schema
        self.num_partitions = num_partitions
        self.num_replicas = num_replicas

        self.broker_properties = {
            "bootstrap.servers": "PLAINTEXT://localhost:9092",
            "schema.registry.url": "http://localhost:8081"
        }

        # If the topic does not already exist, try to create it
        if self.topic_name not in Producer.existing_topics:
            self.create_topic()
            Producer.existing_topics.add(self.topic_name)

        self.producer = AvroProducer(
            self.broker_properties,
            default_key_schema=key_schema,
            default_value_schema=value_schema
        )

    def create_topic(self):
        #Creates the producer topic if it does not already exist
        client = AdminClient(
            {"bootstrap.servers": self.broker_properties["bootstrap.servers"]}
        )

        #Check if topic exists in client topic list
        topicList = client.list_topics()

        if self.topic_name in topicList.topics:
            logger.info(f'Topic {self.topic_name} exists in client. Topic will not be created. Finishing process.')
            return
                
        #Does not exist, log, create and contimue
        logger.info(f"Creating topic: {self.topic_name}")

        futures = client.create_topics(
        [
            NewTopic(
            topic=self.topic_name,
            num_partitions=self.num_partitions,
            replication_factor=self.num_replicas)
        ])

        for topic, future in futures.items():
            try:
                future.result()
                logger.info(f"{self.topic_name} topic creation complete")
            except Exception as e:
                logger.fatal(f"unable to create topic {topic} with topic name: {self.topic_name} with exception: {e}")

    def close(self):
        """Prepares the producer for exit by cleaning up the producer"""
        if self.producer is not None:
            logger.debug("flushing producer.")
            self.producer.flush()

    def time_millis(self):
        """Use this function to get the key for Kafka Events"""
        return int(round(time.time() * 1000))
