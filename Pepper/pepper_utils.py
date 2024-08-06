# Hack to get the User class in here
# Add the path to the Master/Tablet directory to the Python path
import os
import sys

master_dir = os.path.join(os.path.dirname(__file__), '..', 'Master')
tablet_dir = os.path.join(os.path.dirname(__file__), '..', 'Tablet')
sys.path.append(master_dir)
sys.path.append(tablet_dir)

from User import User
from selenium import webdriver

class TalkEngine(object):
    def __init__(self, services):
        super(TalkEngine, self).__init__()
        self.services = services
        self.tts = self.services['tts']

    def say(self, text, _async=False):
        self.tts.say(text, _async=_async)
        return

class DanceEngine(object):
    def __init__(self, services):

        super(DanceEngine, self).__init__()
        self.services = services
        self.motion_service = self.services['motion']
        self.posture_service = self.services['posture']

    def resetPosture(self):
        self.posture_service.goToPosture("StandInit", 1.0)
        return
    
    def doHello(self):
        jointNames = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw", "RHand", "HipRoll", "HeadPitch"]
        angles = [-0.141, -0.46, 0.892, -0.8, 0.98, -0.07, -0.07]
        times  = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
        isAbsolute = True

        self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

        for i in range(2):
            jointNames = ["RElbowYaw", "HipRoll", "HeadPitch"]
            angles = [1.7, -0.07, -0.07]
            times  = [0.2, 0.2, 0.2]

            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            # Wave the hand back and forth
            angles = [1.3, -0.07, -0.07]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)
        return

    def doLose(self):
        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.44, 0.92, 1.32, 1.76, 2.24])
        keys.append([-0.515251, -0.34076, -0.0929187, -0.257377, -0.329649])

        names.append("HeadYaw")
        times.append([0.44, 0.92, 1.16, 1.32, 1.48, 1.68, 1.92, 2.24])
        keys.append([-0.0156179, -0.0135287, -0.12827, 0.0965434, -0.12827, 0.0965434, -0.0173475, -0.0123995])

        names.append("HipPitch")
        times.append([0.44, 0.92, 1.76])
        keys.append([-0.158713, -0.0544052, -0.277851])

        names.append("HipRoll")
        times.append([0.44, 0.92, 1.76])
        keys.append([-0.0168668, 0.0440326, 0.00417265])

        names.append("KneePitch")
        times.append([0.44, 0.92, 1.76])
        keys.append([0.0375921, -0.0223025, 0.0887257])

        names.append("LElbowRoll")
        times.append([0.44, 0.92, 1.52, 2.24])
        keys.append([-0.425005, -0.68766, -0.425288, -0.416156])

        names.append("LElbowYaw")
        times.append([0.44, 0.92, 1.48, 2.24])
        keys.append([-1.39032, -1.9088, -1.96299, -1.45377])

        names.append("LHand")
        times.append([0.44, 0.92, 1.52, 2.24])
        keys.append([0.305394, 0.62, 0.314203, 0.306419])

        names.append("LShoulderPitch")
        times.append([0.44, 0.92, 1.52, 2.24])
        keys.append([1.41011, 1.45418, 1.40624, 1.46352])

        names.append("LShoulderRoll")
        times.append([0.44, 0.92, 1.52, 2.24])
        keys.append([0.241407, 0.44927, 0.246933, 0.18874])

        names.append("LWristYaw")
        times.append([0.44, 0.92, 1.52, 2.24])
        keys.append([-0.111101, -0.111101, -0.108112, 0.0977037])

        names.append("RElbowRoll")
        times.append([0.44, 0.72, 1.16, 1.52, 2.24])
        keys.append([0.431716, 0.429253, 0.998328, 0.428422, 0.413016])

        names.append("RElbowYaw")
        times.append([0.44, 0.92, 1.32, 1.52, 2.24])
        keys.append([1.21446, 2.02109, 2.02008, 1.91888, 1.19382])

        names.append("RHand")
        times.append([0.44, 0.92, 1.16, 1.32, 1.52, 2.24])
        keys.append([0.315043, 0.98, 0.98, 0.65, 0.53724, 0.3])

        names.append("RShoulderPitch")
        times.append([0.44, 0.92, 1.32, 1.52, 2.24])
        keys.append([1.41886, 1.14145, 1.42942, 1.4546, 1.46675])

        names.append("RShoulderRoll")
        times.append([0.44, 0.92, 1.32, 1.52, 2.24])
        keys.append([-0.194604, -0.212728, -0.211925, -0.204261, -0.181265])

        names.append("RWristYaw")
        times.append([0.44, 0.92, 1.32, 1.52, 2.24])
        keys.append([-0.0875347, 0.912807, 0.90059, 0.783567, 0.108709])        
        self.motion_service.angleInterpolation(names, keys, times, True)
        return

    def doDraw(self):
        names = list()
        times = list()
        keys = list()

        names.append("HeadPitch")
        times.append([0.72, 1.2, 3.16, 4.72, 5.2, 5.56])
        keys.append([-0.113446, 0.224996, 0.200713, 0.240855, 0.125664, -0.20886])

        names.append("HeadYaw")
        times.append([1.2, 4.72, 5.56])
        keys.append([0.154895, 0.157081, -0.305068])

        names.append("HipPitch")
        times.append([0.56, 1.2, 4.16, 5.08])
        keys.append([-0.0409819, -0.216292, -0.348214, -0.0433329])

        names.append("HipRoll")
        times.append([0.56, 1.2, 4.16, 5.08])
        keys.append([0, -0.0567572, -0.0352817, -0.00344329])

        names.append("KneePitch")
        times.append([0.56, 1.2, 4.16, 5.08])
        keys.append([-0.0110766, 0.0291458, 0.075165, -0.012951])

        names.append("LElbowRoll")
        times.append([0.64, 1.12, 4.64, 5.12, 5.48])
        keys.append([-0.799361, -1.48487, -1.51669, -1.53414, -1.37739])

        names.append("LElbowYaw")
        times.append([0.64, 1.12, 4.64, 5.48])
        keys.append([-1.40324, -0.955723, -0.909316, -1.54856])

        names.append("LHand")
        times.append([0.64, 1.12, 1.68, 2.08, 2.68, 3.08, 3.76, 4.16, 4.64, 5.12, 5.48])
        keys.append([0.96, 0.7036, 0.44, 0.73, 0.44, 0.73, 0.44, 0.73, 0.65, 0.52, 0.844074])

        names.append("LShoulderPitch")
        times.append([1.12, 4.64, 5.12, 5.48])
        keys.append([-0.512397, -0.581195, 0.0994838, 0.44047])

        names.append("LShoulderRoll")
        times.append([1.12, 4.64, 5.48])
        keys.append([0.328234, 0.342085, 0.233874])

        names.append("LWristYaw")
        times.append([0.64, 1.12, 4.64, 5.48])
        keys.append([-0.895354, -0.833004, -0.862194, 0.0192082])

        names.append("RElbowRoll")
        times.append([0.56, 1.04, 4.56, 5.04, 5.4])
        keys.append([0.574213, 0.382009, 0.20402, 0.375246, 0.25889])

        names.append("RElbowYaw")
        times.append([0.56, 1.04, 4.56, 5.4])
        keys.append([1.47829, 1.23483, 1.23639, 1.2217])

        names.append("RHand")
        times.append([0.56, 1.04, 4.56, 5.04, 5.4])
        keys.append([0.54, 0.3504, 0.510545, 0.31, 0.412984])

        names.append("RShoulderPitch")
        times.append([1.04, 4.56, 5.4])
        keys.append([1.54785, 1.36831, 1.43506])

        names.append("RShoulderRoll")
        times.append([1.04, 4.56, 5.4])
        keys.append([-0.108956, -0.085903, -0.119999])

        names.append("RWristYaw")
        times.append([0.56, 1.04, 4.56, 5.4])
        keys.append([0.497419, 0.030638, 0.093532, -0.033162])

        self.motion_service.angleInterpolation(names, keys, times, True)
        return

    def doPop(self):
        jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll"]
        angles = [0.64, 1.55, 0.64, -1.55]
        times = [0.5, 0.5, 0.5, 0.5]
        isAbsolute = True

        self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

        for i in range(2):
            jointNames = ["RShoulderPitch", "RElbowRoll", "LShoulderPitch", "LElbowRoll", "HipRoll"]
            times = [0.5, 0.5, 0.5, 0.5, 0.5]

            angles = [0.34, 1.25, 1, -1.25, 0.15]                
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            angles = [1, 1.85, 0.34, -1.85, 0.15]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            angles = [0.34, 1.25, 1, -1.25, -0.15]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)

            angles = [1, 1.85, 0.34, -1.85, -0.15]
            self.motion_service.angleInterpolation(jointNames, angles, times, isAbsolute)
        
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
        self.config = self.services['config']

        # Get the Talk and Dance Engines as well
        self.talk_engine = TalkEngine(self.services)
        self.dance_engine = DanceEngine(self.services)

        # Threshold for the front sonar
        self.threshold = self.config['sonar_threshold'] # Default: 0.5 meters (50 cm)
        self.greet = False
        self.behind_me = False
        self.driver = None

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
            self.behind_me = False
            self.talk_engine.say("Hello! Let me recognize you.", _async=True)
            self.dance_engine.doHello()

            # Start a new instance of Chromium webdriver
            self.driver = webdriver.Chrome(executable_path=r'selenium\chromedriver.exe')

            # Use Selenium to go to page :5002/api/identify_user
            initial_url = "http://127.0.0.1:5002/api/identify_user"
            self.driver.get(initial_url)
            self.dance_engine.resetPosture()
        elif(sonar_back_value != 0.0) and (sonar_back_value < self.threshold) and not self.greet and not self.behind_me:
            self.talk_engine.say("Hey! I see you're behind me! Please come in front of me, so I can recognize you.", _async=True)
            self.behind_me = True
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