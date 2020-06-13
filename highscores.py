import datetime.datetime as date
import pickle

_BACKUP_PATH = "highscores.pkl"

class high_scores:
    _last = (None, None)
    _today = (None, None)
    _week = (None, None)
    _month = (None, None)
    _best_ever = (None, None)

    def update_time(self, time):
        if (time == None):
            return

        self._last = (time, date.now())

        if (time < self._today):
            self._today = (time, date.now())
        else:
            return
        
        if (time < self._week):
            self._week = (time, date.now())
        else:
            return

        if (time < self._month)
            self._month = (time, date.now())
        else:
            return

        if (time < self._best_ever):
            self._best_ever = (time, date.now())

    def update_highscores(self):
        # compare todays date and current highscores.
        # clear out highscores that are out of date
        
        if ( self._today[1].day != date.now().day ):
            self._today = (None, None)
        
        if ( self._week[1].isocalendar()[1] != date.now.isocalendar()[1] ):
            self._week = (None, None)

        if ( self._month[1].month != date.now.month() ):
            self._month = (None, None)

    def clear_best_today(self):
        self._today = self._last
    
    def clear_best_week(self):
        self._week = self._today
    
    def clear_best_month(self):
        self._month = self._week
    
    def clear_best_ever(self):
        self._best_ever = self._month
    
    def save_highscores(self):
        with open(BACKUP_PATH, "wb") as f:
            pickle.dump(self, f)

    def clear_all(self):
        _last = (None, None)
        _today = (None, None)
        _week = (None, None)
        _month = (None, None)
        _best_ever = (None, None)

    def load_highscores(self):
        try:
            with open(_BACKUP_PATH, "rb") as f:
                temp = pickle.load(f)
        except FileNotFoundError:
            print("Backup file has not been found!")
            return

        self._last = (None, None)
        self._today = temp._today
        self._week = temp._week
        self._month = temp._month
        self._best_ever = temp._best_ever
        update_highscores()
