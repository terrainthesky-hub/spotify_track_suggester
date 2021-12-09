from flask import Blueprint, jsonify, render_template, request, redirect
import os

import psycopg2

from dotenv import load_dotenv 

songs_routes = Blueprint("songs_routes", __name__)

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

@songs_routes.route("/fetch/<artist>/<song_name>")
def song_recommender(artist=None, song_name=None):
    # query = f"""
    # SELECT track_id from Songs where Songs.name = {song_name}
    # """

    query = f"SELECT track_id from Songs where Songs.name = '{song_name}'"
    conpg = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                                host=DB_HOST)
    curpg = conpg.cursor()
    curpg.execute(query)
    track_id = curpg.fetchall()
    track_id[0][0]


    return track_id[0][0]
