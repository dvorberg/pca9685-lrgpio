from pca9685 import Controller

def main():
    import lgpio as sbc
    controller = Controller(sbc, 1, 0x40)
    last = controller[14]

    freq = 50
    controller.set_update_rate(freq)

    minpulse = 0.5 / 1000 # ms ->   0°
    maxpulse = 2.5 / 1000 # ms -> 180°
    def set_angle(angle:float):
        pulse = (angle/180) * (maxpulse-minpulse) + minpulse
        return int(pulse * freq * 4096)
    
    last.pwm_off = 0
    last.pwm_on = 0
    while True:
        last.pwm_off = set_angle(80)
        time.sleep(1)
        last.pwm_off = set_angle(100)
        time.sleep(1)
        
main()    
