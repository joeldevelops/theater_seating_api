from bson.objectid import ObjectId

from .seats_models import Seat
from .seating_class import Seating


async def create_seats(seats_info):
    """
    Create a seat in the DB
    """
    rank = seats_info["rank"]
    seats = seats_info["seats"]
    for seat in seats:
        seat["rank"] = rank
    seat_instances = [Seat(**seat) for seat in seats]

    Seat.objects.insert(seat_instances, load_bulk=False)


async def get_seats(venue_id):
    """
    Generic method to load seats with a filter

    :filter: filter down the returned seats by venue_id, rank, and/or row.
    :return: seats document
    """
    venue_seats = Seat.objects(venue_id=ObjectId(venue_id))
    return venue_seats


async def seat_rank_to_layout(venue_id, rank):
    """
    Loads seat documents from the DB and convert them to a rank layout

    :venue_id: ID of the venue to get seats from
    :rank: The rank within the venue to seat
    :return: 2D array of the layout as seat documents
    """
    seats = Seat.objects(venue_id=ObjectId(venue_id), rank=rank).order_by("+row", "+seat_number")
    row = 0
    layout = [[]]
    for i in range(len(seats)):
        if i > 0 and seats[i].row != seats[i - 1].row:
            row += 1
            layout.append([])

        seat = seats[i].to_mongo()
        seat_obj = seat.to_dict()
        del seat_obj["_id"]
        del seat_obj["venue_id"]
        layout[row].append(seat_obj)

    return layout


async def seat_groups(groups, rank):
    """
    Take in an array of groups and a rank layout to sit them in.

    :groups: an array of groups to seat in the order to seat them.
    :rank: represents the seats for a given rank as a 2d array.
    """
    seating = Seating(groups, rank)
    for i in range(len(rank)):
        row_placement = await seating.seat_row()
        updated_placement = await seating.group_preference(i, row_placement)
        for group in updated_placement:
            await seating.seat_group(group["size"], group["position"])

    seating.print_layout()

    return rank
