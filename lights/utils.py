import subprocess
import re
import sqlite3

SIGNAL_THRESHOLD = -70
COMMAND = ['iw', 'dev', 'wlan0', 'station', 'dump']
p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)


# simple data structure which holds client info
class ClientInfo(object):
    def __init__(self):
        self.mac = None 
        self.signal = SIGNAL_THRESHOLD


# calls command which monitors connected devices and parses mac address with signal
def parse_in_range():
    output = subprocess.check_output(COMMAND, universal_newlines=True).splitlines(True)
    client_info = []
    c = None
    for l in output:
        if "Station" in l:
            c = ClientInfo()
            c.mac = re.findall(p, l)[0]
        if "signal:" in l:
             c.signal = int(l.split()[1])
             client_info.append(c)
    return client_info


# gets all devices and range and checks whether there is whitelisted user in range
def filter_stations(conn):
    clients = parse_in_range()
    possible = list(get_whitelisted_macs(conn) - get_users_inside(conn))
    in_range = []
    for c in clients:
        if c.mac in possible and c.signal >= SIGNAL_THRESHOLD:
            in_range.append(c)

    return in_range


def return_in_range_stations(conn):
    clients = parse_in_range()
    whitelisted = get_whitelisted_macs(conn)
    in_range = []
    for c in clients:
        if c.mac in whitelisted and c.signal >= SIGNAL_THRESHOLD:
            in_range.append(c)

    if not in_range:
        return 0, []
    return 1, in_range


# checks whether all conditions are met to unregistered user from system
def try_unregister(conn):
    c = conn.cursor()
    clients = parse_in_range()
    inside = get_users_inside(conn)

    # if some user deactivates wifi, or something malfunctions want to remove
    instant_delete = set(inside) - set(clients)
    for i in instant_delete:
        c.execute("DELETE FROM users_inside WHERE mac=?", (mac,))

    # iterate trough users which were inside and kick one which is out from range
    for mac in inside:
        for c in clients:
            if mac == c.mac and c.signal > SIGNAL_THRESHOLD:
                # delete user from db
                c.execute("DELETE FROM users_inside WHERE mac=?", (mac,))
                conn.commit()
                return True
    return False


# tries to register user to room if conditions are met
def try_register(conn):
    clients = filter_stations(conn)
    strongest_signal = ClientInfo()
    for client in clients:
        if client.signal > strongest_signal.signal:
            strongest_signal = client

    if strongest_signal.mac == None:
        return None

    c = conn.cursor()
    c.execute("INSERT INTO users_inside (mac) VALUES(?)", (strongest_signal.mac,))
    c.execute("UPDATE show_message set mac=?, seconds = 10, show = 'yes' WHERE id = 0", (strongest_signal.mac,))
    conn.commit()


# get users which are registerd inside a room
def get_users_inside(conn):
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    c.execute("SELECT mac FROM users_inside")
    return set(c.fetchall())


# get whitelisted users from database
def get_whitelisted_macs(conn):
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    c.execute('SELECT mac FROM users')
    return set(c.fetchall())
