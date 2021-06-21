import pydantic

from typing import Any, Callable


def _build_decorator(validator: Callable, *fields: str) -> classmethod:
    decorator = pydantic.validator(*fields, allow_reuse=True, check_fields=False)
    return decorator(validator)


def prevent_none(*fields: str) -> classmethod:
    """
    Pydantic validator for optional fields that, if given in the request, can not be None. Using a validator is
    currently the only way to accomplish this behavior.
    """

    def _validate(value: Any) -> str:
        assert value is not None, "Field can not be None"
        return value

    return _build_decorator(_validate, *fields)
