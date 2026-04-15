import time
import lgpio as sbc
from pca9685 import Controller

def main():
    controller = Controller(sbc, 1, 0x40)
    output = controller[15]

    freq = 50
    controller.set_update_rate(freq)

    minpulse = 0.5 / 1000 # ms ->   0°
    maxpulse = 2.5 / 1000 # ms -> 180°
    def set_angle(angle:float):
        pulse = (angle/180) * (maxpulse-minpulse) + minpulse
        return int(pulse * freq * 4096)
    
    output.pwm_off = 0
    output.pwm_on = 0
    while True:
        output.pwm_off = set_angle(80)
        time.sleep(1)
        output.pwm_off = set_angle(100)
        time.sleep(1)
        
main()    
