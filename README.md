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

To run `Flask application` just run this (it will run locally on port 5000)
```
(embedded_systems) $ python3 run.py
```
To start script you have do specify USB location of Arduino device. To find it you have to do this:
```
$ TODO!!!
```
After you can just start the script:
```
(embedded_systems) $ cd lights
(embedded_systems) $ python3 sync.py
```

## User creation
For user creation there is endpoint `create_user`. It accepts 3 parameters 
`name`, `mac` and `message`. `mas` has to be valid MAC address and both `name` and `mac` has to be unique.

This is curl example of user creation;
```
$ curl -X POST "http://0.0.0.0:5000/create_user?name=Pavel&mac=valid_mac&message=Test"
{
  "performed": true
}
```
## Getting room stats and turn on/off light
Endpoint `switch_lights` is for getting stats for room and remotely turning lights off and on.
To get room stats, you have to do just this:
```
$ curl  http://0.0.0.0:5000/switch_lights
{
  "luminosity": "-1", 
  "people_count": "-1", 
  "time": -1
}
```
If you want to turn off/on lights you have to define argument command. It can have two values `turn_on` or 
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