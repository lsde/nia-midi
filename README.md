# nia-midi
This application translates data from OCZ NIA to MIDI.

It sends-out the "brain-fingers" as MIDI notes via the first available MIDI device.

Based on https://github.com/kevinmershon/pynia

## Prerequities
```
# apt install python-virtualenv python3-virtualenv rtmidi xvfb
# cp 47-ocz-nia.rules /etc/udev/rules.d/`
# udevadm control --reload-rules
# virtualenv -p python3 venv
# venv/bin/pip install -r requirements.txt
```

## Running
````
# ./start.sh
````
