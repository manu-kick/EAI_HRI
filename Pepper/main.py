"""
    Main Loop for Pepper
"""

import qi
import sys
import time
import json

from sonar import SonarDetector

def main(session):
    stop_condition = False

    # Main loop of Pepper.
    # We check if a person in front of the Robot and greet him/her
    try:
        while not stop_condition:
            sonar_detector.check_person()

            # If this is true, we have recognized the person
            # We shouldn't check anymore for check_person, but for check_closure
            # if we want to detect if the person is going away
            if sonar_detector.greet:
                print("Greet is True.")

                # After identifying the person, we should start asking about the game, start the game and interact with the person
                # We should also check if the person is leaving or not
                sonar_detector.check_closure()
                stop_condition = True

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
    sonar_service = session.service("ALSonar")
    motion_service = session.service("ALMotion")
    dialog_service = session.service("ALDialog")
    tts = session.service("ALTextToSpeech")

    # SonarDetector
    sonar_detector = SonarDetector((memory_service, sonar_service, tts), config)

    # Start the session
    main(session)