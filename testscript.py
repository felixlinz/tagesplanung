import pytest 
from data_manager import PathManager
from datetime import timedelta
from datetime import date
from data_manager import get_next_file_day

path_manager = PathManager()
path_manager.save_path("")
print(get_next_file_day(date.today()))