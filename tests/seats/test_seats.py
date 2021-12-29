from bson import ObjectId

from src.seats.seats_service import *
from src.seats.seats_models import Seat
from src.seats.seating_class import Seating
from src.wallet.wallet_models import Entitlement

def test_create_seats(mocker, event_loop):
    test_seats = {
        'rank': '1',
        'seats': [{
            'seat_number': '1',
            'row': '1'
        }]
    }
    proxy = mocker.patch('src.seats.seats_models.Seat.objects')
    proxy.return_value.insert.return_value = None
    event_loop.run_until_complete(create_seats(test_seats))
    proxy.insert.assert_called()


def test_get_seats(mocker, event_loop):
    test_venue_id = '61c95f272ae66f3472c7f6e4'
    
    proxy = mocker.patch('src.seats.seats_models.Seat.objects')
    event_loop.run_until_complete(get_seats(venue_id=test_venue_id))
    proxy.assert_called_with(venue_id=ObjectId(test_venue_id))


def test_seat_rank_to_layout(mocker, event_loop):
    test_venue_id = '61c95f272ae66f3472c7f6e4'
    test_rank = '1'
    test_seats = []
    row = 1
    for i in range(0, 9):
        if i % 3 == 0:
            row += 1
        s = Seat(**{ 'row': str(row) })
        s['id'] = ObjectId()
        test_seats.append(s)
    
    proxy = mocker.patch('src.seats.seats_models.Seat.objects')
    proxy.return_value.order_by.return_value = test_seats
    res = event_loop.run_until_complete(seat_rank_to_layout(test_venue_id, test_rank))
    assert isinstance(res, list)
    assert len(res) is 3
    assert len(res[0]) is 3


def test_seat_groups(mocker, event_loop):
    test_rank = [[{
        "user_id": 1,
        "venue_id": ObjectId('61c95f272ae66f3472c7f6e4'),
        "rank": '1',
        "group": 1
    },{
        "user_id": 2,
        "venue_id": ObjectId('61c95f272ae66f3472c7f6e4'),
        "rank": '1',
        "group": 2
    },{
        "user_id": 3,
        "venue_id": ObjectId('61c95f272ae66f3472c7f6e4'),
        "rank": '1',
        "group": 3
    }]]

    mock_seat_row = mocker.patch.object(Seating, 'seat_row', autospec=True)
    mock_seat_row.return_value = test_rank
    mock_group_preferences = mocker.patch.object(Seating, 'group_preference', autospec=True)
    mock_group_preferences.return_value = [{
        'size': 4,
        'position': 1
    },{
        'size': 5,
        'position': 2
    },{
        'size': 6,
        'position': 3
    }]
    mock_seat_group = mocker.patch.object(Seating, 'seat_group', autospec=True)
    mock_user_entitlements_save = mocker.patch.object(Entitlement, 'save', autospec=True)

    event_loop.run_until_complete(seat_groups([], test_rank, {}))
    mock_seat_row.assert_called_once()
    mock_group_preferences.assert_called_once()
    mock_seat_group.assert_called()
    mock_user_entitlements_save.assert_called()

