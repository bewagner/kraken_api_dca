from datetime import date
from pathlib import Path


class Logger:
    """
    Logger that prints to stdout and also writes to a file
    """
    def __init__(self, log_file: str):
        self.__logs = ""
        self.__logging_date = date.today().strftime("%d.%m.%Y")
        self.__log_file = Path(log_file)

        if not self.__log_file.exists():
            self.__log_file.touch()

    def __del__(self):
        """
        Use RAII to write the logs at the end of the script
        """
        if not self.__logs:
            return

        with self.__log_file.open("a") as log_file:
            log_file.write("\n\n")
            log_file.write(self.__logging_date)
            log_file.write(self.__logs)

    def log(self, s: str):
        """
        Log a string. That is print it and add it to the string we print to the file at the end of the script.
        :param s: String to log
        """
        self.__logs += "\n" + s
        print(s)
