# System Requirements Specification v0.3

Revision History
<table>
<tr>
<td>Markus Borg</th>
<td>2021-05-13</th>
<td>Initialized using IEEE SRS template.</th>
<td>0.1</th>
</tr>
<tr>
<td>Markus Borg</td>
<td>2021-09-03</td>
<td>Initial version to discuss at AMLAS workshop.</td>
<td>0.2</td>
</tr>
<tr>
<td>Markus Borg, Jens Henriksson</td>
<td>WIP</td>
<td>Working toward the first complete draft.</td>
<td>0.3</td>
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

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC. 

## 1.1 Purpose ##
SMIRK assists the driver on country roads by performing emergency braking in the case of an imminent collision with a pedestrian. The level of automation offered by SMIRK corresponds to SAE Level 1 - Driver Assistance, i.e., "the driving mode-specific execution by a driver assistance system of either steering or acceleration/deceleration." SMIRK is developed with a focus on evolvability, thus future versions might include steering and thus comply with SAE Level 2.

This document provides the foundation for the SMIRK minimum viable product (MVP).

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- ML: Machine Learning
- ODD: Operational Design Domain
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
- Developers: the entire document is relevant.
- Testers: sections 3 (requirements) and 4 (ODD) are particularly important.
- Safety assessors: focus on headings that map to the AMLAS process.
- Other stakeholders: read sections 1 and 2 to get an overview of SMIRK.

## 1.5 Product Scope ##
SMIRK is an ADAS that is intended to co-exist with other ADAS in a vechicle. We expect that sensors and actuators will be shared among different systems. SMIRK implements its own perception based on radar and camera input. In future versions, it is likely that a central perception system operating on the vehicle will provide SMIRK with input. This is not yet the case. 

## 1.6 References ##
- Ben Abdessalem, Nejati, Briand, and Stifter, 2018. Testing Vision-based Control Systems Using Learnable Evolutionary Algorithms, in Proc. of the 40th Int’l. Conf. on Software Engineering.  
- Borg, Bronson, Christensson, Olsson, Lennartsson, Sonnsjö, Ebadi, and Karsberg, 2021. Exploring the Assessment List for Trustworthy AI in the Context of Advanced Driver-Assistance Systems, In Proc. of the 2nd Workshop on Ethics in Software Engineering Research and Practice.
- Gauerhof, Hawkins, David, Picardi, Paterson, Hagiwara, and Habli, 2020. Assuring the Safety of Machine Learning for Pedestrian Detection at Crossings. In Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP). 
- Nair, De La Vara, Sabetzadeh, and Briand, 2014. [An extended systematic literature review on provision of evidence for safety certification](https://www.sciencedirect.com/science/article/abs/pii/S0950584914000603). *Information and Software Technology*, 56(7), 689-717.
- Picardi, Paterson, Hawkins, Calinescu, and Habli, 2020. [Assurance Argument Patterns and Processes for Machine Learning in Safety-Related Systems](http://ceur-ws.org/Vol-2560/paper17.pdf). In *Proceedings of the Workshop on Artificial Intelligence Safety (SafeAI 2020)*, pp. 23-30.
- Thorn, Kimmel, and Chaka, 2018. [A Framework for Automated Driving System Testable Cases and Scenarios](https://trid.trb.org/view/1574670), Technical Report DOT HS 812 623, National Highway Traffic Safety Administration.

# 2 System Description [C] <a name="system_reqts"></a>
SMIRK is an Open-Source Software (OSS) ML-based ADAS under development. It is a research prototype that provides pedestrian emergency braking that adheres to development practices mandated by the candidate standard ISO 21448. To ensure industrial relevance, SMIRK builds on the reference architecture from PeVi, an ADAS studied in previous work (Ben Abdessalem et al., 2018). SMIRK uses a radar sensor and a camera to detect pedestrians on collision course and commissions emergency braking. The system combines Python source code and a trained DNN for object detection that demonstrates safety-critical driving automation on SAE Level 1.


## 2.1 Product Perspective ##
SMIRK is designed to send a brake signal when a collision with a pedestrian is imminent. The figures below show five standard scenarios and general scenario illustrating that SMIRK can handle arbitrary angles, i.e., not only perpendicular movement. Note that the fifth scenario represents a stationary pedestrian, a scenario that is known to be different to pedestrian detection systems.

![Scenario1](/docs/figures/scenario1.png) <a name="scenario1"></a>
![Scenario2](/docs/figures/scenario2.png) <a name="scenario2"></a>
![Scenario3](/docs/figures/scenario3.png) <a name="scenario3"></a>
![Scenario4](/docs/figures/scenario4.png) <a name="scenario4"></a>
![Scenario5](/docs/figures/scenario5.png) <a name="scenario5"></a>
![Scenario6](/docs/figures/scenario6.png) <a name="scenario6"></a>

## 2.2 Product Functions ##
SMIRK comprices the following product functions, organized into the categories sensors, algorithms, and actuators in line with ISO 21448.

Sensors:
- Radar detection and tracking of objects in front of the vehicle (provided by ESI Pro-SiVIC, not elaborated further).
- A forward-facing mono-camera (provided by ESI Pro-SiVIC, not elaborated further).

Algorithms:
- Time-to-collision calculation for objects on collision course.
- Pedestrian detection based on the camera input.
- Out-of-distribution detection of never-seen-before input (part of the safety-cage mechanism).
- A braking module that commissions emergency braking. 

Actuators:
- Brakes (provided by ESI Pro-SiVIC, not elaborated further).

## 2.3 External Interface Requirements ##
The ESI Pro-SiVIC Python API and DDS communication provides interfaces between the simulator and SMIRK. The Python API is only used for initialization, all subsequent communications uses DDS.

# 3 System Requirements
This section specified the SMIRK system requirements, organized into system safety requirements and ML safety requirements. ML safety requirements are further refined into performance requirements and robustness requirements. The requirements are inspired by Gauerhof et al. (2020).

# 3.1 System Safety Requirements [A] <a name="system_safety_reqts"></a>
SYS-SAF-REQ1: Ego shall stop if collision with a pedestrian is imminent.

# 3.2 Machine Learning Safety Requirements [H] <a name="ml_safety_reqts"></a>
SYS-ML-REQ1: The object detection component shall detect pedestrians if the radar tracking component returns TTC < 4s for the corresponding object.

# 3.2.1 Performance Requirements
- SYS-PER-REQ1: The object detection component shall identify pedestrians that are on or close to the road when they are 50 meters away or closer.
- SYS-PER-REQ2: In a sequence of images from a video feed any object to be detected shall not be missed more then 1 in 5 frames.
- SYS-PER-REQ3: Position of pedestrians shall be determined within 50 cm of their actual position.

# 3.2.2 Robustness Requirements
- SYS-ROB-REQ1: The object detection component shall perform as required in all situations Ego may encounter within the defined ODD.
- SYS-ROB-REQ2: The object detection component shall perform as required in the face of defined component failures arising within the system.
- SYS-ROB-REQ3: The ML component shall identify a person irrespective of their pose with respect to the camera.

# 4 Operational Design Domain [B] <a name="odd"></a>
This section specifies the SMIRK operational design domain (ODD). The ODD specification is based on the taxonomy developed by NHTSA (Thorn et al., 2018). Note that the ODD is deliberately restricted to allow rapid prototyping of a SMIRK MVP.

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
