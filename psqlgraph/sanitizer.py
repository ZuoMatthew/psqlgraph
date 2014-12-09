from sqlalchemy.dialects.postgres import TIMESTAMP, INTEGER, TEXT, FLOAT
from sqlalchemy import DateTime
from datetime import datetime
from types import NoneType
from exc import ProgrammingError
import time

import copy

type_mapping = {
    int: INTEGER,
    str: TEXT,
    float: FLOAT,
    datetime: TIMESTAMP,
    NoneType: NoneType,
}

type_conversion = {
    int: int,
    str: str,
    float: float,
    datetime: lambda x: time.mktime(x.timetuple()) * 1000,
    NoneType: lambda x: None,
}


def cast(variable):
    if type(variable) not in type_conversion:
        raise ProgrammingError(
            'Disallowed value type for jsonb properties')
    return type_conversion[type(variable)](variable)


def sanitize(variable):
    if not isinstance(variable, dict):
        return cast(variable)
    variable = copy.deepcopy(variable)
    for key, value in variable.iteritems():
        variable[key] = cast(value)
    return variable


def get_type(variable):
    return type_mapping.get(type(variable), TEXT)
