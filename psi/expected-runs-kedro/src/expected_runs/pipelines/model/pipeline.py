"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import train_models, get_value_of_wicket

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=train_models, 
                inputs="train_data",
                outputs=["first_model", "second_model"],
                name="train_models"
            ),
            node(
                func=get_value_of_wicket, 
                inputs="train_data",
                outputs="value_of_wicket",
                name="get_value_of_wicket"
            ),
        ])
