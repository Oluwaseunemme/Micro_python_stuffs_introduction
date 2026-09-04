from time import sleep,ticks_ms,mktime,localtime
from network import WLAN, STA_IF
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from dht import DHT11
import ubinascii
import urequest as request

oldtime_folder=0
oldtime_data=0
countn=0
countn2=0
new_folder="data_folder.txt"
content="DATA:"
ssid=""
password="E*******!"
dht_pin=Pin(15)
scl=Pin(22,Pin.OUT,Pin.PULL_UP)
sda=Pin(21,Pin.OUT,Pin.PULL_UP)
sta=WLAN(STA_IF)

sta.active(1)
i2c=I2C(sda=sda, scl=scl , freq=400000)
oled=SSD1306_I2C(128, 64, i2c, addr=0x3C)
sta.connect(ssid, password)
word="trying"
time_tupple=(2025, 7, 22, 4, 20, 0, 3, 203, 0)
mktime(time_tupple)

api_key="e66836****************"
file_src="data_folder.txt" #source of file to upload
vault_id= "2369dd*****************"#gottent from walrus url,encoded id name of vault
parent_id= "9e313e5*************************" #encoded id of folder in vault for my content storage
url='https://api.tusky.io/uploads/?vaultId='+vault_id+'&parentId='+parent_id

def post_to_walrus():
    with open(file_src,'rb') as f:#opening file as f 'rb' means i wanna read in byte format
        file_content = f.read()
        length=len(file_content) #getting the size for header
        filename = f"file{countn2}.txt" #content name on walrus
        print("new file created:"+filename)
        Encode_filename=ubinascii.b2a_base64(filename.encode()).decode().strip()#helps encode content name for walrus
        headers = {
            'Api-Key':api_key,
            'Tus-Resumable': '1.0.0',
            'Upload-Metadata': f"filename {Encode_filename}",#encoded file name
            'Upload-Length': str(length),
            'Content-Type': 'application/offset+octet-stream',
            #'Upload-Offset': '0',
            }
    
    resp = request.post(url, headers=headers)
    print("POST status", resp.status_code)
    location = resp.headers.get('Location')
    #resp.close()

    if resp.status_code not in (201, 204) or not location:#helps check if status_code is not in success codes 2++
        print("Upload creation failed:", resp.text)

    #patch header below
    patch_headers = {
        'Api-Key':api_key,
        'Tus-Resumable': '1.0.0',
        'Upload-Offset': '0',  # This is dynamic, depending on chunk position
        'Content-Type': 'application/offset+octet-stream',
    }
    patch_resp = request.patch(location, data=file_content, headers=patch_headers)
    print("PATCH status:", patch_resp.status_code)
    print("Tusky offset now:", patch_resp.headers.get("Upload-Offset"))
    patch_resp.close()
    if resp.status_code==201 and resp.status_code==201:
        print("Upload to walrus is a success.....")
        oled.text("Uploaded.....",1 ,47)
    else:
        
        oled.text("Upload done.....",1 ,47,0)
        oled.text("Upload failed!!..",1 ,47)

def get_data():
    dht=DHT11(dht_pin)
    dht.measure()
    datas= f"Temperature:{dht.temperature()}°c , Humidity:{dht.humidity()}%"
    return datas
    
def get_time():
    ct=localtime()
    formatted_time=f"{ct[0]}Y:{ct[1]}M:{ct[2]}d:{ct[3]}h:{ct[4]}m:{ct[5]}s"
    return formatted_time
    
def connect_esp():
    global word
    while sta.isconnected()!= 1:
            #print(sta.isconnected())
            oled.text(word, 1, 5)
            oled.show()
            word=word+"."
            sleep(.2)
            oled.fill(0)
            
    oled.text("Connected....", 1, 5)
    oled.text(f"A.P:{ssid}", 1, 16)
    oled.show()
    sleep(.2)
    oled.fill(0)
    
def creat_new(folder_interval):
    global oldtime_folder
    global file_src
    global content
    global countn2
    global filename
    if ticks_ms()-oldtime_folder>=folder_interval:
        oled.text(f"Compiled:{countn2}", 1, 32, 0)
        countn2=countn2+1
        oldtime_folder=ticks_ms()
        print(content)
        with open(file_src,'w') as my_file:
            my_file.write(content)
            #new_folder="folder"+str(countn2)+".txt"
            content="weather_infos:"
        if content not="DATA:":
            post_to_walrus()
        
        oled.text(f"Compiled:{countn2}", 1, 32)
        oled.show()
        
        
def combine_data(data_interval):
    global oldtime_data
    global countn
    global content
    
    if ticks_ms()-oldtime_data>=data_interval:
        oldtime_data=ticks_ms()
        #get_data()
        oled.text(f"NO:{countn}", 1, 16 ,0)
        countn=countn+1
        oled.text("Compiling data...", 1, 5)
        oled.text(f"NO:{countn}", 1, 16)
        oled.show()
        content=content +f"\n[datas:{get_data()} , time:{get_time()}]"
        
while 1:
    if sta.isconnected()!= 1:
        connect_esp()
        
    #print(get_time())
    #print(get_data())
    creat_new(60000)
    combine_data(5000)
        