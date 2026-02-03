from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class BirthdayEntry:
    """
    Standardized internal representation of a Birthday.

    Attributes:
        name: The full name of the person.
        birth_date: The date of birth (Year may be 1604 if unknown).
        original_uid: The UID from the source file for tracking.
        has_year: Boolean indicating if the birth year was actually found.
    """

    name: str
    birth_date: date
    original_uid: Optional[str] = None
    has_year: bool = False
