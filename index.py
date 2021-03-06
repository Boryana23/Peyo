from flask import Flask, request, render_template, jsonify
import RPi.GPIO as GPIO
import serial
from os import system
from serial1 import read_serial
from buttons import read_pin
from volume_control import volume_control
import time
from spotify import spotify_off, spotify_on
from radios import radio_on, radio_off
from usb import play_usb
import multiprocessing

app = Flask(__name__)

NAMES=(
    "Radio 1 Rock",
    "Z-Rock",
)
STREAMS=(
    "http://149.13.0.81/radio1rock.ogg",
    "http://46.10.150.243:80/z-rock.mp3",
)

softwareOn = 0;
playing = 0;

radio = 0;
spotify = 0;
usb = 0;


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/radio', methods = ['POST', 'GET'])
def playRadio():
	if request.method == 'POST':
		radio = request.form['radio']
		if(softwareOn):
			print("radio is now playing")
		return jsonify({'softwareOn' : softwareOn})
	return '', 200;

@app.route('/spotify', methods = ['POST', 'GET'])
def playSpotify():
	if request.method == 'POST':
		spotify = request.form['spotify']
		if softwareOn:
			if spotify:
				spotify_off()
			else:
				spotify_on()
			spotify = 1 - spotify
			print("spotify is now playing")
		return jsonify({'softwareOn' : softwareOn})
	return '', 200;

@app.route('/usb', methods  =['POST', 'GET'])
def playUSB():
	if request.method == 'POST':
		usb = request.form['usb']
		if softwareOn:
			if usb:
				radio_off()
				print("usb music is now off")
			else:
				play_usb()
				print("usb music is now on")
			usb = 1 - usb
		return jsonify({'softwareOn' : softwareOn})
	return '', 200;

@app.route('/mode', methods = ['POST', 'GET'])
def controlBySoftware():
	if request.method == 'POST':
		global softwareOn;
		state = request.form['toggleBar']
		if state == "true":
			softwareOn = 1
			print("softwareOn")
		elif state == "false":
			softwareOn = 0
			print("softwareOff")
	return '', 200;

@app.route('/volume', methods = ['POST', 'GET'])
def controlVolume():
	if request.method == 'POST':
		volume = request.form['myRange']
		if softwareOn:
			if radio:
				radio_off()
			else:
				radio_on(STREAM)
			radio = 1 - radio
			print('volume changed to ' + volume)
		return jsonify({'softwareOn' : softwareOn})
	return '', 200;

@app.route('/play', methods = ['POST', 'GET'])
def controlStartStop():
	if request.method == 'POST':
		state = request.form['play']
		if softwareOn:
			global playing;
			playing = 1 - playing;
			print('state changed to ' + str(playing))
		return jsonify({'softwareOn' : softwareOn})
	return '', 200;

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
