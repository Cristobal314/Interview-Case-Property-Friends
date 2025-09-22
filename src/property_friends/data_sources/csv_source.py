from pathlib import Path 
from typing import Tuple 

import pandas as pd 
from loguru import logger

from .base import DataSource

class CSVDataSource(DataSource):
    """Data source that loads data from CSV files."""
    
    def __init__(self, train_path: Path, test_path: Path) -> None: 
        self._train_path = train_path 
        self._test_path = test_path 
    
    def load(self) -> Tuple[pd.DataFrame, pd.DataFrame]: 
        """Load training and testing data from CSV files.

        Returns:
            A tuple containing the training and testing DataFrames.
        """
        if not self._train_path.exists():
            raise FileNotFoundError(f"Training file not found: {self._train_path}")
        if not self._test_path.exists():
            raise FileNotFoundError(f"Testing file not found: {self._test_path}")
        logger.info(f"Loading training data from {self._train_path}")
        train_df = pd.read_csv(self._train_path)
        logger.info(f"Loading testing data from {self._test_path}")
        test_df = pd.read_csv(self._test_path)
        return train_df, test_df