import datetime
import time

class Transaction :

    def __init__(self, From:str, To:str, data:str):
        self.From = From
        self.To = To
        self.data = data
        self.date_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    def toString(self) -> str :
        ret = "from : " + self.From + "\n"
        ret += "to : " + self.To + "\n"
        ret += "data : " + self.data + "\n"
        ret += "date time : " + self.date_time + "\n"
        return ret

    def msg(self) -> str:
        return self.From + " " + self.To + " " + self.data + " " + self.date_time

