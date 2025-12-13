import calendar
from datetime import datetime
import datetime as dt

def get_month_weeks(year: int) -> list[int]:
    """Get the week number of the first day for each month for the given year."""
    month_weeks = []
    for month in range(1, 13):
        # Simply take the 1st of the month
        first_day = dt.date(year, month, 1)
        # isocalendar returns (year, week, weekday)
        first_day_week = first_day.isocalendar()[1]
        
        # Handle edge case where Jan 1st is in week 52/53 of prev year
        if month == 1 and first_day_week > 50:
            first_day_week = 1
            
        month_weeks.append(first_day_week)
    return month_weeks

def build_date_from_pieces(row: dict) -> dt.date:
    """Reconstruct a date object from year, week, and day name parts."""
    # Using %W (week number 00-53) and %A (full weekday name)
    date_obj = datetime.strptime(f"{row['year']}-{row['week']}-{row['day_of_week_str']}", "%Y-%W-%A")
    return date_obj.date()
