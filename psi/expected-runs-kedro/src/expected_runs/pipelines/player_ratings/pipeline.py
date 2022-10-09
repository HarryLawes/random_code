"""
This is a boilerplate pipeline 'player_ratings'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import get_all_predictions, calculate_match_performance, get_player_ratings


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=get_all_predictions, 
                inputs=["test_data", "first_model", "second_model"],
                outputs="predictions",
                name="get_all_predictions"
            ),
            node(
                func=calculate_match_performance, 
                inputs=["predictions","value_of_wicket"],
                outputs=["bat_performance","bowl_performance"],
                name="calculate_match_performance"
            ),
            node(
                func=get_player_ratings, 
                inputs=["bat_performance","bowl_performance"],
                outputs=["bat_ratings","bowl_ratings"],
                name="get_player_ratings"
            ),
    ])
