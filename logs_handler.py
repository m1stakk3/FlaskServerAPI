import os
import sqlite3
import json
import logging
from datetime import datetime
from flask import make_response

DB_PATH = os.path.abspath("./logs_db")
logging.basicConfig(
    filename="work_log.log",
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s] %(message)s",
    datefmt="%H:%M:%S %d.%m.%y"
)


class DB:

    def __init__(self):
        logging.info("Create connection to Database")
        self.DB = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.SQL = self.DB.cursor()

    def insert_logs(self, message: str):
        """
        Insert logs into DB
        :param message: string value from site
        """
        logging.info(f"Insert message: {message}")
        if len(message) > 0:
            timestamp: str = datetime.now().strftime("%d.%m.%y %H:%M:%S")
            self.SQL.execute("insert into logs(timestamp, message) values ('{}', '{}')".format(timestamp, message))
            self.DB.commit()

    def get_last_ten_logs(self) -> list:
        """
        Get last 10 logs
        :return: list with 10 logs
        """
        logging.info("Get last ten logs and fetch result")
        return [(rec[0], rec[1]) for rec in self.SQL.execute("select timestamp, message from logs order by id desc limit 10").fetchall()]

    def all_messages(self) -> list:
        """
        Get all logs
        :return: list with all logs
        """
        logging.info("Get all logs and fetch result")
        return [(rec[0], rec[1], rec[2]) for rec in self.SQL.execute("select * from logs order by id").fetchall()]

    def clear_logs(self):
        """
        Clear logs
        """
        logging.info("Clearing logs")
        self.SQL.execute("delete from logs")
        self.DB.commit()
        self.SQL.execute("delete from sqlite_sequence where name='logs'")
        self.DB.commit()

    def __del__(self):
        logging.info("Close connection to Database")
        self.DB.close()


class LogsAPI(DB):

    def get_logs(self) -> json:
        """
        Get logs from DB
        """
        logging.info("API GET logs")
        result = {}
        logs = self.all_messages()
        for row in logs:
            id: str = str(row[0])
            timestamp: str = row[1]
            message: str = row[2]
            result[id] = {
                "timestamp": timestamp,
                "message": message
            }
        return json.dumps(result)

    def post_logs(self, logs):
        """
        Post logs to DB
        :param logs: json in format {"message": "text" | string value}
        """
        logging.info("API POST logs")
        logs = json.loads(logs)
        message = logs["message"]
        if len(message) > 0:
            self.insert_logs(message)
            return "Success", 200
        else:
            return "Bad request", 412

    def delete_logs(self):
        logging.info("Deleting all logs")
        self.clear_logs()
        return "Success", 200
