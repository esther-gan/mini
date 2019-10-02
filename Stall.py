import datetime
from dateutil.parser import parse
import random

class Stall:
    
    # initialize information, parse times into objects
    # eg Info('macs', '08:00', '23:00', '01234', [])
    # 0 is monday
    def __init__(self, name, _open, close, days, menu):
        self.name = name
        self._open= parse(_open).time()
        self.close = parse(close).time()
        self.days = days
        #menu = {}
        self.menu = menu
        
    def is_open(self):
        now = datetime.datetime.today()

        # verifies if stall opens over midnight
        if (self._open) < (self.close):
            
            # checks if open based on time and dates
            if (self._open < now.time() < self.close) and (str(now.weekday()) in self.days):
                return True
            
        # if stall opens over midnight
        elif self._open > self.close:
            pass
        
    def is_breakfast(self):
        now = datetime.datetime.today()
        
        # parse changes 12:00 to a time obj so as to perform time arithmetics
        if self._open < now.time() < parse('12:00').time():
            return True
        
    def waiting_time(self, pax):
        total_time = 0
        
        # random float for time taken per pax
        for ppl in range(pax):
            time_taken = random.uniform(1, 3)
            total_time += time_taken
            
        # returns rounded time
        return int(total_time)