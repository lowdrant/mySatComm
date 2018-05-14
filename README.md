# mySatComm
Homebrew groundstation for receiving data from satellites


## Project Breakdown
* Antenna Design
  * Linearly Polarized Yagi Antenna
  * Currently 3-element implementing a basic dipole antenna
* Az-El Controller
  * 2 servo motors control antenna orientation
  * Using Arduino and GPredict to actuate
* Data Reception
   * Using the NooElec NESDR for a radio
   * Using GNURadio to implement the needed DSP
* Decoding
   * TBD

## Software Used
SolidWorks
- Mechanical design software by Dassault Systems
- Not free; requires a license

Arduino IDE
- Used to implement motor controller
- Open source

GNURadio
- Software-Defined Radio programming package
- Free to use

## Folder Guide
* Mechanical
  - Contains all CAD designs
* MCU
   - Code for antenna orientation controller
* SDR
  - Code for radio interfacing