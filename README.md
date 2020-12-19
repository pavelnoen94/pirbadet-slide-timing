# tube-slide
Timing system for tube slides in water parks


```bash
git clone
cd tube-slide
virtualenv -p ($which python3) venv
source venv/bin/activate
pip3 install -r requirements

# install mosquitto
sudo apt install mosquitto
# stop mosquitto
sudo systemctl stop mosquitto.service
# remove the default configuration file
sudo rm /etc/mosquitto/mosquitto.conf
# create a symbolic link to configuration file in the repository
sudo ln -s mosquitto.conf /etc/mosquitto/.
# start the mosquitto service. It will start on boot from now on.
systemctl status mosquitto.service
# start http server for the scoreboard
python3 -m http.server scoreboard/src/ > /dev/null & # use htop or something to kill it later if needed.
# start the timer program
python3 timer/src/main.py
# pray that everything works
```