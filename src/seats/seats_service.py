from .seats_models import Seat


def create_seats(seats_info):
    """
    Create a seat in the DB
    """
    rank = seats_info["rank"]
    seats = seats_info["seats"]
    for seat in seats:
        seat["rank"] = rank
    seat_instances = [Seat(**seat) for seat in seats]

    Seat.objects.insert(seat_instances, load_bulk=False)


def get_seat(id):
    """
    Get seat by ObjectID
    """
    seat = Seat.objects(id=id).first()
    return seat


def get_seats(filter):
    """
    Generic mehtod to load seats with a filter

    :filter: filter down the returned seats by venue_id, rank, and/or row.
    """
    seats = Seat.objects(**filter)
    return seats


def seat_rank_to_layout(venue_id, rank):
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


def seat_groups(groups, rank):
    """
    Take in an array of groups and a rank layout to sit them in.

    :groups: an array of groups to seat in the order to seat them.
    :rank: represents the seats for a given rank as a 2d array.
    """
    row = 0
    column = 0
    group_count = 0
    rtl = row % 2 == 0  # Right to left on even rows
    for group in groups:
        group_count += 1
        for i in range(group):
            rank[row][column] = group_count

            if rtl:
                column += 1
            else:
                column -= 1

            end_of_row = column > len(rank[row]) - 1 or column < 0
            if end_of_row:
                row += 1
                rtl = row % 2 == 0

                # columns could be various sizes within the same rank.
                # reset when going left to right to ensure proper size.
                if column != 0 and row < len(rank) - 1:
                    column = len(rank[row]) - 1
                elif column < 0:
                    column = 0

    return rank
