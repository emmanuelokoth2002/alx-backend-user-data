#!/usr/bin/env python3
'''
Handling Personal Data: This script deals with logging and personal data handling.
'''
import re
from typing import List
import logging
from os import getenv
import mysql.connector

# Define Personally Identifiable Information (PII) fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    ''' Obfuscates specific fields in the log message '''
    for field in fields:
        # Using regex to substitute the specified field values with the redaction string
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for redacting PII in log messages
    """
    # Redaction placeholder
    REDACTION = "***"
    # Log message format
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    # Separator for log messages
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' Filters sensitive values using filter_datum method '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    ''' Creates and configures a logger object '''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' Connects to a secure database '''
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    user = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db = getenv('PERSONAL_DATA_DB_NAME')
    cur = mysql.connector.connect(host=host, user=user, password=password,
                                  database=db)
    return cur


def main():
    ''' Read and filter data '''
    # Connect to the database
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users;')
    # Fetch column names from the database
    field_names = [i[0] for i in cursor.description]
    logger = get_logger()
    for row in cursor:
        # Prepare a log message for each row in the database
        message = ''.join('{}={}; '.format(k, v) for k, v in zip(field_names, row))
        # Log the obfuscated message
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()
