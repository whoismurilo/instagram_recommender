import pandas as pd
import numpy as np
import random
import time

pd.set_option('display.max_columns', None)
start_time = time.time()


def create_dataset(values):
    df = pd.DataFrame(columns=['id', 'gender', 'country_code', 'publication_date', 'reach',
                               'impressions', 'imp_from_followers', 'imp_from_hashtags',
                               'imp_from_explore', 'imp_from_others', 'saves', 'comments',
                               'likes', 'repost_forward', 'profile_visit', 'previous_followers',
                               'gained_followers', 'lost_followers', 'total_followers', 'conversion_rate',
                               'engagement', 'engagement_rate', 'tags'])

    # gender and id
    df['gender'] = random.choices(['Male', 'Female', 'Other'], weights=[3, 3, 1], k=values)
    df['id'] = range(1, len(df['id']) + 1)
    df.set_index('id', inplace=True)

    # country code
    df['country_code'] = random.choices(['US', 'IN', 'BR', 'ID', 'RU'], weights=[5, 4, 4, 3, 2], k=values)

    # tags
    df['tags'] = random.choices(['F1', 'Volleyball', 'Data Science', 'Space', 'Statistic', 'AI'],
                                weights=[5, 3, 4, 3, 3, 4], k=values)

    # publication date
    df['publication_date'] = random.choices(pd.date_range('2022-07-01', periods=7), weights=[3, 9, 10, 1, 5, 2, 6],
                                            k=values)

    # list of cols and weight
    cols_reach = ['imp_from_followers', 'imp_from_hashtags', 'imp_from_explore', 'imp_from_others']
    cols_impressions = ['saves', 'comments', 'likes', 'repost_forward', 'profile_visit']
    cols_followers = ['previous_followers', 'gained_followers']
    weights_reach = [[1.47, 1.44, 1.38, 1.34], [0.56, 0.53, 0.49, 0.46], [0.38, 0.35, 0.31, 0.27],
                     [0.14, 0.12, 0.10, 0.08]]
    weights_impressions = [[0.07, 0.06, 0.04, 0.03], [0.19, 0.17, 0.13, 0.11], [0.28, 0.21, 0.16, 0.12],
                           [0.06, 0.04, 0.02, 0.01], [0.11, 0.09, 0.07, 0.6]]
    weights_followers = [[0.64, 0.60, 0.56, 0.50], [0.007, 0.006, 0.005, 0.003]]

    # create reach
    df['reach'] = np.random.randint(low=100, high=500000, size=values)

    # create impressions
    for i, j in zip(cols_reach, weights_reach):
        df.loc[df['reach'] <= 1000, i] = round(df['reach'] * j[0])
        df.loc[((df['reach'] > 1000) & (df['reach'] <= 50000)), i] = round(df['reach'] * j[1])
        df.loc[((df['reach'] > 50000) & (df['reach'] < 250000)), i] = round(df['reach'] * j[2])
        df.loc[df['reach'] >= 250000, i] = round(df['reach'] * j[3])

    df['impressions'] = (df.iloc[:, 5:9].sum(axis=1)).astype('int64')

    # create actions
    for i, j in zip(cols_impressions, weights_impressions):
        df.loc[df['impressions'] <= 1000, i] = round(df['reach'] * j[0])
        df.loc[((df['impressions'] > 1000) & (df['impressions'] <= 50000)), i] = round(df['reach'] * j[1])
        df.loc[((df['impressions'] > 50000) & (df['impressions'] < 250000)), i] = round(df['reach'] * j[2])
        df.loc[df['impressions'] >= 250000, i] = round(df['reach'] * j[3])

    # create followers
    for i, j in zip(cols_followers, weights_followers):
        if i == "previous_followers":
            df.loc[df['imp_from_followers'] <= 1000, i] = df['imp_from_followers'] * j[0]
            df.loc[((df['imp_from_followers'] > 1000) & (df['imp_from_followers'] <= 50000)), i] = df['imp_from_followers'] * j[1]
            df.loc[((df['imp_from_followers'] > 50000) & (df['imp_from_followers'] < 250000)), i] = df['imp_from_followers'] * j[2]
            df.loc[df['imp_from_followers'] >= 250000, i] = df['imp_from_followers'] * j[3]
        else:
            df.loc[df['imp_from_followers'] <= 1000, i] = (df['imp_from_hashtags'] + df['imp_from_explore'] + df['imp_from_others']) * j[0]
            df.loc[((df['imp_from_followers'] > 1000) & (df['imp_from_followers'] <= 50000)), i] = (df['imp_from_hashtags'] + df['imp_from_explore'] + df['imp_from_others']) * j[1]
            df.loc[((df['imp_from_followers'] > 50000) & (df['imp_from_followers'] < 250000)), i] = (df['imp_from_hashtags'] + df['imp_from_explore'] + df['imp_from_others']) * j[2]
            df.loc[df['imp_from_followers'] >= 250000, i] = (df['imp_from_hashtags'] + df['imp_from_explore'] + df['imp_from_others']) * j[3]

    df.loc[df['imp_from_followers'] <= 1000, 'lost_followers'] = df['imp_from_followers'] * 0.00085
    df.loc[((df['imp_from_followers'] > 1000) & (df['imp_from_followers'] <= 50000)), 'lost_followers'] = df['imp_from_followers'] * 0.0008
    df.loc[((df['imp_from_followers'] > 50000) & (df['imp_from_followers'] < 100000)), 'lost_followers'] = df['imp_from_followers'] * 0.00075
    df.loc[((df['imp_from_followers'] >= 100000) & (df['imp_from_followers'] < 200000)), 'lost_followers'] = df['imp_from_followers'] * 0.00065
    df.loc[((df['imp_from_followers'] >= 200000) & (df['imp_from_followers'] < 300000)), 'lost_followers'] = df['imp_from_followers'] * 0.00055
    df.loc[((df['imp_from_followers'] >= 300000) & (df['imp_from_followers'] < 400000)), 'lost_followers'] = df['imp_from_followers'] * 0.00045
    df.loc[((df['imp_from_followers'] >= 400000) & (df['imp_from_followers'] < 500000)), 'lost_followers'] = df['imp_from_followers'] * 0.00040
    df.loc[((df['imp_from_followers'] >= 500000) & (df['imp_from_followers'] < 600000)), 'lost_followers'] = df['imp_from_followers'] * 0.00035
    df.loc[((df['imp_from_followers'] >= 600000) & (df['imp_from_followers'] < 700000)), 'lost_followers'] = df['imp_from_followers'] * 0.00030
    df.loc[((df['imp_from_followers'] >= 700000) & (df['imp_from_followers'] < 800000)), 'lost_followers'] = df['imp_from_followers'] * 0.00025
    df.loc[((df['imp_from_followers'] >= 800000) & (df['imp_from_followers'] < 900000)), 'lost_followers'] = df['imp_from_followers'] * 0.0002
    df.loc[df['imp_from_followers'] >= 900000, 'lost_followers'] = df['imp_from_followers'] * 0.00015

    df['total_followers'] = (df['gained_followers'] - df['lost_followers']) + df['previous_followers']
    df['conversion_rate'] = (df['gained_followers'] - df['lost_followers']) / df['profile_visit'] * 100
    df['engagement'] = (df.iloc[:, 9:14].sum(axis=1)).astype('int64')
    df['engagement_rate'] = (df['engagement'] / df['previous_followers']) * 100

    columns = ['reach', 'impressions', 'imp_from_followers', 'imp_from_hashtags', 'imp_from_explore',
               'imp_from_others', 'saves', 'comments', 'likes', 'repost_forward', 'profile_visit',
               'previous_followers', 'gained_followers', 'lost_followers', 'total_followers',
               'engagement', 'engagement_rate']

    for i in columns:
        df[i] = df[i].astype('int64')
        df[i] = df[i].round()
    return df


create_dataset(1000000)
