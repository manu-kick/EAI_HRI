# Pepper 

## Introduction
This repository contains the code for the Pepper robot. The code is written in Python and uses the NAOqi SDK to interact with the robot. The code is divided into different modules, each of which is responsible for a specific task.

The modules are:
- **Sonar Detector**: This module is responsible for retrieving values from Sonar Sensors.
- X
- X

Pepper needs Python 2.7.17 because NAOqi works with that specific version!

For proper use, you should start the Docker container from [this](https://bitbucket.org/iocchi/hri_software/src/master/docker/) page, instead of installing a requirements file.

## Running

### Main Loop
To run the main script, execute the following command in your terminal:

`python main.py`

This command activates the main loop of Pepper, waiting for Sonar input. Users should position themselves in front or behind Pepper.

### Sonar simulation
To simulate a Sonar input, use the sonar_sim.py script (located in the pepper_tools directory in the Docker container) as follows:

`python sonar_sim.py --pport PORT --value VALUE --sensor SENSOR`

Replace `PORT` with the port number, `VALUE` with the distance from the obstacle (e.g. 0.3), and `SENSOR` with either `SonarFront` or `SonarBack`.

<i> Maintained by Gianmarco Scarano </i>