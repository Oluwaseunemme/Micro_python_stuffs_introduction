from machine import*
from ssd1306 import*
from time import*
from dht import*
scl=Pin(22, Pin.OUT, Pin.PULL_UP)
sda=Pin(21, Pin.OUT, Pin.PULL_UP)
adc=ADC(Pin(25))
adc.width(10)
adc.atten(ADC.ATTN_11DB)
i2c=I2C(sda=sda, scl=scl , freq=400000)
oled=SSD1306_I2C(128, 64, i2c, addr=0x3C)
d=DHT11(Pin(23))

def rect_clear(x, y, width, height):
    oled.fill_rect(x, y, width, height, 0)
def print_dht():
    t=d.temperature()
    h=d.humidity()
    d.measure()
    print(f"Current temperature and humidity are {t}c and {h}% respectiely")
    oled.text("Temperature:"+str(t)+"*c", 2, 3)
    oled.text("Humidity:"+str(h)+"%", 2, 15)
    oled.show()
oldtime=0
interval=1000
while 1:
    if ticks_ms()-oldtime>=interval:
        oldtime=ticks_ms()
        print_dht()
    sleep(.01)
    oled.fill(0)