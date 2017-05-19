from flask import request, render_template
from flask.ext.api import FlaskAPI
from flask import jsonify

from lights.utils import *

app = FlaskAPI(__name__)


# endpoint is responsible for turning on/off lights and by default returns stats
@app.route('/switch_lights', methods=['GET', 'POST'])
def switch_lights():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    if request.method == 'POST':
        command = request.args.get("command")
        if command != "turn_on" and command != "turn_off":
            return jsonify({
                'error': 'performing bad query'
            }), status.HTTP_404_NOT_FOUND
        try:
            if command == "turn_on":
                cur.execute("UPDATE turning SET turn_on=? WHERE id = 0", (1,))
            else:
                cur.execute("UPDATE turning SET turn_on=? WHERE id = 0", (2,))
            con.commit()
        except:
            con.rollback()
            return jsonify({
                'error': 'error occurred during inserting into database'
            }), status.HTTP_404_NOT_FOUND

    data = cur.execute('SELECT luminosity, people_count, time FROM stats WHERE id = 0')
    lum, people_count, time = data.fetchone()
    con.close()
    return jsonify({
        'luminosity': lum,
        'people_count': people_count,
        'time': time
    })


# endpoint creates new user
@app.route('/create_user', methods=['POST'])
def new_user():
    if request.method == 'POST':
        nm = request.args.get("name")
        mac = request.args.get("mac")
        # validate given arguments
        if nm is None or mac is None:
            return jsonify({
                'performed': False,
                'error': 'one of arguments is not defined'
            })
        if len(re.findall(p, mac)) == 0:
            return jsonify({
                'performed': False,
                'error': 'given mac is not valid'
            }), status.HTTP_404_NOT_FOUND

        con = None
        try:
            con = sqlite3.connect("database.db")
            cur = con.cursor()

            cur.execute("INSERT INTO users (name,mac) VALUES(?, ?)", (nm, mac))
            con.commit()
        except:
            con.rollback()
            return jsonify({
                'performed': False,
                'error': 'error occurred during inserting into database'
            }), status.HTTP_404_NOT_FOUND
        finally:
            con.close()

        return jsonify({
            'performed': True
        })


# TODO check database here and if there is a change render change
@app.route("/message")
def show_message():
    con = None
    try:
        con = sqlite3.connect("database.db")
        cur = con.cursor()

        cur.execute("SELECT show FROM show_message")
        if cur.fetchone()[0] == 'yes':
            cur.execute("SELECT seconds, name, message "
                        "FROM show_message LEFT JOIN users ON show_message.mac = users.mac")
            remaining_time, user, message = cur.fetchone()
            remaining_time = int(remaining_time) - 1
            if remaining_time == 0:
                cur.execute("UPDATE show_message SET seconds=?, show=? WHERE id = 0", (remaining_time, 'no'))
            else:
                cur.execute("UPDATE show_message SET seconds=?", (remaining_time,))
            con.commit()
            return render_template('message.html', user=user)
        else:
            return render_template('message.html')
        con.rollback()
        return jsonify({
            'performed': False,
            'error': 'error occurred during inserting into database'
        }), status.HTTP_404_NOT_FOUND
    finally:
        con.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
