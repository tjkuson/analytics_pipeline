"""Count the number of unique visitors to a website."""
from __future__ import annotations

import sqlite3
import time
from datetime import UTC, datetime


class VisitorCounter:
    """Count the number of unique visitors to a website."""

    def __init__(self: VisitorCounter) -> None:
        """Initialize the VisitorCounter."""
        self.conn_str = "db.sqlite"

    def get_lines(self: VisitorCounter, timestamp: datetime) -> list[tuple[str, str]]:
        """Get the lines from the logs table after a certain time."""
        with sqlite3.connect(self.conn_str) as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT remote_addr,time_local FROM logs WHERE created > ?",
                (timestamp,),
            )
            return cur.fetchall()

    @staticmethod
    def parse_time(time_str: str) -> datetime:
        """Parse the time from the log line."""
        return datetime.strptime(time_str, "[%d/%b/%Y:%H:%M:%S %z]")

    def get_time_and_ip(
        self: VisitorCounter, lines: list[tuple[str, str]]
    ) -> tuple[tuple[str, ...], tuple[datetime, ...]]:
        """Get the time and IP address from the lines."""
        ips, times = zip(
            *((line[0], self.parse_time(line[1])) for line in lines), strict=True
        )
        return ips, times

    def unique_visitors(self: VisitorCounter) -> None:
        """Count the number of unique visitors to the site."""
        unique_ips: dict[str, set[str]] = {}
        counts = {}
        start_time = datetime(year=2017, month=3, day=9, tzinfo=UTC)
        while True:
            # Get information from the database
            lines = self.get_lines(start_time)
            ips, times = self.get_time_and_ip(lines)
            if times:
                # Set the start time to the last time in the list
                start_time = times[-1]

            # Count the unique IPs
            for ip, time_obj in zip(ips, times, strict=True):
                day = time_obj.strftime("%d-%m-%Y")
                if day not in unique_ips:
                    unique_ips[day] = set()
                unique_ips[day].add(ip)
            for day_key, day_counts in unique_ips.items():
                counts[day_key] = len(day_counts)

            # Sort the counts by date
            count_list = sorted(counts.items(), key=lambda x: x[0])

            print(f"\n{datetime.now(tz=UTC)}")
            for item in count_list:
                print(f"{item[0]}: {item[1]}")

            time.sleep(5)


if __name__ == "__main__":
    counter = VisitorCounter()
    counter.unique_visitors()
