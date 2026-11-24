"""Ownership checks: a user can only access apiaries (and their hives) that belong to them.

All helpers rely on `token_required` having run first, which stores the
authenticated user id in `flask.g.current_user_id`.
"""
from uuid import UUID
from flask import current_app, g

from src.features.apiaries.domain.exceptions.apiary_exceptions import ApiaryNotFoundError
from src.features.beehive.domain.exceptions.beehive_exceptions import BeehiveNotFoundException

FORBIDDEN_MESSAGE = "No tienes permiso para acceder a este recurso"


class ForbiddenError(Exception):
    """The authenticated user does not own the requested resource."""

    def __init__(self, message: str = FORBIDDEN_MESSAGE):
        super().__init__(message)


def get_authenticated_user_id() -> str:
    user_id = getattr(g, 'current_user_id', None)
    if not user_id:
        raise ForbiddenError()
    return str(user_id)


def _same_id(a, b) -> bool:
    return str(a).lower() == str(b).lower()


def ensure_same_user(user_id) -> None:
    """The given user id must be the authenticated user."""
    if not _same_id(user_id, get_authenticated_user_id()):
        raise ForbiddenError()


def ensure_apiary_owner(apiary_id):
    """Returns the apiary DTO if it belongs to the authenticated user.

    Raises ApiaryNotFoundError (404) or ForbiddenError (403).
    """
    apiary = current_app.container.get_apiary_by_id_use_case().execute(apiary_id)
    ensure_same_user(apiary.user_id)
    return apiary


def ensure_hive_owner(hive_id):
    """Returns the beehive DTO if its apiary belongs to the authenticated user.

    Raises BeehiveNotFoundException (404) or ForbiddenError (403).
    """
    hive = current_app.container.get_beehive_by_id_use_case().execute(hive_id)
    try:
        ensure_apiary_owner(hive.apiary_id)
    except ApiaryNotFoundError:
        raise BeehiveNotFoundException(hive_id)
    return hive
