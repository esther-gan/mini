import datetime
from dateutil.parser import parse

class Stall:
    
    # initialize information, parse times into objects
    # eg Info('macs', '08:00', '23:00', '01234', [])
    # 0 is monday
    def __init__(self, name, _open, close, days, menu):
        self.name = name
        self._open= parse(_open).time()
        self.close = parse(close).time()
        self.days = days
        self.menu = menu
        
    def now_open(self):
        now = datetime.datetime.today()
            
        # checks if open based on time and dates
        if (self._open < now.time() < self.close) and (str(now.weekday()) in self.days):
            return True
        
    def is_open(self, _open, close, days):
        # checks if open based on time and dates
        if (self._open <= _open) and (self.close >= close) and (days in self.days):
            return True