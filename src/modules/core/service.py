# built-in dependencies
import base64
import uuid
from typing import Optional, Union

# 3rd party dependencies
import numpy as np

# project dependencies
from modules.deepface.service import DeepFaceService
from modules.event.service import KafkaService
from modules.commons.logger import Logger


class CoreService:
    def __init__(
        self,
        logger: Logger,
        deepface_service: DeepFaceService,
        event_service: KafkaService,
        is_eda_activated: bool,
    ):
        self.logger = logger
        self.deepface_service = deepface_service
        self.event_service = event_service
        self.is_eda_activated = is_eda_activated
        self.logger.debug(f"EDA activated: {self.is_eda_activated}")

    def analyze(self, image: str, request_id: str):
        faces = self.deepface_service.extract_faces(image)
        self.logger.info(f"extracted {len(faces)} faces")

        # traditional approach
        if self.is_eda_activated is False:
            for idx, face in enumerate(faces):
                self.analyze_extracted_face(
                    request_id=request_id,
                    face_index=idx,
                    face_id=uuid.uuid4().hex,
                    face=face,
                )
            self.logger.info(f"analyzed {len(faces)} faces")
        else:
            for idx, face in enumerate(faces):
                encoded_face = base64.b64encode(face.tobytes()).decode("utf-8")
                self.event_service.produce(
                    topic_name="faces.extracted",
                    key="extracted_face",
                    value={
                        "face_id": uuid.uuid4().hex,
                        "face_index": idx,
                        "encoded_face": encoded_face,
                        "request_id": request_id or "N/A",
                        "shape": face.shape,
                    },
                )
                self.logger.info(
                    f"{idx+1}-th face sent to kafka topic faces.extracted"
                )

    def analyze_extracted_face(
        self,
        request_id: str,
        face_index: int,
        face_id: str,
        face: Union[np.ndarray, str],
        shape: Optional[tuple] = None,
    ):
        if isinstance(face, str):
            if shape is None:
                raise ValueError(
                    "shape is required when face is base64 string"
                )

            decoded_face = base64.b64decode(face)
            face = np.frombuffer(decoded_face, dtype=np.float64).reshape(shape)

        demography = self.deepface_service.analyze(face)
        self.logger.info(
            f"{face_index+1}-th face analyzed: {demography['age']} years old "
            f"{demography['dominant_gender']} "
        )
