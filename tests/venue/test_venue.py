from src.venue.venue_service import *
from src.venue.venue_models import Venue

def test_create_venue(mocker, event_loop):
    test_venue_name = 'test_name'
    test_venue_sections = [{
        'name': 'main hall'
    }]
    mocked_venue = mocker.patch.object(Venue, 'save', autospec=True)
    res = event_loop.run_until_complete(create_venue(test_venue_name, test_venue_sections))
    mocked_venue.assert_called()
    assert res['main hall'] is not None


def test_get_venue(mocker, event_loop):
    test_id = 'id'
    
    proxy = mocker.patch('src.venue.venue_models.Venue.objects')
    event_loop.run_until_complete(get_venue(id=test_id))
    proxy.assert_called_with(id=test_id)


def test_get_all_venues(mocker, event_loop):
    proxy = mocker.patch('src.venue.venue_models.Venue.objects')
    event_loop.run_until_complete(get_all_venues())
    proxy.assert_called_with()