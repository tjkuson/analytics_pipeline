"""Store logs in a SQLite database."""
from __future__ import annotations

import sqlite3
import time
from datetime import UTC, datetime
from pathlib import Path


class LogSaver:
    """Store logs in a SQLite database."""

    def __init__(self: LogSaver) -> None:
        """Initialize the LogSaver."""
        self.conn_str = "db.sqlite"
        self.create_table()
        log_dir = Path(__file__).parent.parent
        self.log_file_a = Path(log_dir / "log_a.txt")
        self.log_file_b = Path(log_dir / "log_b.txt")

    def create_table(self: LogSaver) -> None:
        """Create the logs table."""
        with sqlite3.connect(self.conn_str) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS logs (
                    raw_log TEXT NOT NULL UNIQUE,
                    remote_addr TEXT,
                    time_local TEXT,
                    request_type TEXT,
                    request_path TEXT,
                    status INTEGER,
                    body_bytes_sent INTEGER,
                    http_referer TEXT,
                    http_user_agent TEXT,
                    created DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

    @staticmethod
    def parse_line(line: str) -> list[str]:
        """Parse a line from the log file."""
        split_line = line.split(" ")
        if len(split_line) < 12:
            return []
        remote_addr = split_line[0]
        time_local = split_line[3] + " " + split_line[4]
        request_type = split_line[5]
        request_path = split_line[6]
        status = split_line[8]
        body_bytes_sent = split_line[9]
        http_referer = split_line[10]
        http_user_agent = " ".join(split_line[11:])
        created = datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%S")
        return [
            remote_addr,
            time_local,
            request_type,
            request_path,
            status,
            body_bytes_sent,
            http_referer,
            http_user_agent,
            created,
        ]

    def insert_record(self: LogSaver, line: str, parsed: list[str]) -> None:
        """Insert a record into the logs table."""
        with sqlite3.connect(self.conn_str) as conn:
            cur = conn.cursor()
            args = [line, *parsed]
            cur.execute("INSERT INTO logs VALUES (?,?,?,?,?,?,?,?,?,?)", args)
            conn.commit()

    def monitor_and_save(self: LogSaver) -> None:
        """Monitor the log files and save to the database."""
        with open(self.log_file_a, "w+") as file_a, open(
            self.log_file_b, "w+"
        ) as file_b:
            while True:
                line_a = file_a.readline()
                line_b = file_b.readline()
                if not line_a and not line_b:
                    # Wait one second and try again
                    time.sleep(1)
                    where_a = file_a.tell()
                    file_a.seek(where_a)
                    where_b = file_b.tell()
                    file_b.seek(where_b)
                    continue
                line = line_a.strip() if line_a else line_b.strip()
                parsed_line = self.parse_line(line)
                if parsed_line:
                    print("Saving log...")
                    self.insert_record(line, parsed_line)


def main() -> None:
    """Run the script."""
    log_saver = LogSaver()
    log_saver.monitor_and_save()  # Will run until you stop the script


if __name__ == "__main__":
    main()
