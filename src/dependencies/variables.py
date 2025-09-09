# built-in dependencies
import os


# pylint: disable=too-few-public-methods
class Variables:
    def __init__(self):
        self.kafka_uri = os.getenv("KAFKA_URI", "CHANGEME")
        self.detector_backend = os.getenv("DETECTOR_BACKEND", "opencv")
        self.is_eda_activated = os.getenv("EDA_ACTIVATED", "0") == "1"
        self.topics = ["faces.extracted"]
