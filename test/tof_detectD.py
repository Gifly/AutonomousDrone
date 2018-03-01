#import sys
#sys.path.insert(0, '/home/pi/Documents/AutonomousDrone')
import time
import VL53L0X

GOOD_ACCURACY_MODE      = 0   # Good Accuracy mode
BETTER_ACCURACY_MODE    = 1   # Better Accuracy mode
BEST_ACCURACY_MODE      = 2   # Best Accuracy mode
LONG_RANGE_MODE         = 3   # Longe Range mode
HIGH_SPEED_MODE         = 4   # High Speed mode

tof = VL53L0X.VL53L0X()
tof.start_ranging(4)
time.sleep(0.001)
distance = tof.get_distance()

while distance > 100:
    distance = tof.get_distance()
    print("La distancia")
    print(distance)

tof.stop_ranging()
