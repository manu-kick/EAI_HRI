# Sonar simulation using memory keys
#
# Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value
# Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value

import qi
import argparse
import sys
import time
import json

memkey = {
    'SonarFront': 'Device/SubDeviceList/Platform/Front/Sonar/Sensor/Value',
    'SonarBack':  'Device/SubDeviceList/Platform/Back/Sonar/Sensor/Value' }

def main():
    # Read the configuration file from JSON
    with open('../config.json') as json_file:
        config = json.load(json_file)

    parser = argparse.ArgumentParser()
    parser.add_argument("--sensor", type=str, default="SonarFront",
                        help="Sensor: SonarFront, SonarBack")
    parser.add_argument("--value", type=float, default=0.75,
                        help="Sensor measurement")
    parser.add_argument("--duration", type=float, default=3.0,
                        help="Duration of the event")

    args = parser.parse_args()

    session = qi.Session()

    # Starting application
    try:
        session.connect("tcp://{}:{}".format(config['pepper_ip'], config['pepper_port']))
        print("Correctly connected to Pepper at " + config['pepper_ip'] + ":" + str(config['pepper_port']))
    except RuntimeError:
        print("Can't connect to Naoqi at ip \"" + config['pepper_ip'] + "\" on port " + str(config['pepper_port']) +".\n"
                "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)

    #Starting services
    memory_service  = session.service("ALMemory")

    val = None
    try:
        val = float(args.value)
    except:
        print("ERROR: value not numerical")
        return

    try:
        mkey = memkey[args.sensor]
        print("Sonar %s = %f" %(args.sensor,val))
        memory_service.insertData(mkey,val)
        time.sleep(args.duration)
        memory_service.insertData(mkey,0.0)
    except:
        print("ERROR: Sensor %s unknown" %args.sensor)

if __name__ == "__main__":
    main()