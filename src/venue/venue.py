from flask import Blueprint, Response, jsonify, request

from .venue_service import *

venue = Blueprint("venue", __name__, url_prefix="/venue")


@venue.route("", methods=["POST"])
def add_venue():
    """
    Create a new venue representation for the API.
    Creation happens by the venue owners or a sales team.
    """
    body = request.get_json()
    venue = create_venue(name=body["name"], sections=body["sections"])
    return jsonify(venue), 201


@venue.route("/<id>", methods=["GET"])
def get_venue_by_id(id):
    """
    Return a venue by ID.

    :return: Venue
    """
    venue = get_venue(id=id)
    return jsonify(venue), 200
