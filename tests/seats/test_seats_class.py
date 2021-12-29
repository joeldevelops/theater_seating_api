from src.seats.seating_class import Seating

# No test cases included for number of groups > number of seats as <= sizes can be assumed

def test_rtl():
    seating = Seating([], [[]], {})

    for num in [0, 2, 4, 6, 8]:
        seating.row = num
        assert seating.ltr() == True
    
    for num in [1, 3, 5, 7, 9]:
        seating.row = num
        assert seating.ltr() == False


def test_remaining_seats_in_row_ltr():
    # 6 elements in row
    seating = Seating([], [[0, 0, 0, 0, 0, 0]], {})
    seating.column = 3
    assert seating.remaining_seats_in_row() == 3


def test_remaining_seats_in_row_rtl():
    seating = Seating([], [[], [0, 0, 0, 0, 0, 0]], {})
    seating.column = 3
    seating.row = 1
    assert seating.remaining_seats_in_row() == 4


def test_seat_row(event_loop):
    test_groups = [1, 2, 3]
    test_rank_layout = [[0, 0, 0, 0, 0, 0]]
    test_prefs = {}
    seating = Seating(test_groups, test_rank_layout, test_prefs)
    res = event_loop.run_until_complete(seating.seat_row())
    assert len(res) == 3 # Method returns list of dicts representing seated groups
    assert res[2]['position'] == 3 # Seated in order


def test_seat_row_with_empty_leftovers(event_loop):
    test_groups = [1, 2, 1] # Activates second for loop as there are no equal size groups
    test_rank_layout = [[0, 0, 0, 0, 0, 0]]
    test_prefs = {}
    seating = Seating(test_groups, test_rank_layout, test_prefs)
    res = event_loop.run_until_complete(seating.seat_row())
    assert res[2]['size'] == 1


def test_seat_row_with_overflow(event_loop):
    test_groups = [1, 2, 6] # Activates third section to wrap group
    test_rank_layout = [[0, 0, 0, 0, 0, 0], [0, 0, 0]]
    test_prefs = {}
    seating = Seating(test_groups, test_rank_layout, test_prefs)
    res = event_loop.run_until_complete(seating.seat_row())
    assert res[2]['size'] == 6


def test_seat_group(event_loop):
    test_groups = [1, 2, 3]
    test_rank_layout = [[{}, {}, {}], [{}, {}, {}]]
    test_prefs = {}
    seating = Seating(test_groups, test_rank_layout, test_prefs)
    event_loop.run_until_complete(seating.seat_group(2, 2))
    assert seating.row == 0
    assert seating.column == 2


def test_row_modifiers(event_loop):
    test_groups = [1, 3, 2]
    test_rank_layout = [[{
            "modifiers": ["aisle"]
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": ["balcony", "aisle"]
        }]]
    test_prefs = {}
    test_placement = [{
        "size": 1
    }, {
        "size": 3
    }, {
        "size": 2
    }]
    seating = Seating(test_groups, test_rank_layout, test_prefs)
    res = event_loop.run_until_complete(seating.row_modifiers(0, test_placement))
    assert res == [
      ["aisle"],
      [],
      ["balcony", "aisle"]
    ]


def test_group_preference(event_loop):
    test_groups = [1, 3, 2]
    test_rank_layout = [[{
            "modifiers": ["aisle"]
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": ["balcony"]
        }, {
            "modifiers": []
        }, {
            "modifiers": ["aisle"]
        }]]
    test_prefs = {}
    test_placement = [{
        "size": 1,
        "preference": "balcony"
    }, {
        "size": 3,
        "preference": "aisle"
    }, {
        "size": 2,
        "preference": "aisle"
    }]

    seating = Seating(test_groups, test_rank_layout, test_prefs)
    res = event_loop.run_until_complete(seating.group_preference(0, test_placement))
    assert res[0]["size"] == 3 # Shuffled
    assert res[1]["size"] == 1
    assert res[2]["size"] == 2 # Position maintained


def test_group_preference_with_duplicate_shuffles(event_loop):
    test_groups = [1, 3, 2]
    test_rank_layout = [[{
            "modifiers": ["aisle"]
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": []
        }, {
            "modifiers": ["balcony", "aisle"]
        }]]
    test_prefs = {}
    test_placement = [{
        "size": 1,
        "preference": "balcony"
    }, {
        "size": 3,
        "preference": None
    }, {
        "size": 2,
        "preference": "aisle"
    }]

    seating = Seating(test_groups, test_rank_layout, test_prefs)
    res = event_loop.run_until_complete(seating.group_preference(0, test_placement))
    assert res[0]["size"] == 2 # Shuffled
    assert res[1]["size"] == 3
    assert res[2]["size"] == 1 # Shuffled

