from flask import Blueprint, Response, jsonify, request

seats = Blueprint("seating", __name__, url_prefix="/seats")

from .seats_service import *


@seats.route("", methods=["GET"])
def get_seats():
    """
    Get seats for a venue by passing in a venue_id

    :venue_id: passed in as a query param to the method
    :return: Array of Seat documents
    """
    query_params = request.args
    if not query_params.get("venue_id"):
        return Response(
            "venue_id is a required query param for this method", status=400
        )

    seats = get_seats(query_params)
    return jsonify(seats), 200


@seats.route("/<id>", methods=["GET"])
def get_seat_by_id(id):
    """
    Get seat by ID
    """
    seat = get_seat(id)
    return jsonify(seat), 200


@seats.route("", methods=["POST"])
def add_seats_by_rank():
    """
    Accept array of seats to batch write. Part of venue initialization.

    :rank: Body field indicating which rank these seats belong to.
    :seats: Array of seats with their details to add.
    """
    body = request.get_json()
    if not body["rank"]:
        return Response("Rank is a required field", status=400)

    create_seats(body)
    return Response("ok", status=201)


@seats.route("/order/", methods=["POST"])
def seating_order():
    """
    Load seats from DB and seat specified groups in the best possible way.

    :venue_id: The ID of the venue to do the seating for.
    :rank: The rank in the venue to seat.
    :groups: The specified array of groups to seat. Array of numbers with each int representing group size.
    :return: 2D array of sat groups.
    """
    body = request.get_json()
    if not body["venue_id"] or not body["rank"]:
        return Response("venue_id and rank are required fields", status=400)

    if not body["groups"]:
        return Response("Array of groups to sit must be supplied", status=400)

    rank_layout = seat_rank_to_layout(venue_id=body["venue_id"], rank=body["rank"])
    seating = seat_groups(groups=body["groups"], rank=rank_layout)

    return jsonify(seating), 200


@seats.route("/order_simple/", methods=["GET"])
def seating_order_simple():
    """
    Simple method that takes in groups and rank array to seat without db interaction.
    Allows testing of algorithm.
    """
    query_args = request.args
    print(query_args)

    groups = [1, 3, 4, 4, 5, 1, 2, 4]
    rank = [
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    seating = seat_groups(groups=groups, rank=rank)

    return jsonify(seating), 200