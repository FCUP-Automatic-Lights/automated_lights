"""sync.py: Arduino to Rasp."""

import serial
from utils import return_in_range_stations, try_unregister, try_register
import sqlite3

if __name__ == "__main__":
    # location of arduino in /dev
    COM1 = serial.Serial('', 9600)
    COM1.write(str.encode('%d %d' % (1, 0)))
    con = sqlite3.connect("../database.db")
    c = con.cursor()

    while True:
        line = COM1.readline().decode("utf-8").replace('\r\n', '')

        print(line)
        if line.startswith('PC'):
            infos = line.split('|')
            # Person Count on the room
            person_count = int(infos[0].strip().split(':')[1])
            # Lumens on the room
            lux = infos[1].strip().split(':')[1]
            # Gives info about time of light
            time = infos[2].strip().split(':')[1]

            # Do anything with data
            ret = c.execute("select people_count, time from stats where id = 0")
            previous_people_count, previous_time = ret.fetchone()
            
            # TODO: this needs refactor
            isThereAnyRegistered, in_range = return_in_range_stations(con)
            if len(in_range) == 0:
                c.execute('delete from users_inside')
            if previous_people_count > person_count:
                try_unregister(con)
            if previous_people_count < person_count or len(in_range) > 0:
                try_register(con)

            # update stats
            time = int(time) + previous_time
            c.execute("UPDATE stats set luminosity=?, people_count=?, time=? where id = 0",
                      (lux, person_count, time))
            
            # remotely switching lights
            c.execute("SELECT turn_on from turning where id = 0")
            tryingToTurnOn = c.fetchone()[0]
            # after we obtained data we will set status to zero
            if tryingToTurnOn != 0:
                c.execute("UPDATE turning set turn_on = 0 where id = 0")
                con.commit()

            COM1.write(str.encode('%d %d' % (isThereAnyRegistered, tryingToTurnOn)))
