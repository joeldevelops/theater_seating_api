from quart import Blueprint, Response, jsonify, request

seats = Blueprint("seating", __name__)

from .seats_service import *


@seats.route("/seats/venue/<venue_id>", methods=["GET"], strict_slashes=False)
async def seats_by_query(venue_id):
    """
    Get seats for a venue by passing in a venue_id

    :venue_id: passed in as a query param to the method
    :return: Array of Seat documents
    """
    if not venue_id:
        return Response(
            "venue_id is a required query param for this method", status=400
        )

    venue_seats = await get_seats(venue_id)
    return jsonify(venue_seats), 200


@seats.route("/seats", methods=["POST"], strict_slashes=False)
async def add_seats_by_rank():
    """
    Accept array of seats to batch write. Part of venue initialization.

    :rank: Body field indicating which rank these seats belong to.
    :seats: Array of seats with their details to add.
    """
    body = await request.get_json()
    if not body["rank"]:
        return Response("Rank is a required field", status=400)

    await create_seats(body)
    return Response("ok", status=201)


@seats.route("/seats/order", methods=["POST"], strict_slashes=False)
async def seating_order():
    """
    Load seats from DB and seat specified groups in the best possible way.

    :venue_id: The ID of the venue to do the seating for.
    :rank: The rank in the venue to seat.
    :groups: The specified array of groups to seat. Array of numbers with each int representing group size.
    :prefs: An object containing keys that map to a groups preferences.
    :return: 2D array of sat groups.
    """
    body = await request.get_json()
    prefs = {}
    if not body["venue_id"] or not body["rank"]:
        return Response("venue_id and rank are required fields", status=400)

    if not body["groups"]:
        return Response("Array of groups to sit must be supplied", status=400)

    if "prefs" in body:
        prefs = body["prefs"]

    rank_layout = await seat_rank_to_layout(body["venue_id"], body["rank"])
    seating = await seat_groups(body["groups"], rank_layout, prefs)

    return jsonify(seating), 200
