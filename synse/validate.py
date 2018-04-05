"""Synse Server utility and convenience methods.
"""

from synse import cache, errors
from synse.i18n import gettext


async def validate_device_type(device_type, rack, board, device):
    """Validate that the device associated with the given routing info
    (rack, board device) matches the given device type.

    Args:
        device_type (str): The type of the device, e.g. "led", "fan", etc.
        rack (str): The rack which the device belongs to.
        board (str): The board which the device belongs to.
        device (str): The ID of the device.

    Raises:
        SynseError: The device does not match the given type.
        SynseError: The specified device is not found.
    """
    _, device = await cache.get_device_meta(rack, board, device)
    if device.type != device_type.lower():
        raise errors.InvalidDeviceType(
            gettext('Device ({}) is not of type {}').format(device.type, device_type)
        )


def validate_query_params(raw_args, *valid_params):
    """Validate that the incoming request's query parameters are valid.

    Any unsupported query parameter will cause an error to be raised.
    Absence of a supported query parameter will not cause an error. If
    a supported query parameter is found, it is added to the response
    dictionary.

    Args:
        raw_args: An incoming Sanic request's `raw_args`, which contains the
            query params that came in as part of the request.
        *valid_params: The query parameter keys that are valid for the request.

    Returns:
        dict: A dictionary that maps the supported query parameters found in
            the request with their values.
    """
    params = {}
    for k, v in raw_args.items():
        if k not in valid_params:
            raise errors.InvalidArgumentsError(
                gettext('Invalid query param: {} (valid params: {})').format(k, valid_params)
            )
        params[k] = v
    return params