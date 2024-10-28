# ApulianPepper
Project for the course Elective in AI, Human Robot Interaction Module held by Prof. Iocchi, University of Rome "La Sapienza"

<i>Developed by Emanuele Rucci, Gianmarco Scarano & Giancarlo Tedesco</i>

---------------------
## Instructions (Windows & Linux)

1. Start Choregraphe

2. API Server | Master, Tablet & Pepper (From Miniconda):
   1. `cd Master && python app.py`
   2. `cd Tablet && python app.py`
   3. `conda activate pepper && cd Pepper && python pepper_server.py`

5. Now, open another PowerShell (or Bash) and run the scripts:
   1. `conda activate pepper && cd Pepper && python main.py`
   2. `conda activate pepper && cd Pepper && python sonar_sim.py --value 0.3 --sensor SonarFront --duration 600`

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
