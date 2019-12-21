<h1>
	Cleaning-Bot
	<img src="rpi.jpg" width="96" height="96" align="center">
</h1>

A microcontroller project to create a bot, which uses image processing, and machine learning to detect trash on the road, and clean it.
(Contributions encouraged!)

## About The Project

Current status: R-pi image processing using OpenCV to detect a line using centroid method. Aggregation complete.

## Architecture
Commit 1. Arduino connected to 2 motors and 1 colour sensor
Commit 2. Adding readme
Commit 3. OpenCV program (boss.py) to detect and follow line
Commit 4. New program (program.py) for detection using centroid method

## Usage
Detect trash on the road, and clean it


### Hardware usage
1. R-pi 3 (3.3v)
2. Motor driver L298 (5v)
3. Camera
4. 4 motors - 4 wheels (9v)
5. Chasis
6. Rechargable 9V batteries


## Current TODO

Mounting and Testing 
program.py final python file for basic line following using opencv, imperfect
