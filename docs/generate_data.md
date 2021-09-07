# Training data generation
The `generate_data.py` script generates training data for pedestrian detection models using the ESI Pro-SiVIC simulator.

Currently it is only possible to generate data from four different scenarios in a single pre-defined scene. The four scenarios are:

1. Pedestrian crossing from the left
2. Pedestrian crossing from the right
3. Pedestrian walking towards car
3. Pedestrian walking away from car

## Requirements

* ESI Pro-SiVIC.
* Pro-SiVIC python DDS install/Release folder in PATH and PYTHONPATH according to DDS instructions.
* Python 3.7 (Pro-SiVIC DDS requirement).
* Only tested on Windows 10.

## Quickstart

```
$ git clone https://github.com/RI-SE/smirk
cd smirk
```

Install dependencies:

```
# Using poetry
poetry install

# Using pip (requirements generated from poetry.lock)
$ pip install -r requirements.txt
```

Copy the `simple_aeb.script` scenario in `prosivic_scripts` to the Pro-SiVIC scripts folder e.g. `"C:\Users\Yourname\Pro-SiVIC\My project\scripts"`.

Start Pro-SiVIC, then run the data generation:

```
$ python src/generate_data.py
```

Captured camera images and pedestrian pixel masks will be saved to: `C:\Users\Yourname\Pro-SiVIC\My project\sensors\[date-and-time]\[simulation-id]`.

## Configuration
It is possible to customize the data generation by passing a configuration file:

```
$ python generate_data.py -h

usage: generate_data.py [-h] [-c CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        path to config file
```

The default example configuration file is available in the `examples` folder:

```
$ cat examples/data-generation-config.yaml

scenarios:
  -
    type: 'left'
    pedestrian:
      speeds: [2]
      angles: "${range:30,151,20}"
      distances_from_car: "${range:10,151,10}"
      distances_from_road: [2]
  -
    type: 'right'
    pedestrian:
      speeds: [2]
      angles: "${range:30,151,20}"
      distances_from_car: "${range:10,151,10}"
      distances_from_road: [2]
  -
    type: 'towards'
    pedestrian:
      speeds: [2]
      distances_from_car: [150]
      offsets_from_road_center:  "${range:-3,4,1}"
      max_walking_distance: 140
  -
    type: 'away'
    pedestrian:
      speeds: [2]
      distances_from_car: [10]
      offsets_from_road_center:  "${range:-3,4,1}"
      max_walking_distance: 140
```

The `scenarios` list defines the different scenario configurations to run. For each scenario type, the Cartesian product av all parameter values will be used to generate the data. The following scenario types are available:

* `type` - Scenario type, can be one of the following values:
  * left - Pedestrian walking from the left side of the road.
  * right - Pedestrian walking from the right side of the road.
  * towards - Pedestrian walking towards the car.
  * away - Pedestrian walking away from the car.

The left/right scenarios terminate once the pedestrian has crossed the road. The towards/away scenarios terminate after the specified walking distance.

The following parameters are common for all scenarios:

* `speeds` (List[integer]) - Pedestrian speed in m/s.
* `distances_from_car` (List[integer]) - Starting distance from car in meters.
* `max_walking_distance`: The distance in meters the pedestrian will walk. (Optional for left/right scenarios).

The left/right scenarios have additional parameters:

* `angles` (List[integer]) - Walking angles in degrees where 0 represents walking parallel with the road away from the car, 90 represents walking perpendicular to the road, and 180 represents walking parallel with the road towards the car.
* `distance_from_road` (integer) - Starting offset from the edge of the road in meters.

The towards/away scenarios have additional parameters:

* `offsets_from_road_center` (List[integer]) - Offset in meters from the center of the road. Positive values offests left, negative values offset right.

Apart from standard yaml syntax, it is possible to use `"${range:start,stop,step}"` to generate a list of values starting at `start`, incrementing by `step` up to but not including `stop`.
