"""sync.py: Arduino to Rasp."""

import serial
from .utils import filter_stations, try_unregister, try_register
import sqlite3

if __name__ == "__main__":
    COM1 = serial.Serial('/dev/cu.usbmodem14321', 9600)

    COM1.write(str.encode('%d %d' % (1, 0)))
    con = sqlite3.connect("database.db")
    c = con.cursor()

    while True:
        line = COM1.readline().decode("utf-8").replace('\r\n', '')

        # ROOM
        if line.startswith('PC'):
            infos = line.split('|')
            # Person Count on the room
            person_count = infos[0].strip().split(':')[1]
            # Lumens on the room
            lux = infos[1].strip().split(':')[1]
            # Gives info about time of light
            time = infos[2].strip().split(':')[1]
            # Info about status about last request:
            # 1 -> Success;
            # 0 -> Failure;
            # -1 -> No Request
            last_status = infos[3].strip().split(':')[1]

            # Do anything with data
            ret = c.execute("select people_count from stats where id = 0")
            previous_people_count = int(ret.fetchone()[0])
            if previous_people_count > person_count:
                try_unregister(con)
            if previous_people_count < person_count:
                try_register(con)

            # update stats
            c.execute("UPDATE stats set luminosity=?, people_count=?, time=?, last_status=? where id = 0",
                      (lux, person_count, time, last_status))
            con.commit()

            # Query data and return to arduino

            # is in range, is not registered, is whitelisted
            isThereAnyRegistered, in_range = filter_stations(con)
            c.execute("SELECT turn_on, turn_off from turning where id = 0")
            tryingToTurnOn, tryingToTurnOff = c.fetchone()

            COM1.write(str.encode('%d %d %d' % (isThereAnyRegistered, tryingToTurnOn, tryingToTurnOff)))
