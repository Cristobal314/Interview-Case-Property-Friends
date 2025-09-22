import json 
from pathlib import Path

import typer 

from property_friends.config.training import TrainingConfig, load_training_config
from property_friends.training.pipeline_runner import run_training_pipeline

app = typer.Typer(help="Utility to run the training pipeline for Property Friends.") 

@app.command()
def train(config: Path = typer.Argument(Path("config/training.yaml"), exists=True, readable=True, help="Path to the training config file")) -> None: 
    """Run the training pipeline with the specified configuration."""
    training_config: TrainingConfig = load_training_config(config)
    result = run_training_pipeline(training_config) 
    typer.echo("Training finished successfully.")

@app.command()
def api(
    host: str = typer.Option("0.0.0.0", help="Host to bind the API server to"),
    port: int = typer.Option(8000, help="Port to bind the API server to"),
    reload: bool = typer.Option(False, help="Enable auto-reload for development"),
) -> None: 
    """Start the API server."""
    import uvicorn

    uvicorn.run("property_friends.api.main:create_app", host=host, port=port, reload=reload, factory=True)

def main() -> None: 
    app()