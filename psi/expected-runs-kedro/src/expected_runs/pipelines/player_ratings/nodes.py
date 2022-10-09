"""
This is a boilerplate pipeline 'player_ratings'
generated using Kedro 0.18.2
"""

import pandas as pd

def get_innings_predictions(df, model, innings):

    df = df[df['innings'] == innings]
    
    if innings == 1:
        X = df[['innings_wickets', 'batter_balls_faced', 'powerplay', 'over_number']]
    elif innings == 2:
        X = df[['innings_wickets', 'batter_balls_faced', 'powerplay', 'over_number', 'run_rate_required']]
    
    y = df['score_value']
    X['pred'] = model.predict(X)
    X['actual'] = y

    results = X.merge(
            df[['event_id','batsman_striker_name', 'bowler_name', 'innings', 'outcome',
                'date', 'middle', 'death', 'wicket', 'innings_remaining_balls']],
            left_index = True, right_index = True
        )
        
    if innings == 1:
        results['run_rate_required'] = None
        
    return results

def get_all_predictions(df, first_model, second_model):
    
    results1 = get_innings_predictions(df, first_model, 1)
    results2 = get_innings_predictions(df, second_model, 2)    
    
    results = pd.concat([results1, results2])
    results['wide_multiplier'] = results['outcome'].apply(lambda x: 0 if x == 'wide' else 1)
    results['pred'] = results['pred'] * results['wide_multiplier']
    
    return results
    
def calculate_match_performance(df, value_of_wicket):
    
    df = df.merge(value_of_wicket)
    df['runs_gained_wicket'] = df['wicket'] * df['value_of_wicket']
    df['runs_gained_survival'] = (1 - df['wicket']) * df['value_of_survival']
    
    df['runs_gained'] = (df['actual'] - df['pred']) +\
                                df['runs_gained_wicket'] + df['runs_gained_survival']    
                                
    bat_performance = df.groupby(
        ['event_id', 'date', 'batsman_striker_name'], as_index=False
    ).agg(
        {'batter_balls_faced':'count', 'runs_gained':'sum'}
        ).rename(
            columns={'batsman_striker_name':'player_name'}
        )
    
    bowl_performance = df.groupby(
        ['event_id', 'date', 'bowler_name'], as_index=False
    ).agg(
        {'batter_balls_faced':'count', 'runs_gained':'sum'}
        ).rename(
            columns={'batter_balls_faced':'balls_bowled', 'bowler_name':'player_name'}
        )

    bowl_performance['runs_gained'] = bowl_performance['runs_gained'] * -1
    
    bat_performance['type'] = 'Bat'
    bowl_performance['type'] = 'Bowl'
    
    return bat_performance, bowl_performance

def smooth_rating(df, bat):
    
    df = df.sort_values('date').set_index('date')
    
    if bat:
        span = 40
    else:
        span = 50
    
    ratings = df.sort_values(
        'date'
        ).groupby(
        'player_name'
        )[['runs_gained']].ewm(
            span=span
        ).mean().groupby(
            'player_name'
        ).tail(1).sort_values(
            'runs_gained', ascending=False
        ).rename(
            columns={'runs_gained':'player_rating'}
        )
        
    return ratings

def get_player_ratings(bat_performance, bowl_performance):
    
    bat_ratings = smooth_rating(bat_performance, bat=True).reset_index()
    bowl_ratings = smooth_rating(bowl_performance, bat=False).reset_index()
    
    bat_innings = bat_performance.groupby(
        'player_name', as_index=False
        )[['runs_gained']].count().rename(
            columns={'runs_gained':'innings'}
            )
    
    bowl_innings = bowl_performance.groupby(
        'player_name', as_index=False
        )[['runs_gained']].count().rename(
            columns={'runs_gained':'innings'}
            )
    
    bat_ratings = bat_ratings.merge(bat_innings)
    bowl_ratings = bowl_ratings.merge(bowl_innings)
    
    bat_ratings.to_csv("data/07_model_output/bat_ratings.csv")
    bowl_ratings.to_csv("data/07_model_output/bowl_ratings.csv")
    
    return bat_ratings, bowl_ratings