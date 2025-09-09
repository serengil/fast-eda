from modules.core.service import CoreService
from modules.deepface.service import DeepFaceService
from modules.event.service import KafkaService
from modules.commons.logger import Logger
from dependencies.variables import Variables


class Container:
    def __init__(self, variables: Variables):
        self.logger = Logger()
        self.deepface_service = DeepFaceService(
            logger=self.logger,
            detector_backend=variables.detector_backend,
        )
        self.event_service = KafkaService(
            logger=self.logger,
            server_uri=variables.kafka_uri,
        )

        for topic_name in variables.topics:
            self.event_service.create_topic_if_not_exists(
                topic_name=topic_name
            )

        self.core_service = CoreService(
            logger=self.logger,
            deepface_service=self.deepface_service,
            event_service=self.event_service,
            is_eda_activated=variables.is_eda_activated,
        )

        self.logger.info("Container initialized")
