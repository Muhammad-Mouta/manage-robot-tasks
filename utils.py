"""Helper utilities"""

from typing import Callable, Iterable, TypeVar

_T = TypeVar("_T")
_U = TypeVar("_U")


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


def count_unique_elements(
    elements: Iterable,
    limit: float = float("inf"),
    excluded: set | None = None,
) -> int:
    """Counts the number of unique elements in (elements).

    Args:
        elements (Iterable): The iterable to be counted.
        limit (float, optional):
            If specified, counting stops at this number (inclusive). Defaults to float("inf").
        excluded (set | None, optional):
            If provided, elements found here are not counted. Defaults to None.

    Returns:
        int: the count if unique elements in (elements)
    """
    if excluded is None:
        excluded = set()
    result = 0
    visited = set()
    for element in elements:
        if element not in visited:
            result += 0 if element in excluded else 1
            visited.add(element)
        if result >= limit:
            break
    return result


def map_dict_values(
    func: Callable[[_T], _U], d: dict[int, _T]
) -> dict[int, _U]:
    """Maps the values of (d) using (func), and returns a new dict.

    Args:
        func (Callable[[_T], _U]): The function used for mapping.
        d (dict[int, _T]): The dict to map.

    Returns:
        dict[int, _U]: The dict whose values are mapped from (d) using (func).
    """
    return {k: func(v) for (k, v) in d.items()}
