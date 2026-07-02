from modules.log_parser import parse_log

logs = parse_log("sample_logs/sample.log")

for log in logs:
    print(log)
