# wibed-controller
This repository contains the source code of the WiBed central controller.

## The WiBed project
The WiBed project is aimed at designing, implementing and providing a wireless testbed based on
off-the-shelf IEEE802.11-capable routers to allow for experimenting on a mesh network of several
tenths of nodes and with significant number of hops in a realistic environment.

## The Wibed controller
The WiBed controller is the central application that manages a deployment of the WiBed testbed.
It controls the routers participating on the testbed, allowing to manage and configure them, and 
also handles the management of experiments performed in the mesh network.

### System requirements
The controller can be installed on a bare metal machine or a virtual host. It is designed to be run on
devices with constrained resources, like an Alix 2D2. These are the recommended minimum hardware and software requirements:
* 1 GHz CPU core
* 512 MB free RAM
* 2 GB free disk space
* 1 network interface
* Debian 7.1 OS or later
* Python 2.7

### Installation
This tiny guide assumes you fulfill the previous hardware requirements and that you have a fresh Debian OS where you
can download and install more packages. The installation is performed by the non-administrative user *wibed*; you can
use the username you like the best.

* Install required tools: `build-essential` and `git`:
```
sudo aptitude install build-essential git
```
* Install required packages: `python2.7`, `python-pip` and `python-virtualenv`:
```
sudo aptitude install python2.7 python-pip python-virtualenv
```
* Clone the `wibed-controller` repository and checkout the `local` branch:
```
cd
git clone http://git.confine-project.eu/wibed/wibed-controller.git
cd wibed-controller
git checkout -b local origin/local
```
* Initialize the python virtual environment:
```
virtualenv wibed_env
```
* Install the remaining python packages in `requirements.txt` using `pip`:
```
wibed_env/bin/pip2.7 install -r requirements.txt
```
* Initialize the database:
```
wibed_env/bin/python2.7 initdb.py
```
* Start the web server in the background:
```
wibed_env/bin/python2.7 tornadoserver.py  > /dev/null 2>&1 &
```
* Add an init.d script to start the server on boot:
```
[ToDo]
```

The WiBed controller HTTP server is listening on port 8080.
