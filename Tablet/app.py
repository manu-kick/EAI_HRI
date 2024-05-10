from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy

import os
import gensim
import gensim.downloader as api
import random
import json
import requests

# ==========================================
# Configure the MySQL connection
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://freedb_hri_user:b$4HB$P7#$J#Sr!@sql.freedb.tech/freedb_hri_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
wv = None
# ==========================================

# Class of the User object
class User:
    '''
        This is a local class that represents the User object, here can be implemented user-related methods
    '''
    def __init__(self, name, surname, age, features, favorite_game = "Tic Tac Toe", id = None):

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

class SemanticPingPong(db.Model):
    __tablename__ = 'SemanticPingPong'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    outcome = db.Column(db.String(1)) #X, O

class SessionModel(db.Model):
    __tablename__ = 'Sessions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    state = db.Column(db.String(255))

# ==========================================

# 0. / (home page)
@app.route('/')
def home():
    return render_template('index.html')

# 1. /api/get-session (get the current session from the database)
@app.route('/api/get-session')
def get_sessions():
    # Query all sessions
    all_sessions = SessionModel.query.all()

    # Return the last session
    return_session = all_sessions[-1]
    return {
        'id': return_session.id,
        'user_id': return_session.user_id,
        'state': return_session.state
    }

# 2. /api/change_favorite_game/{user_id} (change the favorite game of the user in the database)
@app.post("/api/change_favorite_game/<user_id>")
def change_favorite_game(user_id):
    # Get the user from the user_id
    user = UserModel.query.filter_by(id=user_id).first()
    user_ = user

    # If the user has the favorite game tic tac toe, change it to semantic ping pong
    if user_.favorite_game == 'Tic Tac Toe':
        user_.favorite_game = 'Semantic Ping Pong'
    else:
        user_.favorite_game = 'Tic Tac Toe'

    # Update the user in the database
    user = UserModel.query.filter_by(id=user_id).first()
    user.favorite_game = user_.favorite_game
    db.session.commit()

    return user.favorite_game

# 3. /api/get-favorite-game/{user_id} (get the user favorite game from the database)
@app.get("/api/get-favorite-game/<user_id>")
def get_favorite_game(user_id):
    # Query the user with the id 0
    user = UserModel.query.filter_by(id=user_id).first()
    return {
        'favorite_game': user.favorite_game
    }

# 5. /serve_game/{game_name} (set in the current session in the database the game that the user is playing and serve the game to the user)
@app.route('/serve_game/<game_name>/<user_id>')
def serve_game(game_name, user_id):
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"
    # Get the profile of the user with user_id from the database
    user = UserModel.query.filter_by(id=user_id).first()
    user = User(user.name, user.surname, user.age, user.user_features, user.favorite_game, id = user_id)

    if game_name == 'tic_tac_toe':
        # serve the html file in the /tictactoe/tictactoe.hmtl folder
        return render_template('/tictactoe.html', user=user.get_profile())
    else:
        # serve the html file in the /semantic_ping_pong/semantic_ping_pong.html folder
        return render_template('/semanticpingpong.html', user=user.get_profile())

# 6. /api/{game_name}/store_result (store the result of the game in the database)
@app.route('/api/<game_name>/store_result',  methods=['POST'])
def store_result(game_name):
    # Get the Post data "type" and "user_id"
    data = request.json
    type_ = data['type']
    user_id = data['user_id']

    if game_name == 'tic_tac_toe':
        # Store the result in the database in the table TicTacToe
        new_result = TicTacToeModel(user_id=user_id, outcome=type_)
    else:
        # Store the result in the database in the table SemanticPingPong
        new_result = SemanticPingPong(user_id=user_id, outcome=type_)

    db.session.add(new_result)
    db.session.commit()

    return {
        'result': 'success'
    }

# 7. /api/get_initial_word (get the initial word for the semantic ping pong game)
@app.route("/api/get_initial_word", methods=['GET'])
def get_intial_word():
    # This function return the initial word for the semantic ping pong game
    # It is a random word from a list of words

    # Read the words from the txt file
    with open('english-common-words.txt') as f:
        words = f.readlines()

    words = [x.strip() for x in words]
    
    return  words[random.randint(0, len(words)-1)]

# 8. /api/get_word_points/{previous_word}/{current_word} (get the similarity between the previous word and the current word)
@app.route("/api/get_word_points/<previous_word>/<current_word>", methods=['POST'])
def get_word_points(previous_word, current_word):
    # cosine similarity 
    similarity = wv.similarity(previous_word, current_word)
    
    # make the similarity a number float then return as a string
    return str(float(similarity))

# 9. /api/emit_word/{word} (emit a word to the user)
@app.route("/api/emit_word/<word>", methods=['POST'])
def pepper_emit_word(word):
    # get 10 most similar words to the word
    similar_words = wv.most_similar(word, topn=20)

    # http call to endpoint /api/elaborate_mental_model with 5002 port
    # get the mental model of the user
    mental_difficulty = requests.get('http://localhost:5002/api/elaborate_mental_model').json()['difficulty']
    
    # Given the mental model of the user, the robot can choose the word to say (1 is expert than will return the most similar word)
    # The robot can choose the word to say
    if mental_difficulty == 1:
        word_to_say = similar_words[5][0]
    else:
        word_to_say = similar_words[12][0]

    print("From similar words: ", similar_words)
    print("Word to say: ", word_to_say)
    
    return word_to_say

# SIMULATE THIS (THE FOLLOWING CODE) has to be placed in the pepper server
@app.route("/api/change_session_status", methods=['POST'])
def change_session_status():
    data = request.json
    # Take the last session using the user_id
    session = SessionModel.query.filter_by(user_id=data['user_id']).first()
    print(session.id)

    # Update the session status
    session.state = data['status']
    db.session.commit()

    return {
        'result': 'success'
    }

if __name__ == '__main__':
    # Read the configuration file from JSON
    with open('../config.json') as json_file:
        config = json.load(json_file)
    
    # # To be run only once to download the word2vec model.
    if(os.path.exists('word2vec.gen')):
        wv = gensim.models.KeyedVectors.load('word2vec.gen')
    else:
        wv = api.load('word2vec-google-news-300')
        wv.save(F'word2vec.gen')

    app.run(host=config['master_ip'], debug=True, port=5001)
