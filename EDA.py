import os
import numpy as np
import pandas as pd
import psycopg2
from dotenv import load_dotenv


# credentials
load_dotenv('.env')
username = os.getenv('username')
password = os.getenv('password')
host = os.getenv('host')
db = os.getenv('db')
port = os.getenv('port')
engine = os.getenv('engine')

# open db
connection = psycopg2.connect(user=username, password=password, host=host, database=db, port=port)
cursor = connection.cursor()

# extract data from database
cursor.execute("""SELECT * FROM instagram;""")
extract = cursor.fetchall()

# create dataframe
data = pd.DataFrame(np.array(extract).reshape(len(extract), 23))
data.columns = ['id', 'gender', 'coutry_code', 'publication_date', 'reach', 'impressions',
                'imp_from_followers', 'imp_from_hashtags', 'imp_from_explore', 'imp_from_others',
                'saves', 'comments', 'likes', 'repost_forward', 'profile_visit', 'previous_followers',
                'gained_followers', 'lost_followers', 'total_followers', 'conversion_rate', 'engagement',
                'engagement_rate', 'tags']

data.set_index('id', inplace=True)
