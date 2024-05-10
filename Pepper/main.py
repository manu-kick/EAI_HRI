"""
    Main Loop for Pepper
"""
import qi
import sys
import time
import json

from pepper_utils import PepperUtils

pepper_endpoint = None

def main(session):

    # Main loop of Pepper.
    # We check if a person in front of the Robot and greet him/her
    try:
        while not pepper_utils.sonar_detector.greet:
            pepper_utils.sonar_detector.check_person()

            # If this is true, we have recognized the person
            # We shouldn't check anymore for check_person, but for check_closure
            # if we want to detect if the person is going away
            while pepper_utils.sonar_detector.greet:

                # This will automatically exit the while loop if the person is going away
                # Because the variable greet will be set to False in check_closure
                if pepper_utils.sonar_detector.check_closure():
                    pepper_utils.sonar_detector.driver.quit()
                    pepper_utils.talk_engine.say("Hey, I see you are leaving. Goodbye!", _async=True)
                    pepper_utils.dance_engine.doHello()
                    pepper_utils.dance_engine.resetPosture()
                    pepper_utils.sonar_detector.driver = None

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

    # Starting application
    try:
        connection_url = "tcp://{}:{}".format(config['pepper_ip'], config['pepper_port'])
        app = qi.Application(["MainPepper", "--qi-url=" + connection_url])
        print("Correctly connected to Pepper at " + config['pepper_ip'] + ":" + str(config['pepper_port']))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + config['pepper_ip'] + "\" on port " + str(config['pepper_port']) +".\n"
                "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    app.start()
    session = app.session

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