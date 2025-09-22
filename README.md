# Property Friends - Real Estate Valuation API

## Overview

Property Friends is a production-ready machine learning service for real estate property valuation in Chile. This project transforms an experimental Jupyter notebook into a robust, scalable API service following software engineering best practices.

The solution provides a RESTful API that receives property characteristics and returns accurate valuation predictions based on a Gradient Boosting Regressor model trained on Chilean real estate data.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Assumptions](#assumptions)
- [Future Improvements](#future-improvements)
- [Technical Requirements Met](#technical-requirements-met)

## Features

- **Production-Ready ML Pipeline**: Modular, maintainable training pipeline with clear separation of concerns
- **RESTful API**: FastAPI-based service with automatic documentation
- **Security**: API key authentication for all prediction endpoints
- **Containerization**: Full Docker support for consistent deployment
- **Logging**: Comprehensive logging system using Loguru for model monitoring
- **Configuration Management**: YAML-based configuration for easy parameter tuning
- **Data Source Abstraction**: Extensible architecture for future database integrations

## Architecture

The application follows a modular architecture with clear separation between:

- **Data Layer**: Abstract data sources with CSV implementation (extensible for databases)
- **Training Pipeline**: Configurable ML pipeline with preprocessing and model training
- **Service Layer**: Model service for lazy loading and prediction handling
- **API Layer**: FastAPI application with schema validation and security
- **CLI Interface**: Command-line tools for training and API server management

## Prerequisites

- Python 3.10+
- Docker 
- Training data files: `data/train.csv` and `data/test.csv`

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Cristobal314/Interview-Case-Property-Friends.git
cd property-friends
```

### 2. Set Up Environment Variables

Create a `.env` file based on the provided example:

```bash
cp .env.example .env
```

Edit `.env` and set your API key:

```env
PROPERTY_FRIENDS_API_KEY=your-secure-api-key-here
PROPERTY_FRIENDS_MODEL_PATH=artifacts/model.joblib
PROPERTY_FRIENDS_FEATURE_STORE_PATH=artifacts/feature_columns.json
```

### 3. Prepare Training Data

Place your training and test CSV files in the `data/` directory:

```bash
mkdir -p data
# Copy your train.csv and test.csv files to data/
```

### 4. Build Docker Image

```bash
docker-compose build
```

## Usage

### Training the Model

Before running the API, you must train the model:

```bash
# Using Docker
docker-compose run --rm api train

# Or locally (requires pip install -e .)
property-friends train
```

This will:
- Load data from CSV files
- Train the Gradient Boosting model
- Save the model and metrics to the `artifacts/` directory
- Generate a feature store for validation

### Starting the API Server

```bash
# Using Docker Compose (recommended)
docker-compose up

# Or locally
property-friends api --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Making Predictions

#### Using cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: your-secure-api-key-here" \
  -d '{
    "type": "casa",
    "sector": "Las Condes",
    "net_usable_area": 120.0,
    "net_area": 150.0,
    "n_rooms": 3,
    "n_bathroom": 2,
    "latitude": -33.4489,
    "longitude": -70.6693
  }'
```

#### Using Python

```python
import requests

url = "http://localhost:8000/predict"
headers = {
    "Content-Type": "application/json",
    "X-API-KEY": "your-secure-api-key-here"
}
data = {
    "type": "casa",
    "sector": "Las Condes",
    "net_usable_area": 120.0,
    "net_area": 150.0,
    "n_rooms": 3,
    "n_bathroom": 2,
    "latitude": -33.4489,
    "longitude": -70.6693
}

response = requests.post(url, json=data, headers=headers)
print(f"Predicted price: ${response.json()['price']:,.0f}")
```

## API Documentation

### Interactive Documentation

Once the server is running, access the interactive API documentation at:

-  `http://localhost:8000/docs`

### Endpoints

#### Health Check

```http
GET /health
```

Returns the API health status. No authentication required.

#### Prediction

```http
POST /predict
```

**Headers:**
- `Content-Type: application/json`
- `X-API-KEY: {your-api-key}`

**Request Body:**
```json
{
  "type": "string",
  "sector": "string",
  "net_usable_area": "number",
  "net_area": "number",
  "n_rooms": "integer",
  "n_bathroom": "integer",
  "latitude": "number",
  "longitude": "number"
}
```

**Response:**
```json
{
  "price": "number"
}
```

## Configuration

### Training Configuration

Edit `config/training.yaml` to adjust model parameters:

```yaml
target: price
categorical_columns:
  - type
  - sector
drop_columns: []
model:
  learning_rate: 0.01
  n_estimators: 300
  max_depth: 5
  loss: absolute_error
```

### API Configuration

Environment variables in `.env`:

- `PROPERTY_FRIENDS_API_KEY`: API authentication key
- `PROPERTY_FRIENDS_MODEL_PATH`: Path to trained model
- `PROPERTY_FRIENDS_FEATURE_STORE_PATH`: Path to feature configuration

## Project Structure

```
property-friends/
├── src/property_friends/
│   ├── api/              # API layer (FastAPI app, schemas, config)
│   ├── config/           # Configuration management
│   ├── data_sources/     # Abstract data source implementations
│   ├── evaluation/       # Model evaluation metrics
│   ├── pipeline/         # ML pipeline components
│   ├── service/          # Model service layer
│   ├── training/         # Training pipeline orchestration
│   └── cli.py           # Command-line interface
├── config/
│   └── training.yaml    # Training configuration
├── notebooks/           # Original Jupyter notebook
├── artifacts/           # Generated models and metadata
├── data/               # Training and test data (gitignored)
├── docker-compose.yml  # Docker orchestration
├── Dockerfile         # Container definition
├── pyproject.toml     # Project dependencies
└── README.md         # This file
```

## Assumptions

The following assumptions were made during development:

1. **Data Schema Consistency**: Training and test files share the same schema and include the target variable named `price`.

2. **Feature Stability**: Future data sources should maintain the same set of columns. New fields should be explicitly added to either `categorical_columns` or `drop_columns` in the configuration as required.

3. **Data Availability**: The model assumes all features will be available at prediction time. Missing values are not handled in the current implementation.

4. **Geographic Scope**: The model is specifically trained for Chilean real estate properties and may not generalize to other markets.

5. **Currency**: All price predictions are in the same currency as the training data (assumed to be CLP).

## Future Improvements

The following improvements were identified but not implemented due to the 5-hour time constraint:

### Infrastructure
- **Infrastructure as Code**: Implement Terraform modules for cloud deployment (AWS/GCP/Azure)
- **Container Orchestration**: Kubernetes manifests for production-grade deployment
- **Load Balancing**: Implement horizontal scaling with load balancer

### MLOps
- **Model Registry**: Integrate MLflow for experiment tracking and model versioning
- **Retraining Pipeline**: Automated retraining workflow with data drift detection
- **A/B Testing**: Infrastructure for model comparison and gradual rollout
- **Validation Dataset**: Separate validation set for hyperparameter tuning

### Software Engineering
- **Testing Suite**: Comprehensive unit tests, integration tests, and contract tests
- **CI/CD Pipeline**: GitHub Actions workflows for automated testing and deployment
- **API Versioning**: Implement versioned endpoints for backward compatibility

### Monitoring & Observability
- **Metrics Collection**: Prometheus metrics for model performance tracking
- **Distributed Tracing**: OpenTelemetry integration for request tracing

### Data Engineering
- **Feature Store**: Centralized feature management system
- **Data Pipeline**: Apache Airflow DAGs for data preprocessing
- **Database Integration**: Direct connection to PostgreSQL/MySQL databases
- **Data Validation**: Great Expectations for data quality checks

## Technical Requirements Met

This implementation successfully addresses all requirements specified in the challenge:

- **Dockerized Pipeline and API**: Full Docker support with docker-compose
- **Logging System**: Comprehensive logging using Loguru for future model monitoring
- **API Documentation**: Auto-generated documentation via FastAPI
- **Security**: API key authentication system implemented
- **Data Source Abstraction**: Factory pattern for future database integrations
- **Best Practices**: Modular architecture, error handling, type hints, and documentation
- **Scalability**: Design supports horizontal scaling and future extensions