import json 
from loguru import logger 
from pathlib import Path
from typing import Any, Dict, List 
import joblib 
import pandas as pd 

class ModelService:
    """Lazy Load of the trained model and provide prediction service"""
    def __init__(self, model_path: Path, feature_store_path:  Path) -> None: 
        self._model_path = Path(model_path)
        self._feature_store_path = Path(feature_store_path)
        self._pipeline = None 
        self._features: List[str] | None = None

    def load(self) -> None: 
        if self._pipeline is not None and self._features is not None: 
            logger.info("Model and feature store already loaded.")
            return
        if not self._model_path.exists():
            raise FileNotFoundError(f"Model file not found at {self._model_path}")
        if not self._feature_store_path.exists():
            raise FileNotFoundError(f"Feature store file not found at {self._feature_store_path}")
        logger.info(f"Loading model from {self._model_path}")
        self._pipeline = joblib.load(self._model_path)
        
        logger.info(f"Loading feature store from {self._feature_store_path}")
        with open(self._feature_store_path, "r") as f: 
            payload = json.load(f) 
        features = payload.get("features")
        if not isinstance(features, list): 
            raise ValueError("Feature store file is malformed or missing 'features' key.")
        self._features = features
        logger.info("Model and feature store loaded successfully.")
    
    @property
    def features(self) -> List[str]: 
        if self._features is None: 
            self.load()
        assert self._features is not None
        return self._features
    
    def predict(self, payload: Dict[str, Any]) -> float:
        if self._pipeline is None: 
            self.load() 
        assert self._pipeline is not None

        frame = pd.DataFrame([payload])
        missing = set(self.features) - set(frame.columns) 
        if missing: 
            raise ValueError(f"Missing features in payload: {missing}")
        ordered_frame = frame[self.features]
        prediction = float(self._pipeline.predict(ordered_frame)[0])
        logger.info(f"Prediction: {prediction} for payload: {payload}")
        return prediction
        

        