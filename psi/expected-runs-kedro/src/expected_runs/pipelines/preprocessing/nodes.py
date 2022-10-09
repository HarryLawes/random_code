"""
This is a boilerplate pipeline 'preprocessing'
generated using Kedro 0.18.2
"""

import pandas as pd
import math

def exclude_non_t20s(df):
    
    df['t20'] = df['over_limit'].apply(lambda x: True if x in [0, 20] else False)
    df['date'] = pd.to_datetime(df['date'], utc = True)

    t20_matches = df.groupby('event_id', as_index=False)[['t20']].min()
    t20_matches = t20_matches[t20_matches['t20'] == True]

    t20_matches_list = list(t20_matches['event_id'])
    t20_matches_list.remove(1204677)
    df = df[df['event_id'].isin(t20_matches_list)]
    
    return df

def exclude_certain_matches(df):
    
    df['date'] = pd.to_datetime(df['date'], utc = True)
    
    matches = df.groupby('event_id').head(1)[['event_id', 'date', 'batsman_striker_team_name', 'bowler_team_name']]
    
    # Excluding matches with missing info
    matches = matches[matches['batsman_striker_team_name'].notnull()]
    # Excluding U19 matches - development formats not the most relevant
    matches = matches[~matches['batsman_striker_team_name'].str.contains('Under-19s')]

    # Excluding BBL matches with Power Surge + Bash Boost
    bbl_teams = ['Sydney Thunder', 'Sydney Sixers', 'Melbourne Renegades', 'Melbourne Stars',
                'Hobart Hurricanes', 'Brisbane Heat', 'Perth Scorchers', 'Adelaide Strikers']
    
    matches = matches[~((matches['batsman_striker_team_name'].isin(bbl_teams)) &
            (matches['date'] > pd.to_datetime('2020-6-01', utc=True)))]

    # Excluding matches before the start of the IPL
    matches = matches[matches['date'] >= pd.to_datetime('2008-4-18', utc=True)]

    match_id_list = list(matches['event_id'])
    
    df = df[df['event_id'].isin(match_id_list)]
    
    return df

def exclude_anomalies(df):
    
    df = df.merge(
        df.groupby(
            ['event_id', 'innings'], as_index = False
        )[['batsman_striker_team_id']].nunique().sort_values(
        'batsman_striker_team_id'
        ).rename(
            columns={'batsman_striker_team_id':'batting_teams'}
        )
    )
    
    df = df[df['batting_teams'] == 1]
    df = df[df['overs'] <= 20]
    df = df[df['innings_wickets'] != 10]
    
    df = df[(df['innings_runs'] < df['innings_target']) | (df['innings'] == 1)]
    df = df[~((df['innings'] == 2) & (df['innings_target'] == 0))]
    
    return df

def add_extra_ball(df):
    
    if df['innings_remaining_balls'] == 0 and df['innings'] == 2:
        df['innings_remaining_balls'] = 1
        df['run_rate_required'] = df['innings_remaining_runs']
        
    return df

def prepare_features(df):
    
    df['powerplay'] = df['overs'].apply(lambda x: 1 if x < 6 else 0)
    df['middle'] = df['overs'].apply(lambda x: 1 if x >= 6 and x < 14 else 0)
    df['death'] = df['overs'].apply(lambda x: 1 if x >= 14 else 0)
    df['over_number'] = df['overs'].apply(lambda x: math.floor(x))
    df['wicket'] = df['outcome'].apply(lambda x: 1 if x == 'out' else 0)
    
    df['innings_wickets'] = df.sort_values(
        ['event_id', 'innings', 'overs', 'ball_no']
    ).groupby(['event_id', 'innings'])['innings_wickets'].shift(1).fillna(0)
    
    df = df.apply(add_extra_ball, axis=1)
    
    df['year'] = pd.DatetimeIndex(df['date']).year
    
    return df

def train_test_split(df):
    
    train = df[df['year'] < 2020]
    test = df[df['year'] >= 2020]
    
    train.to_csv("data/05_model_input/train_data.csv")
    test.to_csv("data/05_model_input/test_data.csv")
    
    return train, test