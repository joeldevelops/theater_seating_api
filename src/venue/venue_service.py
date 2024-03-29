from .venue_models import *


async def create_venue(name, sections):
    """
    Take in venue name and create named sections in the document
    """
    venue = Venue()
    venue.name = name
    for section in sections:
        venue[section["name"]] = section

    venue.save()
    return venue


async def get_venue(id):
    """
    Return a venue by ID.

    :return: Venue
    """
    venue = Venue.objects(id=id).first_or_404()
    return venue


async def get_all_venues():
    """
    Return all venues.

    :return: Venues
    """
    venue = Venue.objects()
    return venue
