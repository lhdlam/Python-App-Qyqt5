import re
from decimal import *

from config import RegexHalfWidth


def validateIntegerField(value=None):
    check = False
    try:
        if value and ((isinstance(value, str) and value.isdigit()) or isinstance(value, int)):
            check = True
    except ValueError:
        check = False
    return check


def validateIntegerOrBlankField(value=None):
    check = False
    try:
        if not value or (isinstance(value, str) and value.isdigit()) or isinstance(value, int):
            check = True
    except ValueError:
        check = False
    return check


def validateStringField(value=None):
    check = False
    if value and isinstance(value, str):
        check = True
    return check


def validateStringOrBlankField(value=None):
    check = False
    if not value or isinstance(value, str):
        check = True
    return check


def validateDecimaFiniteField(value=None):
    check = False
    if value and Decimal(value).is_finite() is True:
        check = True
    return check


def validateDecimaFiniteOrNoneField(value=None):
    check = False
    if not value or Decimal(value).is_finite() is True:
        check = True
    return check


def validateMaxLength(value, length):
    check = False
    pattern = re.compile(RegexHalfWidth.regex)
    if not value:
        check = False
    if isinstance(value, str) and length != 56 and len(value) <= length:
        check = True
    if isinstance(value, str) and length == 56 and len(value) <= length and pattern.match(value):
        check = True
    return check


def validateNumeric(value=None):
    check = False
    if value and value.isnumeric():
        check = True
    return check
