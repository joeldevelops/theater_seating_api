from quart import Blueprint, Response, jsonify, request

from .venue_service import *

venue = Blueprint("venue", __name__)


@venue.route("/venue", methods=["POST"])
async def add_venue():
    """
    Create a new venue representation for the API.
    Creation happens by the venue owners or a sales team.
    """
    body = await request.get_json()
    venue = await create_venue(name=body["name"], sections=body["sections"])
    return jsonify(venue), 201


@venue.route("/venue/<id>", methods=["GET"])
async def get_venue_by_id(id):
    """
    Return a venue by ID.

    :return: Venue
    """
    venue = await get_venue(id=id)
    return jsonify(venue), 200
