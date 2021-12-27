from .wallet_models import Entitlement

async def create_user_entitlements(details):
    """
    Take in the details of a ticket/entitlement and save to DB.
    """
    entitlement = Entitlement(**details)

    entitlement.save()
    return entitlement


async def get_entitlements_by_user(user_id):
    """
    Returns list of entitlements by owning user

    :return: List of entitlement documents
    """
    entitlements = Entitlement.objects(user_id=user_id)
    return entitlements
