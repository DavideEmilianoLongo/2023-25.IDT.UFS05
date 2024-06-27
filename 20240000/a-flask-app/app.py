from flask import Flask
import pymysql
import os
from pymysql import MySQLError


appWeb = Flask(__name__)
def initialize_database():
    try:
        # Connessione senza specificare il database, per permettere la creazione del database stesso
        connection = pymysql.connect(
            host="its-rizzoli-idt-mysql-53359.mysql.database.azure.com",
            user="psqladmin",
            passwd="H@Sh1CoR3!"
        )
        cursor = connection.cursor()

        # Leggere il contenuto del file SQL
        with open('script.sql', 'r') as file:
            sql_commands = file.read().split(';')

        # Eseguire ogni comando SQL
        for command in sql_commands:
            if command.strip():  # Ignora comandi vuoti
                cursor.execute(command)

        # Commit delle modifiche
        connection.commit()

        cursor.close()
        connection.close()
    except MySQLError as e:
        print(f"The error '{e}' occurred")

@appWeb.route("/")
def main():
    connection = None
    risposta = "nessuna risposta"
    try:
        connection = pymysql.connect(
            host="its-rizzoli-idt-mysql-53359.mysql.database.azure.com",
            user="psqladmin",
            passwd="H@Sh1CoR3!",
            database="ufs05db"
        )
        risposta = "Connection to MySQL DB successful"
        cursor = connection.cursor()

        query = ("SELECT first_name, last_name FROM employees")
        cursor.execute(query)

        for (first_name, last_name) in cursor:
            risposta = first_name
        cursor.close()
        connection.close()
    except MySQLError as e:
        risposta = f"The error '{e}' occurred"
    return risposta


if __name__ == "__main__":
        # Inizializza il database
    initialize_database()
    # https://learn.microsoft.com/en-us/azure/app-service/reference-app-settings
    # SERVER_PORT Read-only. The port the app should listen to.
    if "PORT" in os.environ:
        appWeb.run(host="0.0.0.0", port=os.environ['PORT'])
    else:
        appWeb.run(host="0.0.0.0")
