"""
    Main Loop for Pepper
"""
import qi
import sys
import time
import json

from pepper_utils import PepperUtils

def main(session):
    stop_condition = False

    # Main loop of Pepper.
    # We check if a person in front of the Robot and greet him/her
    try:
        while not stop_condition:
            pepper_utils.sonar_detector.check_person()        

            # If this is true, we have recognized the person
            # We shouldn't check anymore for check_person, but for check_closure
            # if we want to detect if the person is going away
            if pepper_utils.sonar_detector.greet:
                print("Greet is True.")
                pepper_utils.dance_engine.doHello()
                pepper_utils.dance_engine.resetPosture()

                # "Per cambiare gioco usa il plsnate sul tablet.
                # "Uso di default il gioco "Nome gioco" (prendi da user)
                # Da far dire una sola volta


                # We should also check if the person is leaving or not
                pepper_utils.sonar_detector.check_closure()
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
    posture_service = session.service("ALRobotPosture")
    tts = session.service("ALTextToSpeech")

    # Initialize the PepperUtils object
    pepper_utils = PepperUtils({
        'memory': memory_service,
        'sonar': sonar_service,
        'motion': motion_service,
        'dialog': dialog_service,
        'posture': posture_service,
        'tts': tts
    })

    # Start the session
    main(session)