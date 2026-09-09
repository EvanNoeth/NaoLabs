import sys, time, os, qi

if len(sys.argv) > 1 and len(sys.argv) < 3: #ensures proper number of arguments
    ROBOT_IP = sys.argv[1]
    ROBOT_PORT = 9559
else:
    print("please provide proper number of arguments")
    print("Proper program usage: python3 name.py IP_ADDRESS_HERE")
    sys.exit(1)

def main():
    session = qi.Session()
    try:
        print(f"Connecting to NAO at {ROBOT_IP}:{ROBOT_PORT}...")
        session.connect(f"tcp://{ROBOT_IP}:{ROBOT_PORT}")
        print("Successfully connected to NAO!")
    except RuntimeError as e:
        print(f"Failed to connect to the robot at {ROBOT_IP}: {e}")
        print("Please try again")
        sys.exit(1)

    try:
        tts = session.service("ALTextToSpeech") #initialized text-to-speech service
        pos = session.service("ALRobotPosture")
        led = session.service("ALLeds")
        joint = session.service("ALMotion")
    except Exception as e:
        print(f"Failed to load services: {e}")
        sys.exit(1)
    pos.goToPosture("Stand", 1.0)
    tts.say("Hello, human. I am Nao.")
    joint.setAngles("LShoulderPitch", 0.5, 0.2)
    tts.say("Today we will do the Three good things exercise.")
    led.fadeRGB("FeetLeds", 0xFF0000, 0.5) #makes feet turn red
    time.sleep(1)
    joint.setAngles("HeadYaw", 0.5236, 0.3)
    tts.say("This exercise will have both me and you taking turns sharing three things we are grateful for that have happened to us in the last week!")
    time.sleep(1)
    joint.rest()
    
    #TODO finish Nao's introduction

if __name__ == "__main__":
    main()