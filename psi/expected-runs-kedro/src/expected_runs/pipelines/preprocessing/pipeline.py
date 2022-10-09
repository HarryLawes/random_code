"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.2
"""

from kedro.pipeline import Pipeline, node, pipeline
from .nodes import exclude_non_t20s, exclude_certain_matches, exclude_anomalies,\
                            prepare_features, train_test_split

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [ 
            node(
                func=exclude_non_t20s, 
                inputs="all_matches",
                outputs="t20s",
                name="exclude_non_t20s"
            ),
            node(
                func=exclude_certain_matches, 
                inputs="t20s",
                outputs="selected_matches",
                name="exclude_certain_matches"
            ),
            node(
                func=exclude_anomalies, 
                inputs="selected_matches",
                outputs="clean_matches",
                name="exclude_anomalies"
            ),
            node(
                func=prepare_features, 
                inputs="clean_matches",
                outputs="features",
                name="prepare_features"
            ),
            node(
                func=train_test_split, 
                inputs="features",
                outputs=["train_data", "test_data"],
                name="train_test_split"
            ),
        ]
    )
