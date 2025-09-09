# built-in dependencies
from typing import List

# 3rd party dependencies
from deepface import DeepFace
import numpy as np

# project dependencies
from modules.commons.logger import Logger


class DeepFaceService:
    def __init__(self, detector_backend: str, logger: Logger):
        self.logger = logger

        self.detector_backend = detector_backend

        _ = DeepFace.build_model(
            task="face_detector",
            model_name=detector_backend,
        )
        self.logger.debug(f"detector backend {detector_backend} built")

        self.age = DeepFace.build_model(
            task="facial_attribute",
            model_name="Age",
        )
        self.logger.debug("age model built")

        self.gender = DeepFace.build_model(
            task="facial_attribute",
            model_name="Gender",
        )
        self.logger.debug("gender model built")

    def extract_faces(self, image: str) -> List[np.ndarray]:
        results = []
        face_objs = DeepFace.extract_faces(
            img_path=image,
            detector_backend=self.detector_backend,
            enforce_detection=False,
        )
        for face_obj in face_objs:
            face = face_obj["face"]
            results.append(face)
        return results

    def analyze(self, image: np.ndarray) -> dict:
        results = DeepFace.analyze(
            img_path=image,
            detector_backend="skip",
            enforce_detection=False,
            actions=["age", "gender"],
            silent=True,
        )
        return results[0]
