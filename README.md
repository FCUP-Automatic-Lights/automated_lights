# Automated Lights
School project for Embedded systems class
## Initial Setup
You should run this application in virtual environment. 
Use these commands to do so:
```
$ virtualenv -p python3 embedded_systems --system-site-package 
$ source embedded_systems/bin/activate 
(embedded_systems) $ pip3 install -r requirements.txt
```
After this your prompt should start with `(embedded_systems)` like in example.

## Application description
There are two pieces to run, `Flask application` and script which communicates with Arduino device.
Before running application itself you have to initialize database quick is done this way:
````
$ sqlite3 database.db
sqlite> .read create.sql
````

To run `Flask application` just run this (it will run locally on port 5000)
```
(embedded_systems) $ python3 run.py
```
To start script you have do specify USB location of Arduino device. To find you check out here for more information:
 https://github.com/FCUP-Automatic-Lights/arduino-backend .

After you can just start the script:
```
(embedded_systems) $ cd lights
(embedded_systems) $ python3 sync.py
```

## User creation
For user creation there is endpoint `create_user`. It accepts 3 parameters 
`name`, `mac` and `message`. `mac` has to be valid MAC address and both `name` and `mac` has to be unique.

User creation is performed through post to endpoint and here you can see example and response through `curl`:
```
$ curl -X POST "http://0.0.0.0:5000/create_user?name=Pavel&mac=valid_mac&message=Test"
{
  "performed": true
}
```

## Getting room stats and turn on/off light
Endpoint `switch_lights` is for getting stats for room and remotely turning lights off and on.
This one is has two purposes: You can either get room information or try to turn on/off lights.
To get information you have to do the simple get:
```
$ curl http://0.0.0.0:5000/switch_lights
{
  "luminosity": "-1", 
  "people_count": "-1", 
  "time": -1
}
```
However if you want to turn off/on lights you have to define argument command. It can have two values `turn_on` or 
`turn_off`. You should check whether for `luminosity`, because if room is too bright you can't turn on lights.
You should also check `people_count` since you can't turn off light if there are people in room.
Example for turning on lights:
```
$ curl -X POST http://0.0.0.0:5000/switch_lights?\command=turn_on
{
  "luminosity": "-1", 
  "people_count": "-1", 
  "time": -1
}
```

## Application description
When registered user enters the room welcome messages are shown through html page which is located in 
endpoint `message`. All you have to do is open web browser:
```
$ browser http://0.0.0.0:5000/message
```

This page is refreshed every second to get latest information. 
Welcome message is shown for every user for 10 seconds if there is no user entering after him.