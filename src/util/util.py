import  pytz
from datetime import datetime, timezone

class Utility:

    @staticmethod
    def epoch_to_datetime(epoch_time):
        """Convert epoch time to a human-readable datetime."""
        # The epoch time should be in seconds. If you have milliseconds, divide by 1000.
        #date_time = datetime.fromtimestamp(epoch_time)
        date_time = datetime.fromtimestamp(epoch_time, pytz.utc)
        return date_time.strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def datetime_to_epoch(date_time_str, date_format="%Y-%m-%d %H:%M:%S", timezone_str="UTC"):
        """Convert a date-time string to an epoch timestamp."""
        timezone = pytz.timezone(timezone_str)
        datetime_obj = datetime.strptime(date_time_str, date_format)
        datetime_obj_tz = timezone.localize(datetime_obj)  # Make the datetime object timezone-aware
        epoch = int(datetime_obj_tz.timestamp())
        return epoch

    @staticmethod
    def get_utc_rounded_down(datetime_input: datetime):
        """Rounds the datetime down to the nearest 4 hour datetime"""
        rounded_hour = (datetime_input.hour // 4) * 4
        rounded_down = datetime_input.replace(hour=rounded_hour, minute=0, second=0, microsecond=0)
        return rounded_down