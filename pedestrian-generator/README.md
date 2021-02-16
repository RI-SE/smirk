# Pedestrian generator
Generates training data for pedestrian detection models using the ESI Pro-SiVIC simulator.

## Requirements

* ESI Pro-SiVIC.
* Pro-SiVIC python DDS install/Release folder in PATH and PYTHONPATH according to DDS instructions.
* Python 3.7 (Pro-SiVIC DDS requirement).
* Only tested on Windows 10.

## Quick start

```
$ git clone https://github.com/RI-SE/smirk
cd smirk\pedestrian-generator
```

If python DDS is not already set up, add DDS install folder to path e.g. by running the provided powershell script with admin privileges: 

```
$ .\util\set-prosivic-env-vars.ps1 C:\path\to\DDS\install\Release
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Copy the scenario in prosivic_scenes to your Pro-SiVIC scripts folder.


```
copy prosivic_scenes\scenario1.script "C:\Users\Yourname\Pro-SiVIC\My project\scripts"
```

Start Pro-SiVIC, then run the scenario:

```
$ python src\cli.py
```

Captured camera images and pedestrian pixel masks will be saved to:

```
C:\Users\Yourname\Pro-SiVIC\My project\sensors\[date-and-time]\[simulation-id]
```

## Configuration
Scenario configurations are specified in `scenario-config.yaml`.

Not all configuration values are currently supported, and the format will change in the future.

Currently only a very limited set of scenarios are supported. The following restrictions apply:

* The only possible pedestrian action is walking from the left and right of the road, with some additional configuration options such as walking angle, distance and speed.
* The Pro-SiVIC scenario script must be set up in a very specific (not documented) way.
