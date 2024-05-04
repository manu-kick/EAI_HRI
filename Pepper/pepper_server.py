from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import sys
import qi

from pepper_utils import PepperUtils

# Configure the MySQL connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://freedb_hri_user:b$4HB$P7#$J#Sr!@sql.freedb.tech/freedb_hri_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Initialize the database
db = SQLAlchemy(app)

# Global variables
memory_service = None
sonar_service = None
motion_service = None
dialog_service = None
leds_service = None
tts = None

# Class of the User object
class User:
    '''
        This is a local class that represents the User object, here can be implemented user-related methods
    '''
    def __init__(self, name, surname, age, features, favorite_game = "tic tac toe", id = None):

        self.id = id
        self.name = name
        self.surname = surname
        self.age = age
        self.favorite_game = favorite_game
        self.features = features

    def get_profile(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'age': self.age,
            'favorite_game': self.favorite_game,
            'features': self.features
        }

    def __str__(self):
        return self.name + ' ' + self.surname + ' (' + str(self.age) + ')'

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
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    state = db.Column(db.String(255))

#----------------------------------------------
#----------------------------------------------
#----------------------------------------------

@app.route('/')
def home():
    pepper_utils.talk_engine.say("Hello World!")
    pepper_utils.dance_engine.doHello()
    pepper_utils.dance_engine.resetPosture()
    return make_response()

@app.route("/api/say/<word>", methods=['GET'])
def say_word(word):
    pepper_utils.talk_engine.say(word)
    return make_response()

@app.route("/api/move/<movement>", methods=['GET'])
def move(movement):
    # Move the robot
    print("Trying to move the robot. Movement: " + movement)

    if movement == "win":
        pepper_utils.dance_engine.doPop()
    elif movement == "lose":
        pepper_utils.dance_engine.doLose()
    else:
        pepper_utils.dance_engine.doHello()

    print("Resetting posture...")
    pepper_utils.dance_engine.resetPosture()
    return make_response()

if __name__ == '__main__':
    # Read the configuration file from JSON
    with open('../config.json') as json_file:
        config = json.load(json_file)

    session = qi.Session()

    # Starting application
    try:
        session.connect("tcp://{}:{}".format(config['pepper_ip'], config['pepper_port']))
        print("Correctly connected to Pepper at " + config['pepper_ip'] + ":" + str(config['pepper_port']))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + config['pepper_ip'] + "\" on port " + str(config['pepper_port']) +".\n"
                "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    # Set the needed services
    memory_service = session.service("ALMemory")
    motion_service = session.service("ALMotion")
    sonar_service = session.service("ALSonar")
    dialog_service = session.service("ALDialog")
    posture_service = session.service("ALRobotPosture")
    tts = session.service("ALTextToSpeech")
    animation_service = session.service("ALAnimationPlayer")

    # Initialize the PepperUtils object
    pepper_utils = PepperUtils({
        'memory': memory_service,
        'motion': motion_service,
        'sonar': sonar_service,
        'dialog': dialog_service,
        'posture': posture_service,
        'animation': animation_service,
        'tts': tts,
        'config': config,
        'session': session
    })
    
    app.run(host=config['master_ip'], debug=True, port=5003)
