class Pepper(object):
    def __init__(self, services, config):
        super(Pepper, self).__init__()
        self.services = services
        self.config = config

    def change_eye_color(self, color):
        # Change the eye color of the robot
        self.services[0].insertData("ALMemory/InsertData", "EyeLeds/rgb/Left/blink", color)
        self.services[0].insertData("ALMemory/InsertData", "EyeLeds/rgb/Right/blink", color)