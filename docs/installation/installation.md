# Installation

> Assuming raspberry pi 4 running some debian based distro

## step 1 download and install
```bash
# Update the system
sudo apt update -y && sudo apt upgrade
#install git, python and python package mananger
sudo apt install git python3 python3-pip
# clone the repo
git clone https://github.com/pavelnoen94/tube-slide
cd tube-slide
# install required packages
pip3 install -r requirements.txt

```
## step 2 configure
- replace ip address to the mosquitto broker in the configuration file `white_slide.ini`
- make sure mossquitto broker is started with websockets. Use mosquitto.conf file in the repo

## step 3 

