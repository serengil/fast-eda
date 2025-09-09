# 3rd party dependencies
from faststream import FastStream
from faststream.kafka import KafkaBroker

# project dependencies
from dependencies.container import Variables

variables = Variables()

broker = KafkaBroker(variables.kafka_uri)
faststream_app = FastStream(broker)
