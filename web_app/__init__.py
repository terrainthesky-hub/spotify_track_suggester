# web_app/__init__.py

from dotenv import load_dotenv
from flask import Flask
import os
from web_app.models import db, migrate
from web_app.routes.songs_routes import songs_routes
from web_app.routes.home_routes import home_routes


load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URL")


def create_app():
    app = Flask(__name__)
    
    # configure the database:
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # suppress warning messages
    db.init_app(app)
    migrate.init_app(app, db)

    # configure routes:
 #   app.register_blueprint(database_routes)
    app.register_blueprint(songs_routes)
    app.register_blueprint(home_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
