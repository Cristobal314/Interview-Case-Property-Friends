from typing import Dict 

import numpy as np 
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error

def regression_metrics(y_true, y_pred) -> Dict[str, float]: 
    """Calculate common regression metrics.

    Args:
        y_true: True target values.
        y_pred: Predicted target values.

    Returns:
        Dictionary with MAE, MAPE, and RMSE.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {
        "mae": mae,
        "mape": mape,
        "rmse": rmse
    }