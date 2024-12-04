"""Helper utilities"""


def is_positive_int(value, nonzero=False) -> bool:
    """Checks if (value) is a positive integer.

    Args:
        value: The value to check
        nonzero (bool, optional):
            If True, the function returns False if (value == 0). Defaults to False.

    Returns:
        bool: True if (value) is a positive integer.
    """
    return isinstance(value, int) and (
        value >= 0 if not nonzero else value > 0
    )
