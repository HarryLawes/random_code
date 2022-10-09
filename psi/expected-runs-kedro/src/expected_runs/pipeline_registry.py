"""Project pipelines."""
from typing import Dict

from kedro.pipeline import Pipeline, pipeline
from expected_runs.pipelines import model, preprocessing, player_ratings


def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from a pipeline name to a ``Pipeline`` object.
    """
    
    preprocessing_pipeline = preprocessing.create_pipeline()
    model_pipeline = model.create_pipeline()
    player_ratings_pipeline = player_ratings.create_pipeline()
    
    return {
        "preprocessing": preprocessing_pipeline,
        "model": model_pipeline,
        "player_ratings": player_ratings_pipeline,
        "__default__": preprocessing_pipeline + model_pipeline + player_ratings_pipeline
        }
