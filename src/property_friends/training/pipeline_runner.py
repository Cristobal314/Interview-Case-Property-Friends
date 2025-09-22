import json 
from loguru import logger
from pathlib import Path 
from typing import List, Dict
import joblib 
import pandas as pd 

# TODO: Property friends will have: config, data_sources, evaluation and pipeline
from property_friends.config.training import TrainingConfig
from property_friends.data_sources.factory import build_data_source
from property_friends.pipeline.model import build_model_pipeline
from property_friends.evaluation.metrics import regression_metrics