
from typing import List

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
app = FastAPI(
    title="CropCheck AI API",
    description="AI-assisted crop symptom analysis and inspection guidance.",
    version="1.0.0",
)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        error = exc.detail.get("error", "Request failed.")
        code = exc.detail.get("code", "REQUEST_ERROR")
    else:
        error = str(exc.detail)
        code = "REQUEST_ERROR"

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error, "code": code},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Please provide all required fields with valid values.",
            "code": "INVALID_REQUEST",
        },
    )



class PossibleCause(BaseModel):
    name: str
    reason: str
    what_to_check: List[str]


class AnalysisResponse(BaseModel):
    possible_causes: List[PossibleCause] = Field(max_length=3)
    inspection_checklist: List[str]
    safe_next_steps: List[str]
    needs_expert_review: bool


class ErrorResponse(BaseModel):
    error: str
    code: str


@app.get("/")
def home():
    return {"message": "CropCheck AI backend is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/api/analyze-crop",
    response_model=AnalysisResponse,
    responses={400: {"model": ErrorResponse}, 413: {"model": ErrorResponse}},
)
async def analyze_crop(
    photo: UploadFile = File(...),
    symptoms: str = Form(...),
    crop_name: str = Form(default=""),
):
    if not symptoms.strip():
        raise HTTPException(
            status_code=400,
            detail={"error": "Symptoms must not be empty.", "code": "EMPTY_SYMPTOMS"},
        )

    if photo.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(
            status_code=400,
            detail={"error": "Upload a JPEG, PNG, or WebP image.", "code": "INVALID_IMAGE_TYPE"},
        )

    image_bytes = await photo.read()

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail={"error": "The uploaded image is empty.", "code": "EMPTY_IMAGE"},
        )

    if len(image_bytes) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail={"error": "Image must be 5 MB or smaller.", "code": "IMAGE_TOO_LARGE"},
        )

    # AI integration will be added in the next step.
    raise HTTPException(
        status_code=503,
        detail={
            "error": "Crop analysis is not available yet.",
            "code": "AI_NOT_CONFIGURED",
        },
    )
