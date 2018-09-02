import requests
from git import Repo
import shutil
import time
import os
import subprocess
from subprocess import call

def update(ver):
    url = 'https://api.github.com/repos/cyber-Ahn/tgn_smart_home/contents/version.txt'
    page = requests.get(url)
    read_data = page.text
    split_data = read_data.split('sha')
    read_data = split_data[1]
    split_data = read_data.split('size')
    read_data = split_data[0]
    split_data = read_data.split(':"')
    read_data = split_data[1]
    split_data = read_data.split('",')
    read_data = split_data[0]
    if read_data == ver:
        return("Your software is up to date")
    else:
        Repo.clone_from("https://github.com/cyber-Ahn/tgn_smart_home.git", "/home/pi/Desktop/update")
        shutil.move("/home/pi/Desktop/update/main_gui.py", "/home/pi/tgn_smart_home/main_gui.py")
        shutil.move("/home/pi/Desktop/update/version.txt", "/home/pi/tgn_smart_home/version.txt")
        shutil.move("/home/pi/Desktop/update/setup.sh", "/home/pi/tgn_smart_home/setup.sh")
        shutil.move("/home/pi/Desktop/update/remove.sh", "/home/pi/tgn_smart_home/remove.sh")
        shutil.rmtree('/home/pi/tgn_smart_home/icons', ignore_errors=True)
        shutil.rmtree('/home/pi/tgn_smart_home/language', ignore_errors=True)
        shutil.rmtree('/home/pi/tgn_smart_home/libs', ignore_errors=True)
        shutil.move("/home/pi/Desktop/update/icons", "/home/pi/tgn_smart_home/icons")
        shutil.move("/home/pi/Desktop/update/language", "/home/pi/tgn_smart_home/language")
        shutil.move("/home/pi/Desktop/update/libs", "/home/pi/tgn_smart_home/libs")
        shutil.move("/home/pi/Desktop/update/update.py", "/home/pi/tgn_smart_home/update.py")
        shutil.move("/home/pi/Desktop/update/setup_files/tgnLIB.py", "/usr/local/lib/python3.5/dist-packages/tgnLIB.py")
        shutil.rmtree('/home/pi/Desktop/update', ignore_errors=True)
        setn = "lxterminal -e python3 /home/pi/tgn_smart_home/libs/settings.py update"
	os.system(setn)
        return("New version available SHA:"+read_data+"\nUpdate successful")
print(update("fe804e59218a9228ebad3a37aa44fccbc9a96287"))
time.sleep(6)
