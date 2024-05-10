# Pepper 

## Introduction
This repository contains the code for the Pepper robot. The code is written in Python and uses the NAOqi SDK to interact with the robot. The code is divided into different modules, each of which is responsible for a specific task.

The modules are:
- **Sonar Engine**: This module is responsible for retrieving values from Sonar Sensors.
- **Dance Engine**: This module is responsible for the dancing moves of Pepper.
- **Talk Engine**: This module is responsible for letting Pepper speak to the User.

Pepper needs Python 2.7.17 because NAOqi works with that specific version!

For proper use, you should start the Docker container from [this](https://bitbucket.org/iocchi/hri_software/src/master/docker/) page, then install also the requirements libraries from the requirements file.

You can also run this on Windows, simply install Choreographe 2.5.5.5 and download the necessary SDK (<i>pynaoqi-python2.7-2.5.7.1</i>) by adding it to the PATH.

## Running

### Main Loop
To run the main script, execute the following command in your terminal:

`python main.py`

This command activates the main loop of Pepper, waiting for Sonar input. Users should position themselves in front or behind Pepper.

### Sonar simulation
To simulate a Sonar input, use the sonar_sim.py script as follows:

`python sonar_sim.py --value VALUE --sensor SENSOR --duration DURATION`

Replace `VALUE` with the distance from the obstacle (e.g. 0.3), `SENSOR` with either `SonarFront` or `SonarBack` and `DURATION` with a duration of the input (e.g. if you want to stay for a long time, put 600 which are 10 minutes).

Whenever you want to move away from Pepper, simply set `VALUE` to 0.0 or a value greater than `sonar_threshold` in `config.json`.

<i> Maintained by Gianmarco Scarano </i>