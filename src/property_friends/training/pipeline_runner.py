import json 
from loguru import logger
from pathlib import Path 
from typing import List, Dict
import joblib 
import pandas as pd 

from property_friends.config.training import TrainingConfig
from property_friends.data_sources.factory import build_data_source
from property_friends.pipeline.model import build_model_pipeline
from property_friends.evaluation.metrics import regression_metrics

def _resolve_feaure_columns(dataset:pd.DataFrame, config: TrainingConfig) -> List[str]:
    """Determine the feature columns by excluding target and drop columns."""
    all_columns = list(dataset.columns)
    excluded = set(config.drop_columns + [config.target])
    feature_columns = [
        col for col in all_columns 
        if col not in excluded
    ]
    missing = set(config.categorical_columns) - set(feature_columns)
    if missing: 
        raise ValueError(f"Categorical columns {missing} not found in dataset columns.")
    logger.debug(f"Resolved feature columns: {feature_columns}")
    return feature_columns

def _ensure_artifact_directory(config: TrainingConfig) -> None:
    """Create the artifacts directory if it doesn't exist."""
    artifact_dir = Path(config.artifacts_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured artifact directory exists at: {artifact_dir}")

def _persist_artifacts(pipeline, features:List[str], metrics:Dict[str, float], config: TrainingConfig) -> None:
    _ensure_artifact_directory(config)

    joblib.dump(pipeline, config.model_path)
    logger.info(f"Saved model pipeline to {config.model_path}")
    with config.feature_store_path.open("w", encoding="utf-8") as f: 
        json.dump({"features":features}, f, indent=2)
    logger.info(f"Saved feature columns to {config.feature_store_path}")

    with config.metrics_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    logger.info(f"Saved metrics to {config.metrics_path}")

def run_training_pipeline(config: TrainingConfig) -> Dict[str, Dict[str, float]]: 
    """Run the full training pipeline: load data, train model, evaluate, and save artifacts.
    Args:
        config: TrainingConfig object with all necessary configuration.
    Returns:
        Dictionary with training and test metrics.
    """
    logger.info("Starting training pipeline...")
    logger.debug(f"Loading datasets using {config.data_source.type}")
    data_source = build_data_source(config.data_source)
    train_df, test_df = data_source.load()

    logger.info(f"Loaded training data with shape {train_df.shape} and test data with shape {test_df.shape}")
    if config.target not in train_df.columns:
        raise ValueError(f"Target column '{config.target}' not found in training data.")    
    if config.target not in test_df.columns:
        raise ValueError(f"Target column '{config.target}' not found in test data.")
    if not set(config.categorical_columns).issubset(set(train_df.columns)):
        raise ValueError("Some categorical columns not found in training data.")
    if not set(config.categorical_columns).issubset(set(test_df.columns)):
        raise ValueError("Some categorical columns not found in test data.")
    
    feature_columns = _resolve_feaure_columns(train_df, config)
    logger.info(f"Using feature columns: {feature_columns}")
    logger.debug("Preparing training and test sets.")
    X_train = train_df[feature_columns]
    y_train = train_df[config.target]
    X_test = test_df[feature_columns]
    y_test = test_df[config.target]

    logger.info("Building and training the model pipeline.")
    pipeline = build_model_pipeline(config.categorical_columns, config.model)
    logger.info("Training the model...")
    pipeline.fit(X_train, y_train)

    logger.info("Evaluating the model...")
    predictions = pipeline.predict(X_test)
    metrics = regression_metrics(y_test, predictions)
    logger.info(f"Evaluation metrics: {metrics}")
    _persist_artifacts(pipeline, feature_columns, metrics, config) 
    logger.success("Training pipeline completed successfully.")
    
    return {"metrics":metrics, "features":feature_columns}