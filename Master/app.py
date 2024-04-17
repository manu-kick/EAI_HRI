from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

from User import User

import cv2
import dlib
import face_recognition
import json
import numpy as np

app = Flask(__name__)
# database connection details => https://freedb.tech/dashboard/index.php
# HOST: sql.freedb.tech
# PORT: 3306
# DATABASE NAME: freedb_hri_database

# USER: freedb_hri_user
# Password: b$4HB$P7#$J#Sr!

# Configure the MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://freedb_hri_user:b$4HB$P7#$J#Sr!@sql.freedb.tech/freedb_hri_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)


#Global variables accessible by all the functions
user = None


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

#write the SQL to alter the column game_id in the session table and call it state
# ALTER TABLE Sessions ADD COLUMN state VARCHAR(255) NOT NULL DEFAULT 'active';

#Drop the column game_id
# ALTER TABLE Sessions DROP COLUMN game_id;

#make the id column of the Sessions table the primary key and autoincrement
# ALTER TABLE Sessions MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY;

# remove user_id as foreign key
# ALTER TABLE Sessions DROP FOREIGN KEY Sessions_ibfk_1;

datFile =  "shape_predictor_68_face_landmarks.dat"

# Initialize dlib's face detector (HOG-based) and the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(datFile)

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
        
        
@app.route('/')
def hello_world():
    # Test connection to the database
    # Query all users
    all_users = UserModel.query.all()

    # # Query users based on a condition
    # specific_users = UserModel.query.filter_by(name='John').all()

    # # Query users based on multiple conditions
    # specific_users = UserModel.query.filter_by(name='John', surname='Doe').all()

    # # Query users based on a condition and retrieve only the first result
    # first_user = User.query.filter_by(name='John').first()

    # # Query users based on a condition and retrieve a single result or None if not found
    # single_user = User.query.filter_by(name='John').one_or_none()
    
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
    # Open the default camera (usually the webcam)
    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise Exception("Could not open video device!")

    # Capture frame-by-frame
    _, image = cap.read()

    # Display the captured frame
    # cv2.imshow('Webcam', frame)
    
    # Use a pre-computed image path
    #image_path = "faces/emanuele_1.jpg"
    #image = cv2.imread(image_path)

    # TODO Algorithm to identify the user --> Giancarlo
    # Call the inference of a model from a module (user identification) 
    #user_id = detect_user(image)
    
    det = Detector()
    inference = det.detect_user(image)

    inference = int(inference) # Fixes: Python type numpy.int64 cannot be converted

    # Create an example user profile
    user_id = inference + 1 # Because the user_id starts from 1
    user = UserModel.query.filter_by(id=user_id).first()
    user_features = user.user_features.decode('utf-8')
    user = User(user.name, user.surname, user.age, user_features, user.favorite_game, id = user_id) # TODO Make the user_id dynamic

    if user.favorite_game == 'tic_tac_toe':
        state_session = 0
    else:
        state_session = 20
        
    # create a session in the session table in the database (session_id, user_id, game_id)
    new_session = SessionModel(user_id=user.id, state=state_session)
    db.session.add(new_session)
    db.session.commit()

    return user.get_profile()

# def detect_user(image):
#     '''
#     Given an image, detect the user, Run the algorithm to identify the user
#     1. Extract features from the image
#     2. Take the features of all the users from the database
#     3. Compare the features of the image with the features of the users
#     4. Return the user_id of the user that matches the most with the image
#     5. If the user is not present, create a new user in the database and return the user_id
#     '''
#     # TODO
#     user_id = 0

#     return  user_id

# 3. /api/get_game (the master knows which game to send to the user)
@app.route('/api/get_game')
def get_game():
    return 'Get Game'

# 4. /api/elaborate_mental_model (elaborate the mental model of the user setting a difficulty level based on the user's profile)
@app.route('/api/elaborate_mental_model')
def elaborate_mental_model():
    return 'Elaborate Mental Model'

# 5. /serve_game/{game_name} (set in the current session in the database the game that the user is playing and serve the game to the user)
# @app.route('/serve_game/<game_name>')
# def serve_game(game_name):
#     assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"

#     # let's suppose we have for now the User Id of the current user
#     user_id = 0
#     # Get the profile of the user with user_id from the database

#     user = User('John', 'Doe', 25, "[1,2,3,4,5]", favorite_game  = 'tic_tac_toe', id = user_id)


#     #TODO Suppose here to send message to 
#     if game_name == 'tic_tac_toe':
#         # serve the html file in the /tictactoe/tictactoe.hmtl folder
#         return render_template('/tictactoe/tictactoe.html', user=user.get_profile())


#     else:
#         # serve the html file in the /semantic_ping_pong/semantic_ping_pong.html folder
#         return "Serve semantic ping pong game"
        

# 6. /api/{game_name}/ask_user_feedback (receive the feedback from the user and store it in the database)
@app.route('/api/<game_name>/ask_user_feedback')
def ask_user_feedback(game_name):
    '''
    Ask the user feedback in the game
    '''
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"


# 7. api/{game_name}/emit_pepper_feedback (send the feedback to the Pepper robot)
@app.route('/api/<game_name>/emit_pepper_feedback')
def emit_pepper_feedback(game_name):
    return 'Emit Pepper Feedback ' + game_name

# 8. /api/{game_name}/store_result (store the result of the game in the database)
# @app.route('/api/<game_name>/store_result',  methods=['POST'])
# def store_result(game_name):
#     # Get the Post data "type" and "user_id"
#     data = request.json
#     if game_name == 'tic_tac_toe':
#         type_ = data['type']
#         user_id = data['user_id']

#         # Store the result in the database in the table TicTacToe
#         new_result = TicTacToeModel(user_id=user_id, outcome=type_)
#         db.session.add(new_result)
#         db.session.commit()
#     else:
#         # TO implement the semantic ping pong
#         raise NotImplementedError

#     return {
#         'result': 'success'
#     }

if __name__ == '__main__':
    # Read the configuration file from JSON
    with open('../config.json') as json_file:
        config = json.load(json_file)

    app.run(host=config['master_ip'], debug=True, port=5002)
