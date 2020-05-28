

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


# class Tracks(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     artist_name = db.Column(db.String(256))
#     track_name = db.Column(db.String(256))
#     album_name = db.Column(db.String(256))
#     track_id = db.Column(db.String(128))
#     artist_id = db.Column(db.String(128))
#     year = db.Column(db.Integer)
#     danceability = db.Column(db.Float)
#     energy = db.Column(db.Float)
#     key = db.Column(db.Integer)
#     loudness = db.Column(db.Float)
#     mode = db.Column(db.Float)
#     speechiness = db.Column(db.Float)
#     acousticness = db.Column(db.Float)
#     instrumentalness = db.Column(db.Float)
#     liveness = db.Column(db.Float)
#     valence = db.Column(db.Float)
#     tempo = db.Column(db.Float)
#     duration_ms = db.Column(db.Integer)
#     time_signature = db.Column(db.Integer)

class Songs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acousticness = db.Column(db.Float)
    artists = db.Column(db.String(512))
    danceability = db.Column(db.Float)
    duration_ms = db.Column(db.Integer)
    energy = db.Column(db.Float)
    explicit = db.Column(db.Float)
    track_id = db.Column(db.String(512))
    instrumentalness = db.Column(db.Float)
    key = db.Column(db.Integer)
    liveness = db.Column(db.Float)
    loudness = db.Column(db.Float)
    mode = db.Column(db.Integer)
    name = db.Column(db.String(512))
    popularity = db.Column(db.Integer)
    release_date = db.Column(db.String(256))
    speechiness = db.Column(db.Float)
    tempo = db.Column(db.Float)
    valence = db.Column(db.Float)
    year = db.Column(db.Integer)



