# Training data generation
The `generate_data.py` script generates training data for pedestrian detection models using the ESI Pro-SiVIC simulator.

Currently it is only possible to generate data from four different scenarios in a single pre-defined scene. The four scenarios are:

1. Object crossing from the left
2. Object crossing from the right
3. Object walking towards car
3. Object walking away from car

Various scenario parameters can be specified as described in the configuration section below.

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
  - type: left
    pedestrian:
      appearance:
        - male_business
        - male_casual
        - male_construction
        - female_business
        - female_casual
        - child
      speeds: [2]
      angles: [90]
      distances_from_car: [50]
      distances_from_road: [2]
  - type: right
    pedestrian:
      appearance: female_business
      speeds: [2]
      angles: "${range:30,151,20}"
      distances_from_car: "${range:10,151,10}"
      distances_from_road: [2]
  - type: towards
    max_travel_distance: 140
    pedestrian:
      appearance: child
      speeds: [2]
      distances_from_car: [150]
      offsets_from_road_center: "${range:-3,4,1}"
  - type: away
    max_travel_distance: 140
    pedestrian:
      appearance: male_business
      speeds: [2]
      distances_from_car: [10]
      offsets_from_road_center: "${range:-3,4,1}"
  - type: right
    object:
      type:
        - box
        - cone
        - pyramid
        - sphere
      speeds: [1, 2]
      distances_from_car: "${range:10,151,10}"
      distances_from_road: [2]
```

Apart from standard yaml syntax, it is possible to use `"${range:start,stop,step}"` to generate a list of values starting at `start`, incrementing by `step` up to but not including `stop`.

The `scenarios` list defines the different scenario configurations to run. For each scenario type, the Cartesian product av all parameter values will be used to generate the data. The following scenario types are available:

* `type` - Scenario type, can be one of the following values:
  * `left` - Object moving from the left side of the road.
  * `right` - Object moving from the right side of the road.
  * `towards` - Object moving towards the car.
  * `away` - Object moving away from the car.

The left/right scenarios terminate once the object has crossed the road. The towards/away scenarios terminate after the specified distance.

There are two main types of objects that can cross the road `pedestrian` and `obejct`.

### Object
Object are limited to crossing the road in a straight line, perpendicular to the road, from left or right.

An object scenario is configured using the following parameters:

- `type` (string): Scenario type, can be one of `left, right`
  * `object`: 
    * `type` (string or List[string]): Appearance of object, can be one of `box`, `cone`, `pyramid`, `sphere`
    * `speeds` (List[number]): Object speed in m/s
    * `distances_from_car` (List[number]): Starting distance from car in meters.
    * `distances_from_road` (List[number]): Starting offset from the edge of the road in meters.

### Pedestrian
A pedestrian can either cross the road from left or right at different angles, or walk in a straight line towards or away from the car.

A left/right scenario is configured using the following parameters:

- `type` (string): Scenario type, can be one of `left, right`
  * `pedestrian`:
    * `appearance` (string or List[string]): Appearance of pedestrian, one of `male_business`, `male_casual`, `male_construction`, `female_business`, `female_casual`, `child`.
    * `speeds` (List[number]): Object speed in m/s
    * `distances_from_car` (List[number]): Starting distance from car in meters.
    * `distances_from_road` (List[number]): Starting offset from the edge of the road in meters.
    * `angles` (List[number]): Walking angle in degrees where 0 represents walking parallel with the road away from the car, 90 represents walking perpendicular to the road, and 180 represents walking parallel with the road towards the car.

A towards/away scenario is configured using the following parameters:

- `type` (string): Scenario type, can be one of `towards, away`
  * `max_travel_distance` (number): The distance in meters the to walk.
  * `pedestrian`:
    * `appearance` (string or List[string]): Appearance of pedestrian, one of `male_business`, `male_casual`, `male_construction`, `female_business`, `female_casual`, `child`.
    * `speeds` (List[number]): Object speed in m/s
    * `distances_from_car` (List[number]): Starting distance from car in meters.
    * `offsets_from_road_center` (List[number]): Offset in meters from the center of the road. Positive values offsets left, negative values offset right.
