from datetime import datetime
from dateutil import parser  # more flexible than strptime

def parse_date(date_str):
    if date_str.lower() in ["present", "now", "current"]:
        return datetime.today()
    try:
        return parser.parse(date_str)
    except Exception as e:
        print(f"⚠️ Failed to parse date '{date_str}': {e}")
        return None

def validate_timeline(experiences):
    flags = []
    for i in range(len(experiences) - 1):
        current = experiences[i]
        next_exp = experiences[i + 1]

        end_date = parse_date(current.get("end_date", ""))
        start_date = parse_date(next_exp.get("start_date", ""))

        if not end_date or not start_date:
            continue  # skip comparison if either date is invalid

        if start_date < end_date:
            flags.append(
                f"⚠️ Overlap: '{next_exp['job_title']}' at {next_exp['company']} starts before previous role ended."
            )
        elif (start_date - end_date).days > 365 * 2:
            flags.append(
                f"🕳️ Gap: More than 2 years between '{current['company']}' and '{next_exp['company']}'"
            )

    return flags
