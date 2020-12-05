# Add the shortcut of this file in the folder to auto start on windows startup:
# C:\Users\admin\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
import requests, bs4
import win10toast
import time
from datetime import datetime,date
import csv
import os
import re


def if_file_exists_do_orElse(file_name):
        if not os.path.isfile(file_name):
                with open(file_name, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(["Date","Time", "Battery", "Status"])
        else:
                filesize = os.path.getsize(file_name)
                if filesize == 0:
                        with open(file_name, 'a', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(["Date","Time", "Battery", "Status"])

def get_battery():
        battery = str(bs4.BeautifulSoup(requests.get('http://jiofi.local.html/#').text,features="html.parser").select('#batterylevel')[0])
        battery = int(re.findall('value="([0-9]+)%"', battery)[0])
        return battery

def get_battery_status():
        battery_status_str = str(bs4.BeautifulSoup(requests.get('http://jiofi.local.html/#').text,features="html.parser").select('#batterystatus')[0])
        battery_status = re.findall('value="([a-zA-Z]+)"', battery_status_str)
        return battery_status[0]

def append_data_to_file(file_name, date, time, battery, status):
        with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([date, time, battery , status])
        
        
if __name__ == "__main__":
        toast = win10toast.ToastNotifier()
        today = date.today()

        file_name = 'analytics\\wifi_battery_analytics.csv'
        if_file_exists_do_orElse(file_name)
        
        while(1):
                battery = 0
                try:
                        battery = get_battery()
                        battery_status = get_battery_status()
                except:
                        toast.show_toast("Wifi Not connected","Not on jioFi.",duration = 20,icon_path = r"\Users\admin\Pictures\wifi.ico")
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                print("Time =", current_time, " Wifi battery = ", str(battery) + "%  ", battery_status)

                append_data_to_file(file_name, today.strftime("%b-%d-%Y"), current_time, str(battery) + "%", battery_status)
                
                extremely_low_battery_msg = "Few minutes of battery left.\nBattery Left: " + str(battery) + "%" + "\nStatus: " + battery_status
                medium_battery_msg = "Wifi battery is about to black out.\nBattery Left: " + str(battery) + "%" + "\nStatus: " + battery_status
                battery_full_msg = "Battery Level: " + str(battery) + "%" + "\nStatus: " + battery_status
                
                if(battery <= 10):
                        toast.show_toast("WARNING: Battery LOW",extremely_low_battery_msg,duration = 20,icon_path = r"assets\extremely_low_battery.ico")
                elif(battery <= 30):
                        toast.show_toast("Wifi battery below 30%",medium_battery_msg,duration = 20,icon_path =r"assets\battery-low-medium.ico")
                elif(battery <= 50):
                        toast.show_toast("Wifi battery near to half",battery_full_msg,duration = 20, icon_path= r"assets\battery-half.ico")
                elif(battery >= 96):
                        toast.show_toast("Wifi battery FULL",battery_full_msg,duration = 20, icon_path= r"assets\battery-full.ico")
                elif(battery >= 90):
                        toast.show_toast("Wifi battery Almost full",battery_full_msg,duration = 20, icon_path= r"assets\battery-full.ico")
                time.sleep(2700)
