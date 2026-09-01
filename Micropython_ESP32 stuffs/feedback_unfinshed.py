from machine import*
from time import sleep
from ssd1306 import*

scl=Pin(22, Pin.OUT, Pin.PULL_UP)
sda=Pin(21, Pin.OUT, Pin.PULL_UP)
i2c=I2C(sda=sda, scl=scl , freq=400000)
oled=SSD1306_I2C(128, 64, i2c, addr=0x3C)
adc=ADC(Pin(25))
pwm=PWM(Pin(4))
adc.width(10)
adc.atten(ADC.ATTN_11DB) 
pwm.freq(50000)

def get_feedback():
    return adc.read()
def set_duty():
    global duty_cycle
    if get_feedback() < 450:
        duty_cycle=duty_cycle+5
    elif get_feedback() > 500:
        duty_cycle=duty_cycle-5
duty_cycle=170
while 1:
    get_feedback()
    set_duty()
    pwm.duty(duty_cycle)
    print("duty_Cycle:", duty_cycle)
    print("feeback:", get_feedback())
    sleep(.005)