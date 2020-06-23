# mySatComm
Homebrew groundstation for receiving data from satellites. Servos are controlled via Raspberry Pi; DSP is handled through the GNU Radio and GPredict. Go [here](mechanical/stl) to see STL models in GitHub.

## Project Overview
This is a farm-to-table amateur radio project composed of 3 major subprojects:

* Mechanical Design
	* Antenna Rig
	* Orientation Controller
* Command & Control Software
	* Servomotor low-level control
	* GPredict command interface
	* Rotator trajectory generation
* Digital Signal Processing
	* Radio demodulation and doppler shifting
	* Information decoding

## Installation
Clone this repo to your Raspberry Pi and run [install.sh](installers/install.sh). All Python dependencies will be installed in a virtual environment at `$HOME/.satcomm`. Additionally, 

To uninstall, run the corresponding [uninstall.sh](installers/uninstall.sh) script.

On your PC, install [GPredict](http://gpredict.oz9aec.net/), [GNU Radio](https://www.gnuradio.org/), and download the [SDR folder](sdr).

## Using the programs
1. Create a GPredict module tracking some satellites of interest. Be sure to look at the [manual](documentation/gpredict_manual.PDF) and [website](http://gpredict.oz9aec.net/).

2. Configure GPredict to interface with your Raspberry Pi as a networked rotator (you'll need its IP address).

3. Configue GPredict to work with your SDR. If you don't have a go-to, I recommend using the [NooElec NESDR Mini 2](https://www.nooelec.com/store/sdr/sdr-receivers/nesdr-mini2-rtl2832u-r820t2.html).

4. Wait for a satellite to pass within range, then activate GPredict radio and rotator control programs and run `./run.sh` on your Pi.

5. Watch it go!

## Software/Retailer Links
* [GPredict](http://gpredict.oz9aec.net/) - Satellite tracking and antenna actuation software
* [PiGPIO](http://abyz.me.uk/rpi/pigpio/index.html) - Provides hardware-timed GPIO control on Raspberry Pi
* [Raspberry Pi](https://www.raspberrypi.org/) - Hobbyist-oriented single-board computer
* [SolidWorks](https://www.solidworks.com/) - CAD software
* [SainSmart](https://www.com.sainsmart) - Robotic components manufacturer

## Project Subfolders
* [Antenna Design](mechanical/antenna)
* [Az-El Controller](mechanical/azel_controller)
* [Control Software](cmd-n-ctl/)
* [Data Reception](sdr/rx)
* [Data Decoding](sdr/decoder)

### Mechanical Quick Reference
* [GitHub-viewable Models](mechanical/stl)
* [Antenna Rotator](mechanical/drawings/controller.PDF)
* [Base Dipole](mechanical/drawings/dipole.PDF)
* [Bill of Materials](BOM.txt)

### Software Quick Reference
* [HamLib (GPredict Command Library)](http://hamlib.sourceforge.net/manuals/1.2.15/index.html)
* [HamLib on RPi](https://kb9mwr.blogspot.com/2013/04/raspberry-pi-web-based-rig-control.html)
* [Servo Characterization](cmd-n-ctl/servo-tests)

## Design Decisions
### Antenna
* 3-element linearly polarized yagi antenna
	* Directionality recommended for satellite reception
	* Circular polarization is annoying (for me) to get right
* Homebrew dipole antenna base made from PVC, AWG14 wire, and screws
	* COTS parts increase accessiblity and homebrew aesthetic
	* Thicker wire chosen for increased rigidity

### Controller
* Custom housing
	* Convenient mount point for rotator
	* Minimizes wiring connecting Pi and servos
	* 3D printed for rapid prototyping
* Solderboard Pi shield
	* More reliable wiring of servo battery power
	* Faster connect/disconnect of servos from Pi

### Software
* GPredict
	* Open source satellite tracking software
	* Computes necessary antenna orientation automatically
	* Sends antenna orientation commands over TCP/IP
	* [Manual here](documentation/gpredict_manual.PDF)
* PiGPIO
	* Provides almost-hardware-timed PWM (important for servo control)
	* PWM less noisy and more reliable than RPi-GPIO or wiringPi
	* Simple Python interface

## SDR Sources & Acknowledgements
* Wolfgang Nagele for his [GRC Gpredict Doppler shift correction block](https://github.com/wnagele/gr-gpredict-doppler)
* Alexandru Csete for [this tutorial for an APT decoder in GRC](http://oz9aec.net/radios/gnu-radio/simple-apt-decoder-prototype)

## Author
Marion Anderson - [lowdrant](https://github.com/lowdrant)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details
