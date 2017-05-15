"""sync.py: Arduino to Rasp."""

import serial

if __name__ == "__main__":
    COM1 = serial.Serial('/dev/cu.usbmodem14321', 9600)

    COM1.write(str.encode('%d %d' % (1, 0)))

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

            # Query data and return to arduino

            isThereAnyRegistered = 1
            tryingToTurnOn = 0
            COM1.write(str.encode('%d %d' % (isThereAnyRegistered, tryingToTurnOn)))
