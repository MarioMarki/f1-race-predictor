import pandas as pd

df = pd.read_csv("data/results.csv")
def predict_podium(df, season, race_round):
    present = df.loc[(df['season'] == season) & (df['round'] == race_round) & (df['session'] == 'race'), 'driverId'].unique().tolist()
    if race_round == 1:
        history = df[(df['season'] == season-1)]
    else:
        history = df[(df['season'] == season) & (df['round'] < race_round)]
    total_points = (
            history[history['driverId'].isin(present)]
            .groupby('driverId')['points']
            .sum()
            .sort_values(ascending=False)
            .head(3)
        )

    return total_points.index.tolist()
def actual_podium(df, season, race_round,session = 'race'):
    podium = df[(df['season'] == season) & (df['round'] == race_round) & (df['session'] == session) & (df['position'] <= 3)]
    return podium['driverId'].tolist()
def score(predicted, actual):
    matches=0
    for driver in predicted:
        if driver in actual:
            matches+=1
    return matches
scores = []
for season in df["season"].unique():
    for race_round in df.loc[(df['season'] == season) & (df['session'] == 'race'), 'round'].unique():
        if season == 2014 and race_round == 1:
            continue
        scores.append(score(predict_podium(df, season, race_round), actual_podium(df, season, race_round)))
print(len(scores))
print(sum(scores) / len(scores))
print('done')