import pydantic
import pytz
import semver

from typing import Any, Callable


def _build_decorator(validator: Callable, *fields: str) -> classmethod:
    decorator = pydantic.validator(*fields, allow_reuse=True, check_fields=False)
    return decorator(validator)


def prevent_none(*fields: str) -> classmethod:
    """
    Pydantic validator for optional fields that, if given in the request, can not be None. Using a validator is
    currently the only way to accomplish this behavior. Pydantic v2 is slated to have a better way to address this.
    """

    def _validate(value: Any) -> str:
        assert value is not None, "Field can not be None"
        return value

    return _build_decorator(_validate, *fields)


def timezone(*fields: str) -> classmethod:
    """
    Pydantic validator to ensure that a given timezone string is valid.
    """

    def _validate(value: str) -> str:
        assert value in pytz.all_timezones, f"{value} is not a valid timezone"
        return value

    return _build_decorator(_validate, *fields)


def version(*fields: str) -> classmethod:
    """
    Pydantic validator to ensure that a given version string conforms to SemVer.
    """

    def _validate(value: str) -> str:
        assert semver.VersionInfo.isvalid(value) is True, f"{value} is not a valid SemVer version"
        return value

    return _build_decorator(_validate, *fields)
