import requests
from datetime import datetime


# class for load and processing data
class ParserRate:
    def __init__(self, patch: str):
        self.patch = patch
        # loading data or generation except
        try:
            self.data_list = requests.get(self.patch).json()
        except requests.ConnectionError:
            raise ConnectionError

    # function for setting window elements
    def return_first_end_data(self):
        data_first = datetime.strptime(self.data_list[0][0], '%m/%d/%Y')
        data_last = datetime.strptime(self.data_list[-1][0], '%m/%d/%Y')
        data_next_last = datetime.strptime(self.data_list[-2][0], '%m/%d/%Y')
        data_next_first = datetime.strptime(self.data_list[1][0], '%m/%d/%Y')
        return data_first, data_last, data_next_last, data_next_first

    # function procesing data
    def return_data(self, date_start, date_end):
        start = len(self.data_list) - (datetime.strptime(self.data_list[-1][0], '%m/%d/%Y') -
                                       datetime.strptime(date_start, '%d.%m.%Y')).days
        end = len(self.data_list) - (datetime.strptime(self.data_list[-1][0], '%m/%d/%Y') -
                                     datetime.strptime(date_end, '%d.%m.%Y')).days

        if end < start:
            raise ValueError

        return self.data_list[start:end]
