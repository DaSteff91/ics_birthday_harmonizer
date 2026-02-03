"""
Module responsible for generating RFC 5545 compliant ICS files.
This serves as the 'Harmonizer' output engine.
"""

import uuid
import logging
from datetime import datetime, timedelta
from typing import List
from icalendar import Calendar, Event, Alarm
from src.models import BirthdayEntry
from src.config import DEFAULT_ALARM_HOURS

logger = logging.getLogger(__name__)


class ICSGenerator:
    """
    Generates a standardized iCalendar from internal BirthdayEntry models.
    """

    def __init__(self) -> None:
        """Initializes the generator with a clean VCALENDAR structure."""
        self.cal = Calendar()
        self.cal.add("prodid", "-//Birthday Harmonizer//EN")
        self.cal.add("version", "2.0")
        self.cal.add("x-wr-calname", "Harmonized Birthdays")

    def _create_event(self, entry: BirthdayEntry) -> Event:
        """
        Transforms a BirthdayEntry into a standardized VEVENT.

        Args:
            entry (BirthdayEntry): The internal data model.

        Returns:
            Event: A fully populated and harmonized iCalendar event.
        """
        event = Event()

        # Identity and Timestamps
        event.add("uid", str(uuid.uuid4()))
        event.add("dtstamp", datetime.now())
        event.add("created", datetime.now())

        # Core Birthday Data
        event.add("summary", entry.name)
        event.add("dtstart", entry.birth_date)
        # End date is start date + 1 day for all-day events
        event.add("dtend", entry.birth_date + timedelta(days=1))
        event.add("rrule", {"freq": "yearly"})

        # Metadata and State
        year_text = str(entry.birth_date.year) if entry.has_year else "Unknown"
        event.add("description", f"Born: {year_text}")
        event.add("categories", ["Birthday"])
        event.add("transp", "TRANSPARENT")
        event.add("status", "CONFIRMED")
        event.add("class", "PUBLIC")

        # Harmonized Alarm ()
        alarm = Alarm()
        alarm.add("action", "DISPLAY")
        alarm.add("description", f"Birthday Reminder: {entry.name}")
        # PT9H = 9 hours after the start of the event (09:00 AM)
        alarm.add(
            "trigger",
            timedelta(hours=DEFAULT_ALARM_HOURS),
            parameters={"RELATED": "START"},
        )
        event.add_component(alarm)

        return event

    def build(self, entries: List[BirthdayEntry]) -> bytes:
        """
        Constructs the final ICS content from a list of entries.

        Args:
            entries (List[BirthdayEntry]): The data to be written.

        Returns:
            bytes: The serialized ICS file content.
        """
        for entry in entries:
            self.cal.add_component(self._create_event(entry))

        return self.cal.to_ical()
