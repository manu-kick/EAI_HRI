# Master Api Module
This is the server that regulates the communication between the games, the database, Pepper robot and the user which interacts with the robot.
It is the main module of the project and it is responsible for the communication between the other modules.

It is a RESTful API that uses the Flask framework to handle the requests and responses.


## Installation
pip install -r requirements.txt

## Running
python3 app.py

## Endpoints
1. /api/identify_user (starting from an image, the server runs an algorithm and identifies the user in the database, if the user is not present, it creates a new user in the database and returns the user's profile)
2. /api/send_user_details

3. /api/get_game (the master knows which game to send to the user)
4. /api/elaborate_mental_model (elaborate the mental model of the user setting a difficulty level based on the user's profile)

5. /serve_game/{game_name} (serve the game to the user)
6. /api/{game_name}/ask_user_feedback (receive the feedback from the user and store it in the database)
7. api/{game_name}/emit_pepper_feedback (send the feedback to the Pepper robot)
8. /api/{game_name}/store_result (store the result of the game in the database)



