from dht import DHT11
from time import sleep
from machine import Pin
while 1:
    sleep(0.45)
    dht=DHT11(Pin(22))
    dht.measure()
    print(f"Temperature:{dht.temperature()}°c       Humidity:{dht.humidity()}%")