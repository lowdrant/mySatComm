# mySatComm
Homebrew groundstation for receiving data from satellites

## Project Breakdown
* Antenna Design
  * Linearly Polarized Yagi Antenna
    * Currently 3-element, basic dipole design, 1 driven element
* Az-El Controller
  * 2 servo motors connected to the antenna
  * Using Arduino and GPredict to actuate
* Data Reception
   * Using the NooElec NESDR software-defined radio to pull in the data
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