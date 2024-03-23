from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Worldd!'


# 1. /api/identify_user (starting from an image, the server runs an algorithm and identifies the user in the database, if the user is not present, it creates a new user in the database and returns the user's profile)
@app.route('/api/identify_user')
def identify_user():
    return 'Identify User'


# 2. /api/send_user_details
@app.route('/api/send_user_details')
def send_user_details():
    return 'Send User Details'


# 3. /api/get_game (the master knows which game to send to the user)
@app.route('/api/get_game')
def get_game():
    return 'Get Game'

# 4. /api/elaborate_mental_model (elaborate the mental model of the user setting a difficulty level based on the user's profile)
@app.route('/api/elaborate_mental_model')
def elaborate_mental_model():
    return 'Elaborate Mental Model'


# 5. /serve_game/{game_name} (serve the game to the user)
@app.route('/serve_game/<game_name>')
def serve_game(game_name):
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"

    if game_name == 'tic_tac_toe':
        # serve the html file in the /tictactoe/tictactoe.hmtl folder
        return render_template('/tictactoe/tictactoe.html')


    else:
        # serve the html file in the /semantic_ping_pong/semantic_ping_pong.html folder
        return "Serve semantic ping pong game"
        

# 6. /api/{game_name}/ask_user_feedback (receive the feedback from the user and store it in the database)
@app.route('/api/<game_name>/ask_user_feedback')
def ask_user_feedback(game_name):
    assert game_name == 'tic_tac_toe' or game_name == 'semantic_ping_pong', "Invalid game name"

    

# 7. api/{game_name}/emit_pepper_feedback (send the feedback to the Pepper robot)
@app.route('/api/<game_name>/emit_pepper_feedback')
def emit_pepper_feedback(game_name):
    return 'Emit Pepper Feedback ' + game_name

# 8. /api/{game_name}/store_result (store the result of the game in the database)
@app.route('/api/<game_name>/store_result')
def store_result(game_name):
    return 'Store Result ' + game_name


if __name__ == '__main__':
    app.run(debug=True)
