from quart import Blueprint, Response

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
async def server_error(error):
    """
    General API error handler.
    """
    print(error)
    return Response(f"Oops, got an error! {error}", status=500)
