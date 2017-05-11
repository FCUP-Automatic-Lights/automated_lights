from flask import request, render_template
from flask.ext.api import FlaskAPI
from flask import jsonify

from lights.utils import *

app = FlaskAPI(__name__)


@app.route("/clients", methods=['GET'])
def get_connected():
    return jsonify({
        'clients_in_range': filter_stations()
    })


@app.route('/enternew')
def new_student():
    return render_template('user.html')


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            mac = request.form['mac']
            message = request.form['message']

            with sqlite3.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO users (name,mac,message) VALUES(?, ?, ?)", (nm, mac, message))
                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list_users():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


@app.route("/message")
def show_message():
    return render_template('message.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
