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
    
# Example usage
if __name__ == "__main__":

    print(Utility.datetime_to_epoch("2024-3-21 00:00:00", "%Y-%m-%d %H:%M:%S", "UTC"))
    print(Utility.epoch_to_datetime(1710979200))
    round_epoch = int(Utility.get_utc_rounded_down(datetime.now(timezone.utc)).timestamp())
    print(round_epoch)
    print(Utility.epoch_to_datetime(round_epoch))


    start = Utility.datetime_to_epoch("2024-2-1 00:00:00", "%Y-%m-%d %H:%M:%S", "UTC")
    print(f"back port test start: {start}")

    end = Utility.datetime_to_epoch("2024-3-01 00:00:00", "%Y-%m-%d %H:%M:%S", "UTC")
    print(f"back port test end: {end}")

    months = [
        "2024-3-1 00:00:00",
        "2024-2-1 00:00:00",
        "2024-1-1 00:00:00",
        "2023-12-1 00:00:00",
        "2023-11-1 00:00:00",
        "2023-10-1 00:00:00",
        "2023-9-1 00:00:00",
        "2023-8-1 00:00:00",
        "2023-7-1 00:00:00",
        "2023-6-1 00:00:00",
        "2023-5-1 00:00:00",
        "2023-4-1 00:00:00",
    ]

    for month in months:
        month_epoch = Utility.datetime_to_epoch(month, "%Y-%m-%d %H:%M:%S", "UTC")
        month_1_hour_back_epoch = month_epoch - 3600
        month_1_hour_back = Utility.epoch_to_datetime(month_1_hour_back_epoch)

        datetime_obj = datetime.strptime(month_1_hour_back, "%Y-%m-%d %H:%M:%S")
        datetime_obj = datetime_obj.replace(tzinfo=timezone.utc)
        start_of_month = datetime(datetime_obj.year, datetime_obj.month, 1, tzinfo=timezone.utc)
        start_of_month_epoch = int(start_of_month.timestamp())
        
        #print(f"{start_of_month}:{start_of_month_epoch}\t{month_1_hour_back}:{month_1_hour_back_epoch}")
        print(f"({start_of_month_epoch},{month_1_hour_back_epoch}),")