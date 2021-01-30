# Skating Reservations
Using selenium, interact with the Toronto eFun platform to quickly register a household for a skating session at a specific part at a specific start time.

## Usage
Create a `env.py` file with:
```
clientNumber=<insert number>
familyNumber=<insert number>
park="Alexandra Park (Bathurst/Dundas)"
time="9:00PM"
```

Run the program using:
```
python3 main.py

Options:
--headless  (headless operation, no browser GUI)
--chrome    (chrome operation)
```

## GCP
Debian 10, f1-microVM, 10GB storage

Installation:
```
sudo apt-get install python3-pip git wget firefox-esr
pip3 install selenium
```

Install geckodriver:
```
wget https://github.com/mozilla/geckodriver/releases/download/v0.29.0/geckodriver-v0.29.0-linux32.tar.gz
tar -xf geckodriver-v0.29.0-linux32.tar.gz
sudo mv geckodriver /usr/bin/geckodriver
```

## Raspberry Pi
[ChromeDriver installation for Raspberry Pi](https://ivanderevianko.com/2020/01/selenium-chromedriver-for-raspberrypi)
```
sudo apt-get install chromium-browser chromium-chromedriver
```

[Adjust SSH timeout for the Pi](https://www.digitalocean.com/community/questions/how-to-increase-ssh-connection-timeout)

## CRON Job
[Setting up a CRON Job](https://vitux.com/how-to-setup-a-cron-job-in-debian-10/)

Run at 12:50 GMT (7:50 ET) on Tues, Thurs, Fri, Sat, Sun during January, February, March
```
50 12 * 1,2,3 0,2,4,5,6 /usr/bin/python3 /home/USERNAME/skating_reservation/morning_script.py >> /home/USERNAME/skating_reservation/log.log 2>&1
```
