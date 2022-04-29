import csv
import sys
from datetime import datetime
from flask import Flask, render_template
from dbdatareader import DBDataReader
from filedatareader import FileDataReader

from datareader import DataReader

app = Flask(__name__)
data_reader: DataReader

@app.route("/")
def dashboard():
    temps = read_last_data("temp", 10)
    co2s = read_last_data("co2", 10)
    humid = read_last_data("humid", 10)

    return render_template('dashboard.jinja', temp=temps, co2=co2s,humid=humid)

def read_last_data(data_type, n):
    return data_reader.read_latest_data(data_type, n)

def create_data_reader():
    global data_reader
    if sys.argv[1] == 'file':
        data_reader = FileDataReader(sys.argv[2])
    elif sys.argv[1] == 'db':
        data_reader = DBDataReader(sys.argv[2], sys.argv[3], sys.argv[4])

if __name__ == "__main__":
    if len(sys.argv) != 3 and len(sys.argv) != 5:
        print("Usage:")
        print("\tapp.py file <path to file>")
        print("\tapp.py db <db address> <db user> <db password>")
        exit()

    try:
        create_data_reader()

        app.run("0.0.0.0")
    except KeyboardInterrupt:
        if data_reader.hasattr("close"):
            data_reader.close()
