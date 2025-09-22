from pydantic import BaseModel, Field

class PredictionRequest(BaseModel):
    """Schema for prediction request."""
    type: str = Field(..., description="Property type, e.g. 'casa' or 'departamento'.")
    sector: str = Field(..., description="Sector or neighborhood of the property.")
    net_usable_area: float = Field(..., description="Net usable area in square meters.")
    net_area: float = Field(..., description="Net area in square meters.")
    n_rooms: int = Field(..., description="Number of rooms.")
    n_bathrooms: int = Field(..., description="Number of bathrooms.")
    latitude: float = Field(..., description="Latitude coordinate of the property.")
    longitude: float = Field(..., description="Longitude coordinate of the property.")

class PredictionResponse(BaseModel):
    """Schema for prediction response."""
    price: float = Field(..., description="Predicted price of the property.")