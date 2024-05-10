# ApulianPepper
Project for the course Elective in AI, Human Robot Interaction Module held by Prof. Iocchi, University of Rome "La Sapienza"

<i>Developed by Emanuele Rucci, Gianmarco Scarano & Giancarlo Tedesco</i>

---------------------

## Modules
This repo contains the implementation of 3 different modules of the project:
- Master API Module
    - User Recognition Module
    - Game Service Module
    - Mental Model Module
    - Database Service Module

- Tablet API Module
    - Rendering Module

- Pepper API Module
    - Sonar Engine
    - Dance Engine
    - Talk Engine

## Configuration
There is a configuration file named `config.json` where you can set various parameters such as:
- Master IP (<i>Default: `127.0.0.1`</i>)
- Pepper IP (<i>Default: `127.0.0.1`</i>)
- Pepper port (<i>The one indicated in Choreographe</i>)
- Sonar Distance Threshold (<i>Default: `0.5`</i>)

## States
Whenever the User interacts with Pepper, a new session is started.
The sessions have different values, such as:
