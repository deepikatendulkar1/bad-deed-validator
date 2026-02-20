"""
Custom exception classes for deed validation errors.
"""
class CountyNotFoundError(Exception):
    """
    Raised when the provided county cannot be found in the dataset (reference dataset) which is given.
    """
    pass
class AmountMismatchError(Exception):
    """
    Raised when the numeric amount does not match the written amount in words.
    """
    pass
class DateLogicError(Exception):
    """
    Raised when there is a logical issue between the signed date and the recorded date.
    """
    pass