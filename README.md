# EAI_HRI
Elective in AI, Human Robot Interaction Module by Prof. Iocchi, Rucci Emanuele, Gianmarco Scarano, Giancarlo Tedesco

This repo contains the implementation of the different modules of the project:
- Master Api Module
    - User Recognition Module
    - Game Service Module
    - Mental Model Module
    - Database Service Module
- Pepper Module

## Configurations
There is a configuration file named `config.json` where you can set various parameters such as:
- Master IP
- Pepper IP
- Pepper port
- Sonar Distance Threshold

> **NOTES:**
>
> **_Master IP:_** Default: `127.0.0.1`. Change this only if you host Pepper on WSL, otherwise leave it as it is.<br>
> **_Pepper port:_** The one indicated in Choreographe.

## States
0 - New session, just arrived a user in front of the robot, the robot has to ask the user if he wants to play to the favorite game
1 