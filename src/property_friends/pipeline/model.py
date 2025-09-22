from typing import Iterable 

from category_encoders import TargetEncoder 
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline

from property_friends.config.training import ModelConfig 

def build_model_pipeline(categorical_columns: Iterable[str], model_config: ModelConfig) -> Pipeline:
    """Build a machine learning pipeline with preprocessing and model.

    Args:
        categorical_columns: List of names of categorical columns to be encoded.
        model_config: ModelConfig object containing model hyperparameters.

    Returns:
        A sklearn Pipeline object that includes preprocessing and the model.
    """
    categorical_transformer = TargetEncoder()

    preprocessor = ColumnTransformer(
        transformers=[
            ('categorical',
            categorical_transformer,
            categorical_columns)
        ])

    model = GradientBoostingRegressor(**model_config.dict())
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    return pipeline