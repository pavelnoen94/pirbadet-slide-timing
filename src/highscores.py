from datetime import datetime as date
import pickle


class high_scores:
    BACKUP_PATH = "highscores.pkl"
    last = (None, None)
    today = (None, None)
    week = (None, None)
    month = (None, None)
    best_ever = (None, None)

    def update_time(self, time):
        if (time == None):
            return

        self.last = (time, date.now())

        if (time < self.today):
            self.today = (time, date.now())
        else:
            return

        if (time < self.week):
            self.week = (time, date.now())
        else:
            return

        if (time < self.month):
            self.month = (time, date.now())
        else:
            return

        if (time < self.best_ever):
            self.best_ever = (time, date.now())

    def update_highscores(self):
        # compare todays date and current highscores.
        # clear out highscores that are out of date

        if ( self.today[1].day != date.now().day ):
            self.today = (None, None)

        if ( self.week[1].isocalendar()[1] != date.now.isocalendar()[1] ):
            self.week = (None, None)

        if ( self.month[1].month != date.now.month() ):
            self.month = (None, None)

    def clear_best_today(self):
        self.today = self.last

    def clear_best_week(self):
        self.week = self.today

    def clear_best_month(self):
        self.month = self.week

    def clear_best_ever(self):
        self.best_ever = self.month

    def save_highscores(self):
        with open(self.BACKUP_PATH, "wb") as f:
            pickle.dump(self, f)

    def clear_all(self):
        self.last = (None, None)
        self.today = (None, None)
        self.week = (None, None)
        self.month = (None, None)
        self.best_ever = (None, None)

    def load_highscores(self):
        try:
            with open(self.BACKUP_PATH, "rb") as f:
                temp = pickle.load(f)
        except FileNotFoundError:
            print("Backup file has not been found!")
            return

        self.last = (None, None)
        self.today = temp._today
        self.week = temp._week
        self.month = temp._month
        self.best_ever = temp._best_ever
        self.update_highscores()
