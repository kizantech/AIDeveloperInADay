import datetime
from typing import Annotated
from semantic_kernel.functions import kernel_function


class DateTimePlugin:

    @kernel_function(description="Gets the current date and time")
    def get_current_date_time(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @kernel_function(description="Gets the year from a given date string in YYYY-MM-DD format")
    def get_year_from_date(self, date_str: Annotated[str, "The date string in YYYY-MM-DD format"]) -> Annotated[str, "The year from the date"]:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return str(date_obj.year)
        except ValueError:
            return "Invalid date format. Please provide date in YYYY-MM-DD format"

    @kernel_function(description="Gets the month from a given date string in YYYY-MM-DD format")
    def get_month_from_date(self, date_str: Annotated[str, "The date string in YYYY-MM-DD format"]) -> Annotated[str, "The month from the date"]:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return str(date_obj.month)
        except ValueError:
            return "Invalid date format. Please provide date in YYYY-MM-DD format"

    @kernel_function(description="Gets the day of the week from a given date string in YYYY-MM-DD format. Monday=0, Sunday=6")
    def get_day_of_week(self, date_str: Annotated[str, "The date string in YYYY-MM-DD format"]) -> Annotated[str, "The day of the week (Monday=0, Sunday=6)"]:
        try:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return str(date_obj.weekday())
        except ValueError:
            return "Invalid date format. Please provide date in YYYY-MM-DD format"
