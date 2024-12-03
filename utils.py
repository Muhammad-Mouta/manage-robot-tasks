def is_positive_int(value, nonzero=False):
    return isinstance(value, int) and (
        value >= 0 if not nonzero else value > 0
    )
