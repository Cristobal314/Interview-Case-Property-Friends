from functools import lru_cache
from pathlib import Path 

from pydantic import BaseSettings, Field 

class APISettings(BaseSettings): 
    """Configuration for the Property Friends API."""
    model_path: Path = Field(
        default=Path("artifacts/model.joblib"), 
        description="Path to the trained model file.")
    feature_store_path: Path = Field(
        default=Path("artifacts/feature_columns.json"), 
        description="Path to the feature columns file.")
    api_key: str = Field(..., 
        description="API key for authenticating requests.")
    
    class Config: 
        env_prefix = "PROPERTY_FIENDS_"
        env_file = ".env"

@lru_cache()
def get_settings() -> APISettings: 
    """Get cached API settings."""
    return APISettings()
