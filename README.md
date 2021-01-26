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
