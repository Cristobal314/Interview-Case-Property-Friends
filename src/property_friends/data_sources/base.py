from abc import ABC, abstractmethod 
from typing import Tuple 
import pandas as pd 

class DataSource(ABC): 
    """Abstract base class for data sources."""
    @abstractmethod
    def load(self) -> Tuple[pd.DataFrame, pd.DataFrame]: 
        """Load training and testing data.

        Returns:
            A tuple containing the training and testing DataFrames.
        """