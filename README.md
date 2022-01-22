# OBS-Tally

OBS Tally-Lights via OBS-Websockets, Python for SBCs like Raspberry Pi

THIS WAS MY FIRST BIG PYTHON PROJECT... RE-Write is undergoing.

## Description

So you want Tallys for your OBS? Okay. Grab your Raspberry Pi, 8-Channel Relais Card, some Lights, a PSU for the Lights and some Duct-Tapes and let's go. How you design the Hardware is up to you! This Script sets GPIO-Pins to LOW or HIGH, based on the Scene-State in OBS.


## Installation

```bash
git clone <repo-url>
cd repo-folder
pip install -r requirements.txt
```


## Usage
 run matching Python file

For LEDs directly on GPIO:
```bash
python obstally.py
```
or

For 8-Chanel Relais Cards:
```bash
python obstally_inverted.py
```

## Access the Webinterface
Spin-Up Webserver with PHP

Put index.php in documents-root (e.g. /var/www/html)

In index.php change tally.xml-path to match the actual path

Go to `http://127.0.0.1:80`, profit!


## Roadmap

### Done ✓

- [x] Make Tally works according to OBS-Scenes

### In Progress
- [ ] Rewrite everything

### Todo

- [ ] Create new 3D-Models for Housing of Tally
- [ ] Create new 3D-Models for Housing of Tally-Master / Raspi

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

HTBAH-Internals: Contact #technik-grafik in Slack

## License
[Apache 2.0](https://choosealicense.com/licenses/apache-2.0/)
