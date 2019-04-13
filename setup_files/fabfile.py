#sudo pip3 install fabric3
from fabric.api import *
import time

# user@host list
env.hosts = [
    'pi@192.168.0.94',
    'pi@192.168.0.95',
    'pi@192.168.0.98',
]

# Set password for each host:port pair
for host in env.hosts:
    env.passwords[host + ':22'] = 'rhjk0096'

@parallel
def reboot():
    # reboot hosts
    sudo('shutdown -r now')

@parallel
def shutdown():
    # shutdown hosts
    sudo('shutdown -h now')

@parallel
def update():
    # apt update hosts
    sudo('apt-get update')
    sudo('apt-get dist-upgrade -y')
