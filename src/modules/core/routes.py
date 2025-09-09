# built-in dependencies
import uuid
import traceback

# 3rd party dependencies
from fastapi import APIRouter, BackgroundTasks, HTTPException, Depends
from fastapi.responses import HTMLResponse

from pydantic import BaseModel
from faststream import Depends as FastStreamDepends

# project dependencies
from dependencies.container import Container
from modules.core.bus import broker
from dependencies.variables import Variables
from dependencies.container import Container

router = APIRouter()


def get_container() -> Container:
    variables = Variables()
    return Container(variables=variables)


@router.get("/", response_class=HTMLResponse)
def home():
    return "<h1>Welcome to EDA Service!</h1>"


class AnalyzeRequest(BaseModel):
    image: str


@router.post("/analyze")
async def analyze(
    payload: AnalyzeRequest,
    background_tasks: BackgroundTasks,
    # container: Container = Depends(get_container), # via FastAPI Depends
):
    container: Container = router.container  # directly attachted to router
    container.logger.info("POST /analyze endpoint is called")

    request_id = uuid.uuid4().hex

    background_tasks.add_task(
        container.core_service.analyze,
        image=payload.image,
        request_id=request_id,
    )

    return {
        "result": True,
        "message": "image will be processed in background",
        "request_id": request_id,
    }


class AnalyzeExtractedFaceRequest(BaseModel):
    face_id: str
    request_id: str
    face_index: int
    encoded_face: str
    shape: tuple


@broker.subscriber("faces.extracted")
async def analyze_extracted_face_kafka(
    input_value: AnalyzeExtractedFaceRequest,
    # container: Container = FastStreamDepends(get_container),  # via FastAPI Depends
):
    container: Container = router.container  # directly attachted to router

    try:
        container.core_service.analyze_extracted_face(
            face_id=input_value.face_id,
            request_id=input_value.request_id,
            face_index=input_value.face_index,
            face=input_value.encoded_face,
            shape=input_value.shape,
        )
        return {"status": "ok", "message": "single face analyzed"}
    except (
        Exception
    ) as err:  # pylint: disable=broad-exception-caught, raise-missing-from
        container.logger.error(
            f"Exception while analyzing single face - {err}"
        )
        container.logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(err))
