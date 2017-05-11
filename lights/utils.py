import subprocess
import re
import sqlite3

SIGNAL_THRESHOLD = 70
COMMAND = ['iw', 'dev', 'wlan0', 'station', 'dump']
p = re.compile(r'([0-9a-f]{2}(?::[0-9a-f]{2}){5})', re.IGNORECASE)


class ClientInfo(object):
    mac = ""
    signal = 0


def filter_stations():
    #output = subprocess.check_output(COMMAND, universal_newlines=True).splitlines(True)
    output = ['Station address (on wlan0)\n', '\tinactive time:\t20 ms\n', '\trx bytes:\t136887\n',
              '\trx packets:\t1496\n', '\ttx bytes:\t90877\n', '\ttx packets:\t471\n', '\ttx retries:\t0\n',
              '\ttx failed:\t0\n', '\tsignal:  \t-41 [-41] dBm\n', '\tsignal avg:\t-40 [-40] dBm\n',
              '\ttx bitrate:\t72.2 MBit/s MCS 7 short GI\n', '\trx bitrate:\t72.2 MBit/s MCS 7 short GI\n',
              '\tauthorized:\tyes\n', '\tauthenticated:\tyes\n', '\tpreamble:\tshort\n', '\tWMM/WME:\tyes\n',
              '\tMFP:\t\tno\n', '\tTDLS peer:\tno\n', 'Station address2 (on wlan0)\n',
              '\tinactive time:\t296330 ms\n', '\trx bytes:\t3622\n', '\trx packets:\t33\n', '\ttx bytes:\t5429\n',
              '\ttx packets:\t35\n', '\ttx retries:\t0\n', '\ttx failed:\t0\n', '\tsignal:  \t-57 [-57] dBm\n',
              '\tsignal avg:\t-57 [-57] dBm\n', '\ttx bitrate:\t54.0 MBit/s\n', '\trx bitrate:\t48.0 MBit/s\n',
              '\tauthorized:\tyes\n', '\tauthenticated:\tyes\n', '\tpreamble:\tshort\n', '\tWMM/WME:\tyes\n',
              '\tMFP:\t\tno\n', '\tTDLS peer:\tno\n']

    client_infos = []
    c = None
    for l in output:
        if "Station" in l:
            if c is not None: client_infos.append(c)
            c = ClientInfo()
            c.mac = re.findall(p, l)
        if "signal:" in l: c.signal = int(l.split()[1])

    whitelisted = get_whitelisted_macs()
    for c in client_infos:
        if c.mac in whitelisted and c.signal <= SIGNAL_THRESHOLD:
            return True
    return False


def create_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE users (mac TEXT, name TEXT, message TEXT)')
    c.execute('CREATE TABLE stats (luminosity TEXT, people_count TEXT, just_entered TEXT)')
    conn.close()


def get_whitelisted_macs():
    conn = sqlite3.connect('database.db')
    conn.row_factory = lambda cursor, row: row[0]
    c = conn.cursor()
    c.execute('SELECT mac FROM users')
    return c.fetchall()
