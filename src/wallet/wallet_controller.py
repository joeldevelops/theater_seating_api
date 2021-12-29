from quart import Blueprint, Response, jsonify, request

from .wallet_service import *

wallet = Blueprint("wallet", __name__)


@wallet.route("/wallet/<int:user_id>", methods=["POST"], strict_slashes=False)
async def add_entitlement():
    """
    Generate ownership of a seat or group of seats.
    """
    body = await request.get_json()
    entitlement = await add_entitlement(body)
    return jsonify(entitlement), 201


@wallet.route("/wallet/<int:user_id>", methods=["GET"], strict_slashes=False)
async def wallet_by_user(user_id):
    """
    Get wallet and return as a list of entitlements.
    """
    entitlements = await get_entitlements_by_user(user_id)
    return jsonify(entitlements), 200
