#!/bin/bash

source /opt/wibed_env/bin/activate
pkill --signal SIGKILL python
rm -rf /opt/wibed-controller/wibed.db*
python /opt/wibe-controller/initdb.py
#( . /opt/wibed_env/bin/activate ; python /opt/wibed-controller/tornadoserver.py ) &
python /opt/wibed-controller/tornadoserver.py

exit 0
