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


async def get_seat(id):
    """
    Get seat by ObjectID
    """
    seat = Seat.objects(id=id).first()
    return seat


async def get_seats(filter):
    """
    Generic mehtod to load seats with a filter

    :filter: filter down the returned seats by venue_id, rank, and/or row.
    """
    seats = Seat.objects(**filter)
    return seats


async def seat_rank_to_layout(venue_id, rank):
    """
    Loads seat documents from the DB and convert them to a rank layout

    :return: 2D array of the layout
    """
    seats = Seat.objects(venue_id=venue_id, rank=rank).order_by("+row", "+seat_number")
    row = 0
    layout = [[]]
    for seat, i in seats:
        if i > 0 and seat.row != seats[i - 1]:
            row += 1
            layout.append([])

        layout[row].append(seat)

    return layout


async def seat_groups(groups, rank):
    """
    Take in an array of groups and a rank layout to sit them in.

    :groups: an array of groups to seat in the order to seat them.
    :rank: represents the seats for a given rank as a 2d array.
    """
    seating = Seating(groups, rank)
    for i in range(len(rank)):
        await seating.seat_row()

    print(seating.rank_seating_layout())

    return rank
