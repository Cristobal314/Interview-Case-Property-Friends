from pathlib import Path 
from typing import List, Literal, Optional 
from pydantic import BaseModel, Field, validator

class DataSourceConfig(BaseModel):
    """Config to describe where to load the training data from."""

    type: Literal["csv"] = "csv" 
    train_path: Path 
    test_path: Path

    @validator("train_path", "test_path")
    def _ensure_paths(cls, value:Path) -> Path: 
        if not value: 
            raise ValueError("Data path must be provided.") 
        return value

class ModelConfig(BaseModel):
    """Hyperparameters used to instantiate the model."""
    
    learning_rate: float = 0.01
    n_estimators: int = 300
    max_depth: int = 5
    loss: str = "absolute_error"

class TrainingConfig(BaseModel): 
    """Configuration for the training pipeline."""
    
    target: str
    categorical_columns: List[str]
    drop_columns: List[str] = Field(default_factory=list)
    data_source: DataSourceConfig
    model: ModelConfig = Field(default_factory=ModelConfig)
    artifacts_dir: Path = Path("artifacts")
    model_filename: str = "model.joblib"
    metrics_filename: str = "metrics.json"
    feature_store_filename: str = "feature_columns.json"

    class Config: 
        arbitrary_types_allowed = True 
    
    @property
    def model_path(self) -> Path: 
        return Path(self.artifacts_dir) / self.model_filename

    @property
    def metrics_path(self) -> Path: 
        return Path(self.artifacts_dir) / self.metrics_filename
    
    @property
    def feature_store_path(self) -> Path: 
        return Path(self.artifacts_dir) / self.feature_store_filename
    
def load_training_config(config_path: Path) -> TrainingConfig: 
    """Load :class:`TrainingConfig` from a YAML file."""
    import yaml 
    with Path(config_path).open("r", encoding="utf-8") as f: 
        config_dict = yaml.safe_load(f)
    return TrainingConfig(**config_dict)