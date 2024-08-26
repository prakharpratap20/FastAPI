from typing import Annotated, get_type_hints, get_origin, get_args
from functools import wraps


# The check_value_range decorator will check if the value of the argument is
# within the specified range.
def check_value_range(func):
    """
    Check if the value of the argument is within the specified range.
    """
    @wraps(func)
    def wrapped(x):
        type_hints = get_type_hints(func, include_extras=True)
        hint = type_hints["x"]

        if get_origin(hint) is Annotated:
            hint_type, *hint_args = get_args(hint)
            low, high = hint_args[0]

            if not low <= x <= high:
                raise ValueError(f"Value {x} is not between {low} and {high}")

        # execute the original function
        return func(x)
    return wrapped
