from enum import Enum

class Operator(str, Enum):
    EQUALS = "EQUALS"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    CONTAINS = "CONTAINS"

class SortOrder(str, Enum):
    ASC = "ASC"
    DESC = "DESC"