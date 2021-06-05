from datetime import datetime

from logger import Logger

now = datetime.now()

current_time = now.strftime("%H:%M:%S")

l = Logger("test_logs.txt")
l.log(current_time)
l.log("Blabla")
