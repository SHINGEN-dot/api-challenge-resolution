from tools import decorator

@decorator.catch_exceptions
def round_float(float_number: float, digit: int):
    """ Round float number with 3 digits """
    return round(float_number, digit)
