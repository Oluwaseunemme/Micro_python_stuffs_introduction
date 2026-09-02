from machine import*
import time
g_led=Pin(4,Pin.OUT)
r_led=Pin(2,Pin.OUT)
b_led=Pin(15,Pin.OUT)

mode_key=Pin(5,Pin.IN,Pin.PULL_UP)
up_key=Pin(18,Pin.IN,Pin.PULL_UP)
down_key=Pin(19,Pin.IN,Pin.PULL_UP)
def_key=Pin(21,Pin.IN,Pin.PULL_UP)

r_oldtime=0
b_oldtime=0
g_oldtime=0

countn=4
intervals=[500,600,1000]
def show_default():
    print("Default delay time settings")
    print("*******************************")
    print("red_delay:",intervals[0])
    print("green_delay:",intervals[1])
    print("blue_delay:",intervals[2])
def blink_leds():
    global r_oldtime,b_oldtime,g_oldtime
    if time.ticks_ms()-r_oldtime>=intervals[0]:
        r_oldtime=time.ticks_ms()
        r_led.value(not r_led.value())
    if time.ticks_ms()-g_oldtime>=intervals[1]:
        g_oldtime=time.ticks_ms()
        g_led.value(not g_led.value())
    if time.ticks_ms()-b_oldtime>=intervals[2]:
        b_oldtime=time.ticks_ms()
        b_led.value(not b_led.value())
def control_led():
    if up_key.value()==0 and countn<3:
        time.sleep_ms(30)
        intervals[countn]+=1
        show_led()
    elif down_key.value()==0 and countn<3:
        time.sleep_ms(30)
        intervals[countn]-=1
        show_led()
def show_leds():
    if countn==0:
        print("*******************************")
        print("Red led mode.....")
        print("********************************")
    elif countn==1:
        print("*******************************")
        print("Green led mode.....")
        print("********************************")
    elif countn==2:
        print("*******************************")
        print("Blue led mode.....")
        print("********************************")
    elif countn==4:
        print("idle state.....")
def show_led():
    if countn==0:
        print("Red:",intervals[countn])
    elif countn==1:
        print("Green:",intervals[countn])
    elif countn==2:
        print("Blue:",intervals[countn])
def control_countn():
    global countn
    if mode_key.value()==0:
        time.sleep_ms(150)
        if countn>0:
            countn-=1
            show_leds()
        else:
            countn=4
            show_leds()
while 1:
    if def_key.value()==0:
        intervals[0]=500
        intervals[1]=600
        intervals[2]=1000
        show_default()
        countn=3
    blink_leds()
    control_led()
    control_countn()