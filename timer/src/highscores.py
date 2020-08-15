from datetime import datetime as date
import pickle, os, json


class high_scores:


    def __init__(self, name, mqtt):
        self.backup_path = name + ".highscores.pkl"
        self.init_highscores()
        self.load_highscores()
        self.mqtt = mqtt

        return


    def load_highscores(self):
        try:
            if os.path.getsize(self.backup_path) > 0:
                with open(self.backup_path, "rb") as f:
                    temp = pickle.load(f)
                    self.highscores = temp
                    self.update_highscores()
        except (FileNotFoundError):
            # file not found. Start a new session
            print("[Info]: Saved high scores is not found. Starting a new session.")
            return


    def save_highscores(self):
        with open(self.backup_path, "wb") as f:
            pickle.dump(self.highscores, f)
        return


    def update_highscores(self):
        # clear out highscores that are "out of date"

        now = date.now()

        if (self.highscores["today"]["date"].day == now.day):
            return

        self.highscores["today"] =  {
            "time" : float(),
            "date" : now,
            "speed" : float()
            }

        if (self.highscores["week"]["date"].isocalendar()[1] == now.isocalendar()[1]):
            return

        self.highscores["week"] = {
            "time" : float(),
            "date" : now,
            "speed" : float()
            }

        if (self.highscores["month"]["date"].month == now.month):
            return

        self.highscores["month"] =  {
            "time" : float(),
            "date" : now,
            "speed" : float()
            }

        return


    def add_result(self, time, speed):
        if (time == None):
            return

        # update all records if the time is better
        for i in self.highscores:
            if(time < self.highscores[i]["time"] or self.highscores[i]["time"] == float()):
                self.highscores[i]["time"] = time
                self.highscores[i]["speed"] = speed
                self.highscores[i]["date"] = date.now()

        # update last time
        self.highscores["last"]["time"] = time
        self.highscores["last"]["speed"] = speed
        self.highscores["last"]["date"] = date.now()

        return


    def init_highscores(self):
        self.highscores =   {
                    "last" :
                        {
                            "time"  : float(),
                            "date"  : date.now(),
                            "speed" : float()
                        },
                    "today" :
                        {
                            "time"  : float(),
                            "date"  : date.now(),
                            "speed" : float()
                        },
                    "week" :
                        {
                            "time"  : float(),
                            "date"  : date.now(),
                            "speed" : float()
                        },
                    "month" :
                        {
                            "time"  : float(),
                            "date"  : date.now(),
                            "speed" : float()
                        },
                    "ever" :
                        {
                            "time"  : float(),
                            "date"  : date.now(),
                            "speed" : float()
                        }
                    }
        return
