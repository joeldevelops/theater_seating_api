from flask import Blueprint, Response, jsonify, request

from .wallet_service import *

wallet = Blueprint("wallet", __name__, url_prefix="/wallet")


@wallet.route("/<user_id>", methods=["POST"])
def add_entitlement():
    """
    Generate ownership of a seat or group of seats.
    """
    body = request.get_json()
    entitlement = add_user_entitlements(body)
    return jsonify(entitlement), 201


@wallet.route("/<user_id>", methods=["GET"])
def get_wallet_by_user(user_id):
    """
    Get wallet and return as a list of entitlements.
    """
    entitlements = get_entitlements_by_user(user_id=user_id)
    return jsonify(entitlements), 200
