
import base64
import json
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, Field, ValidationError

load_dotenv(Path(__file__).with_name(".env"))

app = FastAPI(
    title="CropCheck AI API",
    description="AI-assisted crop symptom analysis and inspection guidance.",
    version="1.0.0",
)

MAX_IMAGE_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}


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


@app.get("/")
def home():
    return {"message": "CropCheck AI backend is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post(
    "/api/analyze-crop",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        413: {"model": ErrorResponse},
        502: {"model": ErrorResponse},
        503: {"model": ErrorResponse},
    },
)
async def analyze_crop(
    photo: UploadFile = File(...),
    symptoms: str = Form(...),
    crop_name: str = Form(default=""),
):
    if not symptoms.strip():
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Symptoms must not be empty.",
                "code": "EMPTY_SYMPTOMS",
            },
        )

    if photo.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Upload a JPEG, PNG, or WebP image.",
                "code": "INVALID_IMAGE_TYPE",
            },
        )

    image_bytes = await photo.read(MAX_IMAGE_SIZE + 1)

    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "The uploaded image is empty.",
                "code": "EMPTY_IMAGE",
            },
        )

    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=413,
            detail={
                "error": "Image must be 5 MB or smaller.",
                "code": "IMAGE_TOO_LARGE",
            },
        )

    api_key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not api_key or api_key == "put_your_api_key_here":
        raise HTTPException(
            status_code=503,
            detail={
                "error": "AI service is not configured.",
                "code": "AI_NOT_CONFIGURED",
            },
        )

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = (
        f"data:{photo.content_type};base64,{image_b64}"
    )

    prompt = f"""
You are CropCheck AI, a cautious crop symptom assistant.

Crop name: {crop_name.strip() or "Unknown"}
Farmer's symptoms: {symptoms.strip()}

Analyze the supplied crop image together with the symptoms.
Return preliminary guidance, not a definitive diagnosis.
Never invent evidence or confidence percentages.
If evidence is insufficient, say so in possible_causes and set
needs_expert_review to true.
Do not prescribe pesticides, chemical dosages, or unsafe treatments.
Give practical visual checks and conservative next steps.
Recommend local agricultural expert review when appropriate.

Return ONLY a valid JSON object with exactly this structure:
{{
  "possible_causes": [
    {{
      "name": "Possible cause or insufficient information",
      "reason": "Why this possibility may fit the evidence",
      "what_to_check": ["Specific thing to inspect"]
    }}
  ],
  "inspection_checklist": ["Inspection step"],
  "safe_next_steps": ["Conservative next step"],
  "needs_expert_review": true
}}

Include no more than 3 possible causes.
All what_to_check values must be lists of strings.
All checklist and next-step values must be lists of strings.
needs_expert_review must be a boolean.
"""

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
            timeout=45.0,
            max_retries=1,
        )

        result = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": image_url},
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
            max_tokens=1200,
        )

        content = result.choices[0].message.content
        if not content:
            raise ValueError("Empty AI response")

        data = json.loads(content)
        analysis = AnalysisResponse.model_validate(data)

        return analysis

    except (OpenAIError, ValueError, json.JSONDecodeError, ValidationError):
        raise HTTPException(
            status_code=502,
            detail={
                "error": (
                    "AI analysis failed. Please retry or seek "
                    "expert agricultural advice."
                ),
                "code": "AI_ANALYSIS_FAILED",
            },
        )
    except Exception:
        raise HTTPException(
            status_code=502,
            detail={
                "error": "Unexpected analysis error. Please try again.",
                "code": "AI_ANALYSIS_FAILED",
            },
        )
