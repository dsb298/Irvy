from client import TcpClient
from pydualsense import *
import pygame
import struct
import time

dualsense = pydualsense()
dualsense.init()
pygame.init()
joystick = ''
# joystick = pygame.joystick.Joystick(0)

HOST = '192.168.1.220'
PORT = 12345

G = 9.81
filt_g = [0,0,0,0,0]
filt_idx = 0

def avg_filt(accel_g):
    global filt_g
    global filt_idx
    if(filt_idx == 5):
        filt_idx = 0
    filt_g[filt_idx] = accel_g
    avg_g = 0
    for val in filt_g:
        avg_g += val
    filt_idx += 1
    return avg_g/5

def main():
    myClient = TcpClient()
    myClient.connect(HOST, PORT)

    msg = b''

    # axis = joystick.get_axis
    rightJoy = [1300,2450]
    sendServoData = True

    run_code = True
    while(run_code):

        # Setup controller
        # axes = joystick.get_numaxes()
        # buttons = joystick.get_numbuttons()

        # msg = myClient.recv_data()
        # msg = struct.unpack('<6f', msg)
        # data = [round(val, 3) for val in msg]
        # amnt = int(avg_filt(data[2]))
        # vib_amnt = 0
        # if(amnt < 9.5):
        #     vib_amnt = 0
        # elif(amnt > 12):
        #     vib_amnt = 255
        # else:
        #     vib_amnt = (amnt - 9.5) * 102

        # if(vib_amnt < 10):
        #     vib_amnt = 0
        # print(vib_amnt)
        # dualsense.setLeftMotor(int(vib_amnt))
        # dualsense.setRightMotor(int(vib_amnt))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_code = False

            # Connect device
            if event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                print(f"Joystick {joystick.get_instance_id()} connencted")

            # Disconnect Device
            if event.type == pygame.JOYDEVICEREMOVED:
                del joystick[event.instance_id]
                print(f"Joystick {event.instance_id} disconnected")

            # Check buttons
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    run_code = False
                elif event.button == 0:
                    rightJoy = [1300,2450]
                    sendServoData = True

                    # dualsense.setLeftMotor(255)
                    # dualsense.setRightMotor(255)
                # elif event.button == 1:
                    # dualsense.setLeftMotor(0)
                    # dualsense.setRightMotor(0)

            # Check joysticks
            if event.type == pygame.JOYAXISMOTION:
                # rightJoy[0] = ((round(joystick.get_axis(3), 3)-(-1))/(1-(-1))*(12-2)+2)
                # rightJoy[1] = ((round(joystick.get_axis(4), 3)-(-1))/(1-(-1))*(12-6)+6)
                if(rightJoy[0] < 2490 and rightJoy[0] > 510):
                    rightJoy[0] += 10*round(joystick.get_axis(3), 1)
                    # if(deadCheck > 1 or deadCheck < -1):
                    #     rightJoy[0] += deadCheck
                    #     sendServoData = True
                else:
                    rightJoy[0] = 1300
                if(rightJoy[1] < 2490 and rightJoy[1] > 1300):
                    rightJoy[1] += 10*round(joystick.get_axis(4), 1)
                    # if(deadCheck > 1 or deadCheck < -1):
                    #     rightJoy[1] += deadCheck
                    #     sendServoData = True
                else:
                    rightJoy[1] = 2450
                print(10*round(joystick.get_axis(4), 1))

        # if(sendServoData):
        msg = struct.pack('<2d',*rightJoy)
        myClient.send_data(msg)
            # sendServoData = False
        time.sleep(.05)


        # rightJoy[0] = joystick.get_axis(2)
        # rightJoy[1] = joystick.get_axis(2)
        # buttonOption = joystick.get_button(9)
        # # buttonX = joystick.get_button(0)
        # if(joystick.get_button(0)):
        #     print("pressed!")
        # buttonCircle = joystick.get_button(1)

        # print(f"Button {0:>2} value: {buttonX}")
        # print(joystick.values())

        # print(rightJoy)

if __name__ == "__main__":
    main()
    dualsense.close()
    pygame.quit()