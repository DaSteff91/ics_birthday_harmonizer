"""
Module responsible for parsing and sanitizing legacy ICS files.
It handles the 'heavy lifting' of extracting meaningful data from
non-standard or messy iCalendar entries.
"""

import re
import logging
from datetime import date
from typing import List, Optional
from icalendar import Calendar, Event
from src.models import BirthdayEntry
from src.config import SENTINEL_YEAR

logger = logging.getLogger(__name__)


class ICSParser:
    """
    A robust parser for converting legacy ICS events into BirthdayEntry models.

    It employs various strategies (waterfall logic) to find names and years
    even when the source file is inconsistent or missing fields.
    """

    def __init__(self, file_path: str):
        """
        Initializes the parser with a path to an ICS file.

        Args:
            file_path (str): The filesystem path to the source .ics file.
        """
        self.file_path = file_path

    def _extract_year(self, text: str) -> Optional[int]:
        """
        Regex-based helper to find a 4-digit year.

        Scans the input text for a year beginning with 19 or 20.

        Args:
            text (str): The string to search (usually SUMMARY or DESCRIPTION).

        Returns:
            Optional[int]: The extracted year as an integer if found, else None.
        """
        match = re.search(r"\b(19|20)\d{2}\b", text)
        return int(match.group(0)) if match else None

    def _clean_name(self, summary: str, uid: str) -> str:
        """
        Ensures a valid name exists for the calendar entry.

        If the summary is empty, it generates a placeholder based on the UID
        to ensure the user can still identify the entry in their calendar.

        Args:
            summary (str): The existing SUMMARY field from the ICS.
            uid (str): The UID of the event used for fallback identification.

        Returns:
            str: A cleaned name or a descriptive fallback.
        """
        name = summary.strip()
        if not name:
            logger.warning(f"Empty summary found for UID: {uid}. Using placeholder.")
            return f"Unknown Birthday ({uid[:8]})"
        return name

    def parse(self) -> List[BirthdayEntry]:
        """
        Main execution method for the parser.

        Iterates through the ICS file, filters for VEVENTs, and applies
        the harmonization logic to create a list of BirthdayEntry objects.

        Returns:
            List[BirthdayEntry]: A collection of harmonized internal models.
        """
        entries: List[BirthdayEntry] = []

        try:
            with open(self.file_path, "rb") as f:
                content = f.read().decode("utf-8")
                cal = Calendar.from_ical(content)
        except Exception as e:
            logger.error(f"Failed to read file {self.file_path}: {e}")
            return entries

        for event in cal.walk("VEVENT"):
            if not isinstance(event, Event):
                continue

            # 1. Extract Basic Data
            uid = str(event.get("UID", "no-uid"))
            summary = str(event.get("SUMMARY", ""))
            description = str(event.get("DESCRIPTION", ""))
            dtstart = event.get("DTSTART").dt

            # Ensure we are working with a date object
            if not isinstance(dtstart, date):
                logger.debug(f"Skipping non-date event: {summary}")
                continue

            # 2. Waterfall Year Extraction
            # Check description first, then summary, then DTSTART if it's old
            birth_year = self._extract_year(description) or self._extract_year(summary)

            has_year = True
            if not birth_year:
                # If DTSTART year is reasonably in the past, treat it as birth year
                if dtstart.year < date.today().year - 1:
                    birth_year = dtstart.year
                else:
                    birth_year = SENTINEL_YEAR
                    has_year = False

            # 3. Create Model
            entry = BirthdayEntry(
                name=self._clean_name(summary, uid),
                birth_date=date(birth_year, dtstart.month, dtstart.day),
                original_uid=uid,
                has_year=has_year,
            )
            entries.append(entry)
            logger.debug(
                f"Parsed: {entry.name} (Year: {birth_year if has_year else 'Unknown'})"
            )

        return entries
