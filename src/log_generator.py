"""Generate fake logs."""

from __future__ import annotations

import random
import time
from datetime import UTC, datetime
from pathlib import Path

from faker import Faker


class LogGenerator:
    """Generate fake logs."""

    def __init__(self: LogGenerator) -> None:
        """Initialize the LogGenerator."""
        self.log_line = """\
            {remote_addr} - - [{time_local} +0000] "{request_type} {request_path} HTTP/1.1" {status} {body_bytes_sent} "{http_referer}" "{http_user_agent}"\
        """
        log_dir = Path(__file__).parent.parent
        self.log_file_a = Path(log_dir / "log_a.txt")
        self.log_file_b = Path(log_dir / "log_b.txt")
        self.log_max = 100

    def generate_log_line(self: LogGenerator) -> str:
        """Generate a fake log line."""
        fake = Faker()
        now = datetime.now(tz=UTC)
        return self.log_line.format(
            remote_addr=fake.ipv4(),
            time_local=now.strftime("%d/%b/%Y:%H:%M:%S"),
            request_type=random.choice(["GET", "POST", "PUT"]),
            request_path="/" + fake.uri_path(),
            status=random.choice([200, 401, 404]),
            body_bytes_sent=random.choice(range(5, 1000, 1)),
            http_referer=fake.uri(),
            http_user_agent=fake.user_agent(),
        )

    @staticmethod
    def write_log_line(log_file: Path, line: str) -> None:
        """Write a log line to a file."""
        with open(log_file, "a") as file:
            file.write(line)
            file.write("\n")

    @staticmethod
    def clear_log_file(log_file: Path) -> None:
        """Clear the log file."""
        with open(log_file, "w+") as file:
            file.write("")

    def generate(self: LogGenerator) -> None:
        """Generate logs."""
        # Initialize the log files
        current_log_file = self.log_file_a
        lines_written = 0
        self.clear_log_file(self.log_file_a)
        self.clear_log_file(self.log_file_b)

        # Generate logs
        while True:
            line = self.generate_log_line()
            self.write_log_line(current_log_file, line)
            lines_written += 1
            if lines_written % self.log_max == 0:
                new_log_file = self.log_file_b
                if current_log_file == self.log_file_b:
                    new_log_file = self.log_file_a
                self.clear_log_file(new_log_file)
                current_log_file = new_log_file
            sleep_time = random.choice(range(1, 5, 1))
            time.sleep(sleep_time)


def main() -> None:
    """Run the main function."""
    log_generator = LogGenerator()
    log_generator.generate()


if __name__ == "__main__":
    main()
