from src.wallet.wallet_service import *
from src.wallet.wallet_models import Entitlement

def test_create_user_entitlements(mocker, event_loop):
    ticket = {}
    mocked_entitlement = mocker.patch.object(Entitlement, 'save', autospec=True)
    event_loop.run_until_complete(create_user_entitlements(ticket))
    mocked_entitlement.assert_called()


def test_get_entitlements_by_user(mocker, event_loop):
    proxy = mocker.patch('src.wallet.wallet_models.Entitlement.objects')
    
    user_id = 5
    event_loop.run_until_complete(get_entitlements_by_user(user_id=user_id))
    proxy.assert_called_with(user_id=user_id)