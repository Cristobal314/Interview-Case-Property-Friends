import json 
from loguru import logger
from pathlib import Path 
from typing import List, Dict
import joblib 
import pandas as pd 

# TODO: Property friends will have: config, data_sources, evaluation and pipeline
from property_friends.config.training import TrainingConfig