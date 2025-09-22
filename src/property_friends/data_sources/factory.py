from property_friends.config.training import DataSourceConfig
from .base import DataSource 
from .csv_source import CSVDataSource
from loguru import logger
def build_data_source(config: DataSourceConfig) -> DataSource:
    """Factory function to create a data source based on the configuration.

    Args:
        config: DataSourceConfig object containing the data source configuration.

    Returns:
        An instance of a DataSource subclass.
    """
    logger.debug(f"Building data source with config: {config}")
    if config.type == "csv":
        return CSVDataSource(train_path=config.train_path, test_path=config.test_path)
    else:
        logger.info("Here you can add more data source types in the future!.")
        raise ValueError(f"Unsupported data source type: {config.type}")