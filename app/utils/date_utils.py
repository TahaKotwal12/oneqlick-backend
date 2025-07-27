import re
from dateutil import parser
import pytz


def parse_date_range(date_range: str):
    """
    Parse date range string into start and end dates.
    
    Args:
        date_range: Date range in format '2025-05-17T22:49:01Z-2025-06-17T05:29:59Z'
        
    Returns:
        Tuple of (start_date, end_date) as datetime objects (converted to UTC)
    """    
    try:
        # Use regex to split the datetime range with timezone format
        # Pattern matches ISO datetime with Z timezone, followed by a hyphen, followed by another ISO datetime
        pattern = r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)-(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z)'
        match = re.match(pattern, date_range)
        
        if not match:
            raise ValueError(f"Invalid date range format. Expected format: '2025-05-17T22:49:01Z-2025-06-17T05:29:59Z'")
        
        start_datetime_str = match.group(1)
        end_datetime_str = match.group(2)
        
        # Parse ISO datetime strings with timezone information
        start_date = parser.isoparse(start_datetime_str)
        end_date = parser.isoparse(end_datetime_str)
        
        # Convert to UTC for consistent server-side processing
        if start_date.tzinfo is not None:
            start_date = start_date.astimezone(pytz.UTC).replace(tzinfo=None)
        if end_date.tzinfo is not None:
            end_date = end_date.astimezone(pytz.UTC).replace(tzinfo=None)
        
        return start_date, end_date
        
    except Exception as e:
        raise ValueError(f"Invalid date format. Expected format: '2025-05-17T22:49:01Z-2025-06-17T05:29:59Z'. Error: {str(e)}")
