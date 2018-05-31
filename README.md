# mySatComm
Homebrew groundstation for receiving data from satellites

## Project Overview
This is a farm-to-table amateur radio project composed of 3 major subprojects:

* Mechanical Design
	* Antenna Rig 
	* Orientation Controller
* Command & Control Software
	* Servomotor control
	* GPredict command interfacing
* Digital Signal Processing
	* Radio demodulation and doppler shifting
	* Information decoding


### Project Subfolders
* [Antenna Design](mechanical/antenna)
* [Az-El Controller](mechanical/azel_controller)
* [Control Software](cmd-n-ctl/)
* [Data Reception](sdr/rx)
* [Data Decoding](sdr/decoder)

### Mechanical Quick Reference
* [Controller](mechanical/drawings/controller.PDF)
* [Dipole ](mechanical/drawings/dipole.PDF)
* [Materials](BOM.txt)

### Software Quick Reference
* [PiGPIO (Servo PWM Library)](http://abyz.me.uk/rpi/pigpio/pigpiod.html)
* [HamLib (GPredict Command Library)](http://hamlib.sourceforge.net/manuals/1.2.15/index.html)
* [HamLib on RPi](https://kb9mwr.blogspot.com/2013/04/raspberry-pi-web-based-rig-control.html)
* [Servo Characterization](cmd-n-ctl/Sweep/Sweep.ino)

## Design Decisions
### Antenna
* 3-element linearly polarized yagi antenna
	* Directionality recommended for satellite reception
	* Circular polarization is difficult (for me) to get right
* Homebrew dipole antenna base made from PVC and coat hangers
	* Coat hanger antennas are aesthetic
	* Cheap COTS parts Increase accessiblity
	
### Controller
* Custom-made servo brackets (sized for [SainSmart SR319](https://www.sainsmart.com/products/copy-of-all-purpose-digital-servo-sr318?nosto=customers-also-bought)) 
	* Had two of those servos on-hand
	* SainSmart doesn't really sell  individual brackets  ($$)
* Custom platform stand
	* I don't own anything I could bolt this to permanently (student lyfe)
	* I don't want to buy a stand when I can 3D print one for free

### Software
* GPredict
	* Free, real-time satellite tracking
	* Computes antenna orientation
	* Can send antenna orientation commands over TCP/IP
	* [Manual here](documentation/gpredict_manual.PDF)
* PiGPIO
	* Provides hardware-time PWM (HUGE for servo control)
	* PWM way less noisy and more reliable than RPi-GPIO or wiringPi
	* Both Python and C interfaces

## Software/Retailer Links
* [GPredict](http://gpredict.oz9aec.net/) - Satellite tracking and antenna actuation software
* [PiGPIO](http://abyz.me.uk/rpi/pigpio/index.html) - Provides hardware-timed GPIO control on Raspberry Pi
* [Raspberry Pi](https://www.raspberrypi.org/) - Hobbyist-oriented single-board computer
* [SolidWorks](https://www.solidworks.com/) - CAD software 
* [SainSmart](https://www.com.sainsmart) - Robotic components manufacturer

## Author
Marion Anderson - [lmander42](https://github.com/lmander42)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details