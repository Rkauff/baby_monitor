'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

Created on Sat May 10 09:11:13 2019

@author: Ryan
'''

def main():

    import RPi.GPIO as GPIO
    import time
    import os
    import glob
    from twilio.rest import Client
     
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
     
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'

    account_sid = "your account sid"
    auth_token = "your auth token"

    client = Client(account_sid, auth_token)

    #GPIO Setup
    temp_channel = 4
    temp = GPIO.setmode(GPIO.BCM)
    temp = GPIO.setup(temp_channel, GPIO.IN)


    #Functions 
    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

     
    def read_temp():
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            temp_f = round(temp_f)
            return temp_f


    def warm_message():
        warm_text = client.messages.create(
            to="+16307889299",
            from_="+16305282150",
            body="It's currently " + str(read_temp()) + " degrees in my crib, how about " \
            "turning up the air conditioning or opening a window?")

    def cold_message():
        cold_text = client.messages.create(
            to="+16307889299",
            from_="+16305282150",
            body="It's currently " + str(read_temp()) + " degrees in my crib, how about " \
            "turning the heat up a little bit?")
        
       
    while True:
        if read_temp() > 82:
            warm_message()
        if read_temp() < 60:
            cold_message()
        time.sleep(300)
        
main()
