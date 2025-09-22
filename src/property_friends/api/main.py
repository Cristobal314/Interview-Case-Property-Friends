from loguru import logger 
from typing import Callable

from fastapi import Depends, FastAPI, HTTPException, Request, status 
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader 

from property_friends.api.config import APISettings, get_settings
from property_friends.api.schemas import PredictionRequest, PredictionResponse
# TODO: Model Service 

API_KEY_HEADER = APIKeyHeader(name="X-API-KEY", auto_error=False) 

def _verify_api_key(settings: APISettings) -> Callable[[str | None], str]: 
    def dependency(api_key:str | None = Depends(API_KEY_HEADER)) -> str: 
        if not api_key or api_key != settings.api_key: 
            logger.warning("Unauthorized access attempt with invalid API key.")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing API Key"
            )
    return dependency

def create_app() -> FastAPI: 
    """"App factory to create and configure the FastAPI application."""

    settings = get_settings()
    model_service = None  # Placeholder for the model service instance
    app = FastAPI(
        title="Property Friends Valuation API",
        description="API for property valuation predictions.",
        version="0.1.0"
    )

    @app.on_event("startup")
    async def _load_model() -> None: 
        logger.info("Starting up and loading model...")
        model_service.load_model() 

    @app.exception_handler(ValueError)
    async def _handle_value_error(_: Request, exc: ValueError) -> JSONResponse:
        logger.error(f"ValueError: {exc}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)}
        )
    
    api_key_verification = _verify_api_key(settings)

    @app.get("/health", tags=["Health"])
    async def health() -> dict[str, str]: 
        return {"status": "ok"}
    
    @app.post("/predict", response_model=PredictionResponse, tags=["Predictions"])
    async def predict(
        payload: PredictionRequest,
        _: str = Depends(api_key_verification)
    ) -> PredictionResponse: 
        try: 
            logger.info(f"Received prediction request {payload.dict()}")
            prediction = model_service.predict(payload.dict())
            return PredictionResponse(price=prediction)
        except Exception as e: 
            logger.error(f"Prediction error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred during prediction."
            )
    
    return app 
