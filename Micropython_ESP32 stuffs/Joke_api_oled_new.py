from network import*
from machine import*
from ssd1306 import*
from time import*
from urequest import*

ssid="**********"
password="E***********88"
url="https://v2.jokeapi.dev/joke/Any?format=txt"
scl=Pin(22,Pin.OUT,Pin.PULL_UP)
sda=Pin(21,Pin.OUT,Pin.PULL_UP)
sta=WLAN(STA_IF)

sta.active(1)
i2c=I2C(sda=sda, scl=scl , freq=400000)
oled=SSD1306_I2C(128, 64, i2c, addr=0x3C)
sta.connect(ssid, password)
word="trying"

def wrap_text(word):
        word_list=word.split()
        text_it=""
        y_axis=0
        oled.fill(0)
        for x in word_list:
            if len(text_it+x) < 15:
                text_it=text_it+" "+x
            else:
                oled.text(text_it, 0, y_axis)
                oled.show()
                y_axis=y_axis+9
                text_it= x
        oled.text(text_it, 0, y_axis)
        oled.show()
countn=0
def get_joke():
    request = urlopen(url, data=None, method="GET")
    joke=request.read().decode('utf-8')
    wrap_text(joke)
    print(joke)
interval=30000
oldtime=0
def new_joke():
    global oldtime
    if ticks_ms()-oldtime >=interval:   
        oldtime=ticks_ms()
        get_joke()
while 1:
    if sta.isconnected() == 1:
         if countn==0:
            oled.text("Connected....", 1, 5)
            oled.text(f"A.P:{ssid}", 1, 16)
            oled.show()
            sleep(.5)
            get_joke()
            countn=1
    else:
        #print(sta.isconnected())
        oled.text(word, 1, 5)
        oled.show()
        word=word+"."
        sleep(.35)
    oled.fill(0)
    sleep(.3)
    new_joke()