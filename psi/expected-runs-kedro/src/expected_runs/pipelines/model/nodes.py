"""
This is a boilerplate pipeline 'model'
generated using Kedro 0.18.2
"""
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import pickle

def train_first_innings(df):
    
    first_inns = df[df['innings'] == 1]
    
    X1 = first_inns[['innings_wickets', 'batter_balls_faced', 'powerplay', 'over_number']]
    y1 = first_inns['score_value']

    model = LinearRegression()
    model.fit(X1, y1)
    
    return model

def train_second_innings(df):
    
    second_inns = df[df['innings'] == 2]
    
    X2 = second_inns[['innings_wickets', 'batter_balls_faced', 'powerplay', 'over_number', 'run_rate_required']]
    y2 = second_inns['score_value']

    model = LinearRegression()
    model.fit(X2, y2)
    
    return model

def train_models(df):
    
    first_model = train_first_innings(df)
    second_model = train_second_innings(df)
    
    pickle.dump(first_model, open('data/06_models/first_model.pkl', 'wb'))
    pickle.dump(second_model, open('data/06_models/second_model.pkl', 'wb'))
    
    return first_model, second_model

def calculate_remaining_balls(df):
    
    if df['innings'] == 1:
        if df['innings_remaining_balls'] == 0:
            df['innings_remaining_balls'] = 121 - df['match_ball_no']
            
    return df

def prepare_wicket_train_data(df):
    
    df = df.apply(calculate_remaining_balls, axis=1)
    
    df = df.merge(
        df.groupby(
            ['event_id', 'innings'], as_index = False
            )['innings_runs'].max().rename(
                columns={'innings_runs':'innings_total'}
                ),
            on=['event_id', 'innings'],
            how='left'
            )

    df['runs_after'] = df['innings_total'] - df['innings_runs'] + df['score_value']
    
    last_balls = df.sort_values('match_ball_no').groupby(['event_id', 'innings']).tail(1)

    complete_innings = list(
        last_balls[
            (last_balls['innings_remaining_balls'] == 1) |
            ((last_balls['innings_wickets'] == 9) & (last_balls['outcome'] == 'out'))
        ]['event_id'])

    df = df[df['event_id'].isin(complete_innings)]
    
    return df

def train_wicket_model(df):
    
    X1 = df[['innings_wickets', 'innings_remaining_balls']]
    y1 = np.log(df['runs_after'] + 1)
    
    model = LinearRegression()
    model.fit(X1, y1)
    
    return model

def get_value_of_wicket(df):
    
    wicket_perc = df['wicket'].mean()
    
    df = df[df['innings'] == 1]
    
    df = prepare_wicket_train_data(df)
    
    model = train_wicket_model(df)
    
    wickets = pd.DataFrame(
        np.arange(0,11,1)
    ).rename(
        columns={0:'innings_wickets'}
    )

    wickets['join'] = 0

    balls_remaining = pd.DataFrame(
        np.arange(0,121,1)
    ).rename(
        columns={0:'innings_remaining_balls'}
    )

    balls_remaining['join'] = 0

    merged = wickets.merge(balls_remaining).drop(columns=['join'])
    
    merged['pred'] = np.exp(model.predict(merged)) - 1

    merged['next_wicket'] = merged.groupby('innings_remaining_balls')['innings_wickets'].shift(-1)
    merged['wicket_pred'] = merged.groupby('innings_remaining_balls')['pred'].shift(-1)

    merged['value_of_wicket'] = merged['wicket_pred'] - merged['pred']

    value_of_wicket = merged.groupby('innings_remaining_balls', as_index = False)[['value_of_wicket']].mean()
    
    value_of_wicket['value_of_survival'] = value_of_wicket['value_of_wicket'] * wicket_perc * -1
    
    return value_of_wicket