# Hack to get the User class in here
# Add the path to the Master/Tablet directory to the Python path
import os
import sys

master_dir = os.path.join(os.path.dirname(__file__), '..', 'Master')
tablet_dir = os.path.join(os.path.dirname(__file__), '..', 'Tablet')
sys.path.append(master_dir)
sys.path.append(tablet_dir)

import time
import requests

from User import User

class TalkEngine(object):
    def __init__(self, services):
        super(TalkEngine, self).__init__()
        self.services = services
        self.tts = self.services['tts']
        self.config = self.services['config']

    def say(self, text, _async=False):
        self.tts.say(text, _async=_async)
        return

class DanceEngine(object):
    def __init__(self, services):

        super(DanceEngine, self).__init__()
        self.services = services
        self.motion_service = self.services['motion']
        self.posture_service = self.services['posture']
        self.animation_service = self.services['animation']
        self.tts = self.services['tts']
        self.config = self.services['config']

    def resetPosture(self):
        self.posture_service.goToPosture("StandInit", 0.25)
        return
    
    def doHello(self):
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
        angles = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
        times  = [2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0]
        isAbsolute = True

        self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

        for i in range(2):
            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.7, -0.07, -0.07]
            times  = [0.8, 0.8, 0.8]

            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            # Wave the hand back and forth
            angles = [1.3, -0.07, -0.07]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)
        return

    def doLose(self):
        self.animation_service.run(".lastUploadedChoregrapheBehavior/thinking")
        return

    def doPop(self):
        jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll"]
        angles = [0.64, 1.55, 0.64, -1.55]
        times = [1.0, 1.0, 1.0, 1.0]
        isAbsolute = True

        self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

        loops = 0

        while loops < 3:
            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            times = [1.0, 1.0, 1.0, 1.0, 1.0]

            angles = [0.34, 1.25, 1, -1.25, 0.15]                
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            angles = [1, 1.85, 0.34, -1.85, 0.15]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            angles = [0.34, 1.25, 1, -1.25, -0.15]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            angles = [1, 1.85, 0.34, -1.85, -0.15]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            loops += 1
        
        # Reset to initial position
        angles = [0.64, 1.55, 0.64, -1.55, 0.0]
        self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

        return

class SonarEngine(object):
    def __init__(self, services):
        super(SonarEngine, self).__init__()
        self.services = services

        # Get the services ALMemory, ALMotion, ALTextToSpeech from the constructor
        self.memory_service = self.services['memory']
        self.motion_service = self.services['motion']
        self.posture_service = self.services['posture']
        self.animation_service = self.services['animation']
        self.tts = self.services['tts']
        self.config = self.services['config']

        # Get the Talk and Dance Engines as well
        self.talk_engine = TalkEngine(self.services)
        self.dance_engine = DanceEngine(self.services)

        # Threshold for the front sonar
        self.threshold = self.config['sonar_threshold'] # Default: 0.5 meters (50 cm)
        self.greet = False
        self.user = User(name="", surname="", age="", features="", favorite_game="", id=None)

    """
    Check if the person is leaving or not.
    """
    def check_closure(self):
        sonar_front_value, sonar_back_value = self.get_sonar_value()

        if self.greet and ((sonar_front_value == 0.0) or (sonar_front_value > self.threshold)):
            self.greet = False
            return True
        else:
            return False

    """
    Get the sonar value from the front sonar sensor.
    """
    def get_sonar_value(self):
        sonar_front_value = self.memory_service.getData("Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value")
        sonar_back_value = self.memory_service.getData("Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value")

        print("Sonar front value: " + str(sonar_front_value))
        print("Sonar back value: " + str(sonar_back_value))

        return sonar_front_value, sonar_back_value

    """
    Check if a person is in front or in the back of the robot.
    """
    def check_person(self):
        sonar_front_value, sonar_back_value = self.get_sonar_value()

        # In this case, we want to detect a person in front of the robot
        # If the sonar front value is smaller than the threshold, we greet the person
        if (sonar_front_value != 0.0) and (sonar_front_value < self.threshold and not self.greet):
            self.greet = True
            self.talk_engine.say("Hello! Let me recognize you.", _async=True)
            self.dance_engine.doHello()

            # Here we should call the face recognition module from the API
            # URL of the API endpoint
            url = 'http://' + self.config['master_ip'] + ':5002/api/identify_user'

            # Sending POST request
            print("Sending POST request to the API for Face Recognition...")
            response = requests.post(url)

            # Checking the response
            if response.status_code == 200:
                print("Request successful. Retrieving user...")
                # Retrieving the image from the request
                user = response.json()
                self.user = User(name=user['name'], surname=user['surname'], age=user['age'], features=user['features'], favorite_game=user['favorite_game'], id=user['id'])
            else:
                print("Error: ", response.status_code)
            
            self.talk_engine.say("Nice to meet you " + self.user.name + "! I am Pepper.")
        elif(sonar_back_value != 0.0) and (sonar_back_value < self.threshold) and not self.greet:
            self.talk_engine.say("Hey! I see you're behind me! Please come in front of me, so I can recognize you.")
        else:
            self.greet = False

        return self.greet
    
class PepperUtils():
    def __init__(self, services):
        self.services = services

        # Instantiate the various engines
        self.sonar_detector = SonarEngine(self.services)
        self.dance_engine = DanceEngine(self.services)
        self.talk_engine = TalkEngine(self.services)