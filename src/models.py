"""
This module defines the internal data models for the birthday harmonizer.
It ensures that data extracted from various ICS sources is validated
and type-safe before being transformed.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class BirthdayEntry:
    """
    Represents a standardized birthday event.

    This model serves as the 'Single Source of Truth' within the application,
    stripping away ICS-specific metadata in favor of pure birthday data.

    Attributes:
        name (str): The cleaned full name of the person.
        birth_date (date): The calculated date of birth.
            Uses SENTINEL_YEAR if the year is unknown.
        original_uid (Optional[str]): The UID from the source ICS file,
            preserved for logging and traceability during the migration.
        has_year (bool): Flag indicating if a valid birth year was found
            in the source metadata or if the sentinel was used.
    """

    name: str
    birth_date: date
    original_uid: Optional[str] = None
    has_year: bool = False
