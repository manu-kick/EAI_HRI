from flask import Flask, render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Configure the MySQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://freedb_hri_user:b$4HB$P7#$J#Sr!@sql.freedb.tech/freedb_hri_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

#----------------------------------------------
#----------------------------------------------
#----------------------------------------------

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
        return f'{self.name} {self.surname} ({self.age})'
    


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
    return render_template('index.html')


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
        

# 5. /serve_game/{game_name} (set in the current session in the database the game that the user is playing and serve the game to the user)
@app.route('/serve_game/<game_name>')
def serve_game(game_name):
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"

    # let's suppose we have for now the User Id of the current user
    user_id = 0
    # Get the profile of the user with user_id from the database

    user = User('John', 'Doe', 25, "[1,2,3,4,5]", favorite_game  = 'tic_tac_toe', id = user_id)


    #TODO Suppose here to send message to 
    if game_name == 'tic_tac_toe':
        # serve the html file in the /tictactoe/tictactoe.hmtl folder
        return render_template('/tictactoe/tictactoe.html', user=user.get_profile())


    else:
        # serve the html file in the /semantic_ping_pong/semantic_ping_pong.html folder
        return "Serve semantic ping pong game"
    
@app.route('/serve_game/')
def serve_game(session):
    
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"

    # let's suppose we have for now the User Id of the current user
    user_id = 0
    # Get the profile of the user with user_id from the database

    user = User('John', 'Doe', 25, "[1,2,3,4,5]", favorite_game  = 'tic_tac_toe', id = user_id)


    #TODO Suppose here to send message to 
    if game_name == 'tic_tac_toe':
        # serve the html file in the /tictactoe/tictactoe.hmtl folder
        return render_template('/tictactoe/tictactoe.html', user=user.get_profile())


    else:
        # serve the html file in the /semantic_ping_pong/semantic_ping_pong.html folder
        return "Serve semantic ping pong game"
    

# 8. /api/{game_name}/store_result (store the result of the game in the database)
@app.route('/api/<game_name>/store_result',  methods=['POST'])
def store_result(game_name):
    # Get the Post data "type" and "user_id"
    data = request.json
    if game_name == 'tic_tac_toe':
        type_ = data['type']
        user_id = data['user_id']

        # Store the result in the database in the table TicTacToe
        new_result = TicTacToeModel(user_id=user_id, outcome=type_)
        db.session.add(new_result)
        db.session.commit()
    else:
        # TO implement the semantic ping pong
        raise NotImplementedError

    return {
        'result': 'success'
    }




if __name__ == '__main__':
    app.run(debug=True, port=5001)
