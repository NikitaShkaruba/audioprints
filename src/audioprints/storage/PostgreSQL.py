# coding=utf-8

import psycopg2

# Класс для взаимосвязи с базой данных
class PostgreSQL:
    config = {
        "dbname":   'nvdvmymy',
        "user":     'nvdvmymy',
        "password": 'C5m3hsj8f6BZ-3qxlzj1GJrL-EUI0-xb',
        "host":     'horton.elephantsql.com',
        "port":     '5432'
    }

    def __init__(self):
        pass

    @staticmethod
    def executeInsert(query):
        connection = psycopg2.connect(**PostgreSQL.config)

        cur = connection.cursor()
        cur.execute(query)
        result = cur.fetchone()
        connection.commit()
        connection.close()

        return result[0]

    @staticmethod
    def execute(query):
        connection = psycopg2.connect(**PostgreSQL.config)

        cur = connection.cursor()
        cur.execute(query)
        connection.commit()

        connection.close()

    @staticmethod
    def executeFetch(query):
        connection = psycopg2.connect(**PostgreSQL.config)

        cursor = connection.cursor()
        cursor.execute(query)

        rows = cursor.fetchall()
        connection.close()

        return rows
