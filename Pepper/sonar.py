import time

class SonarDetector(object):
    def __init__(self, services, config):
        super(SonarDetector, self).__init__()
        self.services = services
        self.config = config

        # Get the services ALMemory, ALMotion, ALTextToSpeech from self.services
        self.memory_service = self.services[0]
        self.sonar_service = self.services[1]
        self.tts = self.services[2]
        
        # Threshold for the front sonar
        self.threshold = self.config['sonar_threshold'] # Default: 0.5 meters (50 cm)
        self.greet = False

    """
    Check if the person is leaving or not.
    """
    def check_closure(self):
        sonar_front_value, sonar_back_value = self.get_sonar_value()

        if self.greet and ((sonar_front_value == 0.0) or (sonar_front_value > self.threshold)):
            self.greet = False
            self.tts.say("Hey Gian, I see you are leaving. Goodbye!")
        
        if self.greet and ((sonar_back_value == 0.0) or (sonar_back_value > self.threshold)):
            self.greet = False
            self.tts.say("Hey Gian, I see you are leaving. Goodbye!")

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
        # If the sonar front value is greater than the threshold, we greet the person
        if(sonar_front_value != 0.0) and (sonar_front_value < self.threshold and not self.greet):
            self.greet = True
            self.tts.say("Hello! Let me recognize you.")

            print("GETTING THE IMAGE!")
            # Here we should call the face recognition module from the API
            time.sleep(3.0)

            self.tts.say("Nice to meet you Gian! I am Pepper.")
        elif(sonar_back_value != 0.0) and (sonar_back_value < self.threshold) and not self.greet:
            self.tts.say("Hey! I see you're behind me! Please come in front of me, so I can recognize you.")
        else:
            self.greet = False

        return self.greet