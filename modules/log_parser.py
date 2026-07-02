import os


def parse_log(file_path):
    """
    Reads a log file and returns a list of log entries.
    """

    logs = []

    if not os.path.exists(file_path):
        return logs

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()

            if line:
                logs.append(line)

    return logs

