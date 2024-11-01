from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

from User import User

import cv2
import face_recognition
import json
import numpy as np

# ========================
# database connection details => https://freedb.tech/dashboard/index.php
# HOST: sql.freedb.tech
# PORT: 3306
# DATABASE NAME: freedb_hri_database
# ========================
# USER: freedb_hri_user
# Password: b$4HB$P7#$J#Sr!
# ========================

# Configure the MySQL connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://freedb_hri_user:b$4HB$P7#$J#Sr!@sql.freedb.tech/freedb_hri_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

# Models for the database
class UserModel(db.Model):
    # set the name of the table in the database
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    age = db.Column(db.Integer)
    favorite_game = db.Column(db.String(255))
    user_features = db.Column(db.BLOB)

class TicTacToeModel(db.Model):
    __tablename__ = 'TicTacToe'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    outcome = db.Column(db.String(1)) #X, O, D (Draw)

class SessionModel(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    state = db.Column(db.String(255))

class Detector:
    def __init__(self, ):
        
        self.tolerance = 0.5    # Similarity threshold
        self.users_features = self.load_known_encodings()
        #get the shape of the features
        self.shape = self.users_features[0].shape
        print("Users features loaded : ", self.users_features.shape)

    def load_known_encodings(self):
        all_users = UserModel.query.all()
        # users = []
        users_features = []
        for user in all_users:
            # the field user.user_features is a binary large object (BLOB) that needs to be converted to a string
            features = user.user_features.decode('utf-8')
           
            # remove the \n and the spaces and convert the string to a numpy array
            features = np.array(features.replace('\n', '').replace(' ', '').replace('[', '').replace(']', '').split(','), dtype=np.float32)
            users_features.append(features)

            # users.append(User(user.name, user.surname, user.age, features, user.favorite_game).get_profile())
        # Convert the list of features to a numpy array (matrix)
        users_features = np.array(users_features)
        
        return users_features

    #     '''
    #     Given an image, detect the user, Run the algorithm to identify the user
    #     1. Extract features from the image
    #     2. Take the features of all the users from the database
    #     3. Compare the features of the image with the features of the users
    #     4. Return the user_id of the user that matches the most with the image
    #     5. If the user is not present, create a new user in the database and return the user_id
    #     '''
    def detect_user(self, image):
        '''
        image: image of the user 
        '''
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        result = -1
        
        for face_encoding in face_encodings:
            distances = face_recognition.face_distance(self.users_features, face_encoding)
            best_match_index = distances.argmin()
            
            if distances[best_match_index] < self.tolerance:
                # Return the index of the user_id of the best match
                result = best_match_index
                # return result
            
        return result

def calculate_win_loss_ratio(user_id):
    with app.app_context():  # Context for database access
        wins = db.session.query(TicTacToeModel).filter_by(user_id=user_id, outcome='X').count()  # Assuming 'X' indicates a win

        losses = db.session.query(TicTacToeModel).filter_by(user_id=user_id, outcome='O').count()  # Assuming 'O' indicates a loss

        total_games = wins + losses 

        if total_games == 0:
            return 0.5  # Default ratio if no games played yet
        else:
            return wins / total_games
        
def calculate_difficulty(user_id):
    with app.app_context():  # Context for database access
        user = UserModel.query.get(user_id)
        user_age = user.age
        win_loss_ratio = calculate_win_loss_ratio(user_id)
        
        # YOUR MENTAL MODEL FORMULA HERE
        difficulty_metric = user_age * (1 - win_loss_ratio)
        easy_threshold = 25

        # Threshold determination
        if difficulty_metric <= easy_threshold:
            difficulty_level = 0
        else:
            difficulty_level = 1

        return difficulty_level

def initialize_webcam() -> cv2.VideoCapture:
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise Exception("Could not open video device!")
    else:
        print("Webcam ready")
        return cap

# Global variables accessible by all the functions
user = None

# Initialize the webcam
cap = initialize_webcam()

@app.route('/')
def hello_world():
    # Test connection to the database
    # Query all users
    all_users = UserModel.query.all()
    
    # Return the all_users as a json object
    users = []
    for user in all_users:
        # the field user.user_features is a binary large object (BLOB) that needs to be converted to a string
        features = user.user_features.decode('utf-8')

        users.append(User(user.name, user.surname, user.age, features, user.favorite_game).get_profile())
    
    # Take the array of users and return it as a json object
    return {'users': users}

# 1. /api/identify_user (starting from an image, the server runs an algorithm and identifies the user in the database, if the user is not present, it creates a new user in the database and returns the user's profile)
@app.route('/api/identify_user', methods=['GET', 'POST'])
def identify_user():
    '''
    Given an image, run the algorithm to identify the user
    and return the user's profile
    '''
    # Variables
    tries = 0   # Number of tries to identify the user
    global cap  # Webcam capture

    # Initialize the detector
    det = Detector()

    if cap is None:
        cap = initialize_webcam()

    while tries < 3:
        # Capture frame-by-frame
        _, image = cap.read()
        
        # # Use a pre-computed image path
        # image_path = "faces/gianmarco_1.jpg"
        # image = cv2.imread(image_path)

        # Algorithm to identify the user
        print("Trying to identify the user... Attempt: ", tries + 1)
        inference = int(det.detect_user(image))

        if (inference == -1):
            print("User not found... Please try again!")
            tries += 1
        else:
            # Create an example user profile
            user_id = inference + 1 # Because the user_id starts from 1
            user = UserModel.query.filter_by(id=user_id).first()
            user_features = user.user_features.decode('utf-8')
            user = User(user.name, user.surname, user.age, user_features, user.favorite_game, id = user_id)

            if user.favorite_game == 'Tic Tac Toe':
                state_session = 0
            else:
                state_session = 20
                
            # create a session in the session table in the database (session_id, user_id, game_id)
            new_session = SessionModel(user_id=user.id, state=state_session)
            db.session.add(new_session)
            db.session.commit()
            break

    # Release the camera
    cap.release()

    if tries == 3:
        return "User not found in Database. Exiting..."
    else:
        return render_template('/identify_user.html', user=user.get_profile())

# 2. /api/get_game (the master knows which game to send to the user)
@app.route('/api/get_game')
def get_game():
    return 'Get Game'

# 3. /api/elaborate_mental_model (elaborate the mental model of the user setting a difficulty level based on the user's profile)
@app.route('/api/elaborate_mental_model')
def elaborate_mental_model():
    # Retrieve the last user session
    last_session = SessionModel.query.order_by(SessionModel.id.desc()).first()

    difficulty_level = calculate_difficulty(last_session.user_id)
    return {'difficulty': difficulty_level}

# 4. /api/{game_name}/ask_user_feedback (receive the feedback from the user and store it in the database)
@app.route('/api/<game_name>/ask_user_feedback')
def ask_user_feedback(game_name):
    '''
    Ask the user feedback in the game
    '''
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"

# 5. api/{game_name}/emit_pepper_feedback (send the feedback to the Pepper robot)
@app.route('/api/<game_name>/emit_pepper_feedback')
def emit_pepper_feedback(game_name):
    return 'Emit Pepper Feedback ' + game_name

if __name__ == '__main__':
    # Read the configuration file from JSON
    with open('../config.json') as json_file:
        config = json.load(json_file)

    app.run(host=config['master_ip'], debug=True, port=5002)
