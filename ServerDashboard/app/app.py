import sys
from flask import Flask, render_template, request
from flask_cors import CORS
from dbdatareader import DBDataReader
from filedatareader import FileDataReader

from datareader import DataReader

app = Flask(__name__)
CORS(app)

data_reader: DataReader

def ac1():
    print("Doing action 1")

def ac2():
    print("Doing action 2")

ACTIONS = [
    ("Button 1", "action1", ac1),
    ("Button 2", "action2", ac2)
]



@app.route("/")
def dashboard():
    temps = read_last_data("temp", 10)
    co2s = read_last_data("co2", 10)
    humid = read_last_data("humid", 10)

    return render_template('dashboard.jinja', temp=temps, co2=co2s,humid=humid, actions=ACTIONS)

@app.route("/doAction")
def doAction():
    action = request.args.get('action')
    list(filter(lambda x: x[1]==action, ACTIONS))[0][2]()
    return ""

@app.route("/data")
def data():
    data_type = request.args.get('dataType')
    res = {
        "data": read_last_data(data_type, 10) 
    }
    return res

def read_last_data(data_type, n):
    return data_reader.read_latest_data(data_type, n)

def create_data_reader():
    global data_reader
    if sys.argv[1] == 'file':
        data_reader = FileDataReader(sys.argv[2])
    elif sys.argv[1] == 'db':
        data_reader = DBDataReader(sys.argv[2], sys.argv[3], sys.argv[4])
        data_reader.connect()

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
