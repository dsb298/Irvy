from server import TcpServer
import adafruit_mpu6050
import board
time.sleep(1)

HOST = '192.168.1.220'
PORT = 12345

i2c = board.I2C()
mpu = adafruit_mpu6050.MPU6050(i2c)

def main():
    myServer = TcpServer()
    myServer.connect(HOST, PORT)

    msg = b"Hello from server!"

    run_code = True
    while(run_code):
        print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (mpu.acceleration))
        print("Gyro X:%.2f, Y: %.2f, Z: %.2f rad/s" % (mpu.gyro))
        # myServer.send_data(msg)

        time.sleep(1)

if __name__ == "__main__":
    main()