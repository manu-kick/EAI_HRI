"""
    Main Loop for Pepper
"""
import qi
import sys
import time
import json
import requests

from pepper_utils import PepperUtils

pepper_endpoint = None

def main(session):
    count = 0

    # Main loop of Pepper.
    # We check if a person in front of the Robot and greet him/her
    try:
        while not pepper_utils.sonar_detector.greet:
            pepper_utils.sonar_detector.check_person()

            # If this is true, we have recognized the person
            # We shouldn't check anymore for check_person, but for check_closure
            # if we want to detect if the person is going away
            while pepper_utils.sonar_detector.greet:
                if(count == 0):
                    print("Greet is True.")
                    pepper_utils.dance_engine.doHello()
                    pepper_utils.dance_engine.resetPosture()
                    
                    # Pepper should say only once:
                    # "To change the game, use the button on the tablet"
                    # "I will use the game "Game Name" (take from user)
                    #
                    # This should be done with an endpoint request to the API "/api/say/<word>"
                    phrase = "To change the game, use the button on the tablet! I will use the game " + pepper_utils.sonar_detector.user.favorite_game
                    url = pepper_endpoint + '/api/say/' + phrase

                    # Sending GET request
                    print("Sending GET request to the API for informing the user about the next steps..")
                    response = requests.get(url)

                    # Checking the response
                    if response.status_code == 200:
                        print("Request successful. Pepper successfully greeted and informed the user about the next steps of the interaction.")
                    else:
                        print("Error: ", response.status_code)
                    count += 1

                # We should also check if the person is leaving or not
                if pepper_utils.sonar_detector.check_closure():
                    pepper_utils.talk_engine.say("Hey " + pepper_utils.sonar_detector.user.name + ", I see you are leaving. Goodbye!", _async=True)
                    pepper_utils.dance_engine.doHello()
                    pepper_utils.dance_engine.resetPosture()
                    count = 0

                # Wait for 1 second before checking sensors again
                time.sleep(1.0)
            # Wait for 1 second before checking sensors again
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        sys.exit(0)

if __name__ == "__main__":

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

    pepper_endpoint = 'http://' + config['master_ip'] + ':5003'

    # Start the session
    main(session)