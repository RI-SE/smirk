# System Requirements Specification v0.2

Revision History
<table>
<tr>
<th>Markus Borg</th>
<th>2021-05-13</th>
<th>Initialized using IEEE SRS template.</th>
<th>0.1</th>
</tr>
<tr>
<td>Markus Borg</td>
<td>WIP</td>
<td>Initial version to discuss at AMLAS workshop.</td>
<td>0.2</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the system requirements for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

## 1.1 Purpose ##
SMIRK assists the driver on country roads by performing emergency braking in the case of an imminent collision with a pedestrian. The level of automation offered by SMIRK corresponds to SAE Level 1 - Driver Assistance, i.e., “the driving mode-specific execution by a driver assistance system of either steering or acceleration/deceleration. SMIRK is developed with a focus on evolvability, thus future versions might include steering and thus comply with SAE Level 2.

This document provides the foundation for the SMIRK minimum viable product (MVP).

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS Guidance on the Assurance of Machine Learning in Autonomous Systems
- ML: Machine Learning

## 1.4 Intended Audience and Reading Suggestions ##
## 1.5 Product Scope ##
## 1.6 References ##
- Nair, De La Vara, Sabetzadeh, and Briand. [An extended systematic literature review on provision of evidence for safety certification](https://www.sciencedirect.com/science/article/abs/pii/S0950584914000603). *Information and Software Technology*, 56(7), 689-717, 2014.
- Picardi,,Paterson, Hawkins, Calinescu, and Habli. [Assurance Argument Patterns and Processes for Machine Learning in Safety-Related Systems](http://ceur-ws.org/Vol-2560/paper17.pdf). In *Proceedings of the Workshop on Artificial Intelligence Safety (SafeAI 2020)*, pp. 23-30, 2020.
- E. Thorn, S. Kimmel, and M. Chaka. [A Framework for Automated Driving System Testable Cases and Scenarios](https://trid.trb.org/view/1574670), Technical Report DOT HS 812 623, National Highway Traffic Safety Administration, 2018.

# 2 System Description [C] <a name="system_reqts"></a>
## 2.1 Product Perspective ##
## 2.2 Product Functions ##
## 2.3 External Interface Requirements ##

# 3 System Safety Requirements [A] <a name="system_safety_reqts"></a>

# 4 Operational Design Domain [B] <a name="odd"></a>
This section specifies the SMIRK operational design domain (ODD). The ODD specification is based on the taxonomy developed by NHTSA [2]. Note that the ODD is deliberately restricted to allow rapid prototyping of a SMIRK MVP.

## 4.1 Physical Infrastructure
<table>
<thead>
  <tr>
    <th colspan="2">Roadway Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Divided highway</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Undivided highway</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Arterial</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Urban</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Rural</td>
    <td>Y (open green fields)</td>
  </tr>
  <tr>
    <td>Parking (surface lots, structures, private/public)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Bridges</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Multi-lane/single lane</td>
    <td>Single lane</td>
  </tr>
  <tr>
    <td>Managed lanes (HOV, HOT, etc.)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>On-off ramps</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Emergency evacuation routes</td>
    <td>N</td>
  </tr>
  <tr>
    <td>One way</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Private roads</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Reversible lanes</td>
    <td>N</td>
  </tr>
  <tr>
    <td colspan="2">Intersection Types</td>
  </tr>
  <tr>
    <td>signaled</td>
    <td>N</td>
  </tr>
  <tr>
    <td>U-turn</td>
    <td>N</td>
  </tr>
  <tr>
    <td>4-way vs. 3-way vs. 2-way</td>
    <td>N</td>
  </tr>
  <tr>
    <td>stop sign</td>
    <td>N</td>
  </tr>
  <tr>
    <td>roundabout</td>
    <td>N</td>
  </tr>
  <tr>
    <td>merge lanes</td>
    <td>N</td>
  </tr>
  <tr>
    <td>left turn across traffic, one-way to one-way</td>
    <td>N</td>
  </tr>
  <tr>
    <td>right turn</td>
    <td>N</td>
  </tr>
  <tr>
    <td>multiple turn lane</td>
    <td>N</td>
  </tr>
  <tr>
    <td>crosswalk</td>
    <td>N</td>
  </tr>
  <tr>
    <td>toll plaza</td>
    <td>N</td>
  </tr>
  <tr>
    <td>railroad crossing</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Surfaces</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Asphalt</td>
    <td>Y</td>
  </tr>
  <tr>
    <td>Concrete<br></td>
    <td>N</td>
  </tr>
  <tr>
    <td>Mixed</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Grating</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Brick</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Dirt</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Gravel</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Scraped road</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Partially occluded</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Speed bumps</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Potholes</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Grass</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Edges and Markings</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Lane markers</td>
    <td>Clear markers</td>
  </tr>
  <tr>
    <td>Temporary lane markers</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Shoulder (paved or gravel)</td>
    <td>Gravel</td>
  </tr>
  <tr>
    <td>Lane barriers</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Grating</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Rails</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Curb</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Cones</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Geometry</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Straightaways</td>
    <td>Y</td>
  </tr>
  <tr>
    <td>Curves</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Hills</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Lateral crests</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Corners (regular, blind)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Negative obstacles</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Lane width</td>
    <td>&lt;TBD&gt;</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
</tbody>
</table>

## 4.2 Operational Constraints
<table> 
  <thead>
  <tr>
    <th colspan="2">Speed Limits</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Minimum Speed Limit</td>
    <td>0 km/h</td>
  </tr>
  <tr>
    <td>Maximum Speed Limit</td>
    <td>70 km/h</td>
  </tr>
  <tr>
    <td>Relative to Surrounding Traffic</td>
    <td>No surrounding traffic</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Traffic Conditions</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Traffic density</td>
    <td>No other traffic</td>
  </tr>
  <tr>
    <td>Altered (Accident emergency vehicle, construction, closed road, special event)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.3 Objects
<table> 
  <thead>
  <tr>
    <th colspan="2">Signage</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Signs (e.g., stop, yield, pedestrian, railroad, school zone, etc.)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Traffic Signals (regular, flashing, school zone, fire dept. zone)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Crosswalks</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Railroad crossing</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Stopped buses</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Construction signage</td>
    <td>N</td>
  </tr>
  <tr>
    <td>First responder signals  </td>
    <td>N</td>
  </tr>
  <tr>
    <td>Distress signals</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Roadway user signals</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Hand signals</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
</tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Users</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Vehicle types (cars, light trucks, large trucks, buses, motorcycles, wide-load, emergency vehicles, construction or farming equipment, horse-drawn carriages/buggies)</td>
    <td>No other vehicles</td>
  </tr>
  <tr>
    <td>Stopped vehicles</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other automated vehicles</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Pedestrians</td>
    <td>0-1 pedestrians, either stationary or moving with a constant speed (<20 km/h) and direction </td>
  </tr>
  <tr>
    <td>Cyclists</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Non-Roadway Users Obstacles</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Animals (e.g., dogs, deer, etc.)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Shopping carts</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Debris (e.g., pieces of tire, trash, ladders)</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.4 Connectivity
SMIRK does not rely on any external connectivity. All items below are either N or N/A.

<table> 
  <thead>
  <tr>
    <th colspan="2">Vehicles</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>V2I and V2V communications</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Emergency vehicles</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Remote Fleet Management System</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Does the system require an operations center?</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Does remote operation expand ODD or support fault handling?</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Infrastructure Sensors</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Work zone alerts</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Vulnerable road user</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Routing and incident management</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Digital Infrastructure</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>GPS</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>3-D Maps</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Pothole Locations</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Weather Data</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Infrastructure Data</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>


## 4.5 Environmental Conditions
<table> 
  <thead>
  <tr>
    <th colspan="2">Weather</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Wind</td>
    <td>Calm winds</td>
  </tr>
  <tr>
    <td>Rain</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Snow</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Sleet</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Temperature</td>
    <td>Between 5 and 30 degree Celsius</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Weather-Induced Roadway Conditions</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Standing Water</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Flooded Roadways</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Icy Roads</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Snow on Road</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Particulate Matter</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Fog</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Smoke</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Smog</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Dust/Dirt</td>
    <td>N</td>
  </tr>
  </tr>
    <tr>
    <td>Mud</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Illumination</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Day (sun: Overhead, Back-lighting and Frontlighting)</td>
    <td>Y, overhead sun</td>
  </tr>
  <tr>
    <td>Dawn</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Dusk</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Night</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Street lights</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Headlights (Regular & High-Beam)</td>
    <td>Turned off</td>
  </tr>
  <tr>
    <td>Oncoming vehicle lights (Overhead Lighting, Back-lighting & Front-lighting)</td>
    <td>N/A, no other traffic</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.6 Zones
SMIRK does not rely on any zone specifics. All items below are either N or N/A.

<table> 
  <thead>
  <tr>
    <th colspan="2">Geofencing</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>CBDs</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>School Campuses</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Retirement Communities</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Fixed Route</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Traffic Management Zones</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Temporary Closures</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Dynamic Traffic Signs</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Variable Speed Limits</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Temporary or Non-Existent Lane Marking</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Human-Directed Traffic</td>
    <td>N</td>
  </tr>
  <tr>
  <td>Loading and Unloading Zones</td>
    <td>N</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">School/Construction Zones</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Dynamic speed limit</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Erratic pedestrian</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Vehicular behaviors</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Regions/States</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Legal/Regulatory</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Enforcement Considerations</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Tort</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

<table> 
  <thead>
  <tr>
    <th colspan="2">Interference Zones</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Tunnels</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Parking Garage</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Dense Foliage</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Limited GPS</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Atmospheric Conditions</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

# 5 ML Component Description [D] <a name="ml_component_desc"></a>

# 6 ML Assurance Scoping Argument Pattern [F] <a name="ml_assurance_scoping_pattern"></a>

# 7 Safety Requirements Allocated to ML Component [E] <a name="ml_component_safety_reqts"></a>

# 8 ML Safety Assurance Scoping Argument [G] <a name="ml_assurance_scoping_argument"></a>
