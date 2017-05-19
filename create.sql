CREATE TABLE users (mac TEXT UNIQUE, name TEXT UNIQUE, message TEXT);
CREATE TABLE stats (luminosity TEXT, people_count TEXT, time INT, last_status INT, id INT PRIMARY KEY);
CREATE TABLE turning (turn_on INT, id INT);
CREATE TABLE users_inside(mac TEXT UNIQUE NOT NULL PRIMARY KEY);
CREATE TABLE show_message (show INT, mac TEXT, seconds INT, id INT);

INSERT INTO stats(luminosity, people_count, time, last_status, id) VALUES (-1,-1,-1,-1,0);
INSERT INTO turning(turn_on, id) VALUES (0, 0);
INSERT INTO show_message(show, mac, seconds, id) VALUES ('no', 'no', '0', 0);
