# built-in dependencies
import random
import json
from json import dumps

# 3rd party dependencies
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

# project dependencies
from modules.commons.logger import Logger


class KafkaService:
    def __init__(self, server_uri: str, logger: Logger):
        self.logger = logger
        self.producer = KafkaProducer(
            bootstrap_servers=[server_uri],
            ssl_check_hostname=False,
            key_serializer=str.encode,
            value_serializer=lambda x: dumps(x).encode("utf-8"),
            max_request_size=3173440261,
            api_version=(0, 11, 5),
        )

        self.admin_client = KafkaAdminClient(bootstrap_servers=server_uri)

    def create_topic_if_not_exists(
        self, topic_name: str, num_partitions: int = 8
    ):
        if topic_name not in self.admin_client.list_topics():
            try:
                new_topic = NewTopic(
                    topic_name,
                    num_partitions=num_partitions,
                    replication_factor=1,
                )
                self.admin_client.create_topics([new_topic])
                self.logger.info(f"Topic {topic_name} created")
            except TopicAlreadyExistsError:
                pass

    def produce(
        self,
        topic_name: str,
        key: str,
        value: dict,
        partitions: int = 8,
        sync: bool = False,
    ):
        target_partition = random.randint(0, max(0, partitions - 1))
        future = self.producer.send(
            topic_name,
            key=json.dumps(key),
            value=value,
            partition=target_partition,
        )
        metadata = future.get(timeout=20)
        self.logger.debug(metadata)
        if sync is True:
            self.producer.flush()  # to make it sync instead of async
