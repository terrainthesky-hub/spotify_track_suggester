# from flask import Blueprint, jsonify, request, flash, redirect

# from web_app.models import db, Migrate, Songs
# import pandas as pd
# database_routes = Blueprint("database_routes", __name__)



# df = pd.read_csv(r'C:\Users\lesle\Desktop\spotify\web_app\spotify_data2.csv')


# @database_routes.route('/refresh', methods=['GET', 'POST'])
# def refresh():
#     db.drop_all()
#     db.create_all()
#     for x in range(0, 100000):
#         df_records = Songs(acousticness = df['acousticness'][x],
#                         artists = df['artists'][x],
#                         danceability = df['danceability'][x],
#                         duration_ms = int(df['duration_ms'][x]),
#                         energy = df['energy'][x],
#                         explicit = int(df['explicit'][x]),
#                         track_id = df['id'][x],
#                         instrumentalness = df['instrumentalness'][x],
#                         key = int(df['key'][x]),
#                         liveness = df['liveness'][x],
#                         loudness = df['loudness'][x],
#                         mode = int(df['mode'][x]),
#                         name = df['name'][x],
#                         popularity = int(df['popularity'][x]),
#                         release_date = df['release_date'][x],
#                         speechiness = df['speechiness'][x],
#                         tempo = df['tempo'][x],
#                         valence = df['valence'][x],
#                         year = int(df['year'][x]))
#         db.session.add(df_records)
#         db.session.commit()
#     return 'Data refreshed!'