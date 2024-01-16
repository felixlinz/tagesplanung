from data_manager import get_next_working_day
from data_manager import format_date_with_weekday
from data_manager import learn_data_from_excel
from datetime import datetime


# Example usage
print(learn_data_from_excel(datetime.today()))