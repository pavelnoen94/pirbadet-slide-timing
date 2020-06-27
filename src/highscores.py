from datetime import datetime as date
import pickle


class high_scores:


    def __init__(self, name):
        self.backup_path = name + ".highscores.pkl"
        self.last = (None, None)
        self.today = (None, None)
        self.week = (None, None)
        self.month = (None, None)
        self.best_ever = (None, None)
        self.load_highscores()

        return


    def add_time(self, time):
        if (time == None):
            return

        self.last = (time, date.now())

        try:
            if (time < self.today[0]):
                self.today = (time, date.now())
            else:
                return
        except TypeError:
            self.today = (time, date.now())

        try:
            if (time < self.week[0]):
                self.week = (time, date.now())
            else:
                return
        except TypeError:
            self.week = (time, date.now())

        try:
            if (time < self.month[0]):
                self.month = (time, date.now())
            else:
                return
        except TypeError:
            self.month = (time, date.now())

        try:
            if (time < self.best_ever[0]):
                self.best_ever = (time, date.now())
        except TypeError:
            self.best_ever = (time, date.now())

        return


    def update_highscores(self):
        # compare todays date and current highscores.
        # clear out highscores that are out of date

        try:
            if (self.today[1].day != date.now().day):
                self.today = (None, None)
        except AttributeError:
            self.today = (None, None)
        try:
            if (self.week[1].isocalendar()[1] != date.now.isocalendar()[1]):
                self.week = (None, None)
        except AttributeError:
            self.week = (None, None)
        try:
            if (self.month[1].month != date.now.month()):
                self.month = (None, None)
        except AttributeError:
            self.month = (None, None)

        return


    def save_highscores(self):
        with open(self.backup_path, "wb") as f:
            pickle.dump(self, f)

        return


    def clear_all(self):
        self.last = (None, None)
        self.today = (None, None)
        self.week = (None, None)
        self.month = (None, None)
        self.best_ever = (None, None)

        return


    def load_highscores(self):
        try:
            with open(self.backup_path, "rb") as f:
                temp = pickle.load(f)
                self.last = (None, None)
                self.today = temp.today
                self.week = temp.week
                self.month = temp.month
                self.best_ever = temp.best_ever
                self.update_highscores()
        except FileNotFoundError:
            pass

        return


    def print_highscores(self):
        print()
        print("highscores:")

        if (self.last[0] != None):
            print("last: " + str(self.last[0]) +"s")

        if (self.today[0] != None):
            print("today: " + str(self.today[0]) +"s")

        if (self.week[0] != None):
            print("week: " + str(self.week[0]) +"s")

        if (self.month[0] != None):
            print("month: " + str(self.month[0]) +"s")

        if (self.best_ever[0] != None):
            print("best_ever: " + str(self.best_ever[0]) +"s")

        return
