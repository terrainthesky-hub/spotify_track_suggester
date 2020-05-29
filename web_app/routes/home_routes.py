from flask import Blueprint, jsonify, render_template, request, redirect
import os



home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def home_page():
    return "go to /fetch/artist/trackname to query the model!"