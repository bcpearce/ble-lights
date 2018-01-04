# BLE-Lights

This application is for controlling a SUPERNIGHT Bluetooth LED Controller using a web application hosted locally on a bluetooth compatible system.

This has been tested running on stock Raspbian 8.0 "jessie" on a Raspberry Pi 2 using a USB bluetooth dongle.

## Installation
Clone the repository and run `pip install -r requirements.txt` from the project root directory.  Run the `app.py` file 

## Running
Launch the webapp by running `python webapp.py <host> <port>` or `python webapp.py` to run on localhost on the default port.

Navigate to the web address using any web browser to control the LED Controller. 
