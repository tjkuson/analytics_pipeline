"""Count the number of browsers that have visited the site."""

from __future__ import annotations

import sqlite3
import time
from datetime import UTC, datetime

from count_visitors import VisitorCounter


class BrowserCounter(VisitorCounter):
    """Count the number of browsers that have visited the site."""

    def __init__(self: BrowserCounter) -> None:
        """Initialize the BrowserCounter."""
        super().__init__()
        self.browsers = ("Firefox", "Chrome", "Opera", "Safari", "MSIE")

    def get_lines(self: BrowserCounter, timestamp: datetime) -> list[tuple[str, str]]:
        """Get the lines from the logs table after a certain time."""
        with sqlite3.connect(self.conn_str) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT time_local,http_user_agent FROM logs WHERE created > ?",
                (timestamp,),
            )
            return cur.fetchall()

    def get_browser_and_time(
        self: BrowserCounter, lines: list[tuple[str, str]]
    ) -> tuple[tuple[str, ...], tuple[datetime, ...]]:
        """Get the browser and time from the lines."""
        browsers, times = zip(
            *(
                (self.parse_user_agent(line[1]), self.parse_time(line[0]))
                for line in lines
            ),
            strict=True,
        )
        return browsers, times

    def parse_user_agent(self: BrowserCounter, user_agent: str) -> str:
        """Parse the user agent string."""
        for browser in self.browsers:
            print(f"Checking for {browser} in {user_agent}")
            if browser in user_agent:
                return browser
        return "Other"

    def count_browsers(self: BrowserCounter) -> None:
        """Count the number of browsers that have visited the site."""
        browser_counts = {}
        start_time = datetime(year=2017, month=3, day=9, tzinfo=UTC)
        while True:
            # Get information from the database
            lines = self.get_lines(start_time)
            browsers, times = self.get_browser_and_time(lines)
            if times:
                # Set the start time to the last time in the list
                start_time = times[-1]
            for browser, _time_obj in zip(browsers, times, strict=True):
                if browser not in browser_counts:
                    browser_counts[browser] = 0
                browser_counts[browser] += 1

            # Sort the counts by date
            count_list = sorted(browser_counts.items(), key=lambda x: x[0])

            print(f"\n{datetime.now(tz=UTC)}")
            for item in count_list:
                print(f"{item[0]}: {item[1]}")

            time.sleep(5)


if __name__ == "__main__":
    bc = BrowserCounter()
    bc.count_browsers()
