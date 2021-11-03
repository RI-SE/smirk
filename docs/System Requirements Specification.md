# System Requirements Specification v0.4

Revision History
<table>
<tr>
<th>Author(s)</th>
<th>Date</th>
<th>Description</th>
<th>Version</th>
</tr>
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
<td>2021-10-18</td>
<td>Complete draft.</td>
<td>0.3</td>
</tr>
<tr>
<td>Jens Henriksson, Kasper Socha</td>
<td>WIP</td>
<td>Updated after internal review.</td>
<td>0.4</td>
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
- DDS: Data Distribution Service
- FPS: Frames Per Second
- GSN: Goal Structuring Notation
- HARA: Hazard and Risk Analysis
- ML: Machine Learning
- ODD: Operational Design Domain
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
- Developers: the entire document is relevant.
- Testers: sections 3 (requirements) and 4 (ODD) are particularly important.
- Safety assessors: focus on headings that map to the AMLAS process.
- Other stakeholders: read sections 1 and 2 to get an overview of SMIRK.

## 1.5 Product Scope ##
SMIRK is an ADAS that is intended to co-exist with other ADAS in a vehicle. We expect that sensors and actuators will be shared among different systems. SMIRK implements its own perception based on radar and camera input. In future versions, it is likely that a central perception system operating on the vehicle will provide SMIRK with input. This is not yet the case. 

## 1.6 References ##
- [System Architecture Description](</docs/System Architecture Description.md>)
- Ben Abdessalem, Nejati, Briand, and Stifter, 2018. Testing Vision-based Control Systems Using Learnable Evolutionary Algorithms, in Proc. of the 40th Int’l. Conf. on Software Engineering.  
- Borg, Bronson, Christensson, Olsson, Lennartsson, Sonnsjö, Ebadi, and Karsberg, 2021. Exploring the Assessment List for Trustworthy AI in the Context of Advanced Driver-Assistance Systems, In Proc. of the 2nd Workshop on Ethics in Software Engineering Research and Practice.
- Gauerhof, Hawkins, David, Picardi, Paterson, Hagiwara, and Habli, 2020. Assuring the Safety of Machine Learning for Pedestrian Detection at Crossings. In Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP).
- Hawkins, Paterson, Picardi, Jia, Calinescu, and Habli. [Guidance on the Assurance of Machine Learning in Autonomous Systems (AMLAS)](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf), v1.1, Techincal Report, University of York, 2021.
- Henriksson, Berger, Borg, Tornberg, Englund, Sathyamoorthy, and Ursing, 2019. Towards Structured Evaluation of Deep Neural Network Supervisors, In Proc. of the International Conference On Artificial Intelligence Testing, pp. 27-34.
- Henriksson, Berger, Borg, Tornberg, Sathyamoorthy, and Englund, 2021. Performance Analysis of Out-of-Distribution Detection on Trained Neural Networks. Information and Software Technology, 130.
- Nair, De La Vara, Sabetzadeh, and Briand, 2014. [An extended systematic literature review on provision of evidence for safety certification](https://www.sciencedirect.com/science/article/abs/pii/S0950584914000603). *Information and Software Technology*, 56(7), 689-717.
- Object Management Group (OMG) Data Distribution Service (DDS)(https://www.dds-foundation.org/what-is-dds-3/), Last checked: 2021-09-09.
- Picardi, Paterson, Hawkins, Calinescu, and Habli, 2020. [Assurance Argument Patterns and Processes for Machine Learning in Safety-Related Systems](http://ceur-ws.org/Vol-2560/paper17.pdf). In *Proceedings of the Workshop on Artificial Intelligence Safety (SafeAI 2020)*, pp. 23-30.
- [Safety First for Automated Driving (SaFAD)](https://www.daimler.com/documents/innovation/other/safety-first-for-automated-driving.pdf), 2019. Joint White Paper by Aptiv, Audi, Bayrische Motoren Werke; Beijing Baidu Netcom Science Technology, Continental Teves AG, Daimler, FCA US, HERE Global, Infineon Technologies, Intel, and Volkswagen.
- The Assurance Case Working Group (ACWG), 2018. [Goal Structuring Notation Community Standard, Version 2](https://scsc.uk/r141B:1?t=1), SCSC-141B. 
- Thorn, Kimmel, and Chaka, 2018. [A Framework for Automated Driving System Testable Cases and Scenarios](https://trid.trb.org/view/1574670), Technical Report DOT HS 812 623, National Highway Traffic Safety Administration.

# 2 System Description [C] <a name="system_reqts"></a>
SMIRK is an Open-Source Software (OSS) ML-based ADAS under development. It is a research prototype that provides pedestrian emergency braking that adheres to development practices mandated by the candidate standard ISO 21448. To ensure industrial relevance, SMIRK builds on the reference architecture from PeVi, an ADAS studied in previous work (Ben Abdessalem et al., 2018). SMIRK uses a radar sensor and a camera to detect pedestrians on collision course and commissions emergency braking. The system combines Python source code and a trained DNN for object detection that demonstrates safety-critical driving automation on SAE Level 1.

The SMIRK system architecture is further described in the [System Architecture Description](</docs/System Architecture Description.md>).

## 2.1 Product Perspective ##
SMIRK is designed to send a brake signal when a collision with a pedestrian is imminent. The figures below show five standard scenarios and a general scenario illustrating that SMIRK can handle arbitrary angles, i.e., not only perpendicular movement. Note that the fifth scenario represents a stationary pedestrian, a scenario that is known to be different to pedestrian detection systems.

![Scenario1](/docs/figures/scenario1.png) <a name="scenario1"></a>
![Scenario2](/docs/figures/scenario2.png) <a name="scenario2"></a>
![Scenario3](/docs/figures/scenario3.png) <a name="scenario3"></a>
![Scenario4](/docs/figures/scenario4.png) <a name="scenario4"></a>
![Scenario5](/docs/figures/scenario5.png) <a name="scenario5"></a>
![Scenario6](/docs/figures/scenario6.png) <a name="scenario6"></a>

The figure below shows a SMIRK context diagram. The sole purpose of SMIRK is pedestrian emergency braking. The design of the SMIRK assumes that it will be deployed in a vehicle with complementary ADAS, e.g., large animal detection, lane keeping assistance, and various types of collision avoidance (cf. Other ADAS 1 - N). We also expect that sensors and actuators will be shared between ADAS. On the other hand, we do not assume a central perception system that fuses various types of sensor input for individual ADAS to use. SMIRK uses a standalone ML model trained for pedestrian detection. Solid lines in the figure show how SMIRK interacts with sensors and actuators in the ego vehicle. Dashed lines indicate how other ADAS might use sensors and actuators.

![Context](/docs/figures/context_diagram.png) <a name="context"></a>

## 2.2 Product Functions ##
SMIRK comprises the following product functions, organized into the categories sensors, algorithms, and actuators in line with ISO 21448.

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

The figure below illustrates detection of a pedestrian on a collision course, i.e., automatic emergency braking shall be commenced.

![pedestrian_detection](/docs/figures/pedestrian_detection.png) <a name="pedestrian_detection"></a>

## 2.3 External Interface Requirements ##
SMIRK and ESI Pro-SiVIC communicate through two different python APIs provided by ESI, the Pro-SiVIC TCP remote controls API, and the Pro-SiVIC DDS API. OMG Data Distribution Service (DDS) is a middleware protocol and API standard for data-centric connectivity from the Object Management Group. In summary,

- All dynamic Pro-SiVIC setup is communicated as Pro-SiVIC commands  over TCP.
- Scenarios are started over TCP.	
- All subsequent data communication, i.e., live data during the simulation, is transferred over DDS through the Python API.

# 3 System Requirements
This section specified the SMIRK system requirements, organized into system safety requirements and ML safety requirements. ML safety requirements are further refined into performance requirements and robustness requirements. The requirements are inspired by Gauerhof et al. (2020).

## 3.1 System Safety Requirements [A] <a name="system_safety_reqts"></a>
This section specifies the highest level SMIRK requirement.

- **SYS-SAF-REQ1: Ego shall commence automatic emergency braking if collision with a pedestrian is imminent.**

Rationale: This is the main purpose of SMIRK. If possible, Ego will stop and avoid a collision. If a collision is inevitable, Ego will reduce speed to decrease the impact severity. Hazards introduced from false positives, i.e., braking for ghosts, are mitigated under ML Safety Requirements.

## 3.2 Safety Requirements Allocated to ML Component [E] <a name="ml_component_safety_reqts"></a>
Based on a HARA, two categories of hazards were identified. First, SMIRK might miss pedestrians and fail to commence emergency braking - we refer to this as a false negative. Second, SMIRK might commence emergency braking when it should not - we refer to this as a false positive. A summary of the HARA is presented below.

- False negative: The severity of the hazard is very high (high risk of fatality). Controllability is high since the driver can brake ego vehicle.
- False positive: The severity of the hazard is high (can be fatal). Controllability is very low since the driver would have no chance to counteract the braking. 
 
To conclude, we refine SYS-SAF-REQ1 in the next section to specify requirements in relation to false negatives. Furthermore, the false positive hazard necessitates the introduction of SYS-ML-REQ2.

## 3.3 Machine Learning Safety Requirements [H] <a name="ml_safety_reqts"></a>
This section refines SYS-SAF-REQ into two separate requirements corresponding to false positives and false negatives, respectively.

- **SYS-ML-REQ1: The object detection component shall detect pedestrians if the radar tracking component returns TTC < 4s for the corresponding object.**
- **SYS-ML-REQ2: The object detection component shall reject input that does not resemble the training data.**

Rationale: SMIRK follows the reference architecture from Ben Abdessalem et al. (2018) and SYS-ML-REQ1 uses the same TTC threshold (4s). SYS-ML-REQ2 motivates the primary contribution of the SMILE projects, i.e., an out-of-distribution detection mechanism that we refer to as a safety cage.

## 3.3.1 Performance Requirements
This section specifies performance requirements corresponding to the ML safety requirements with a focus on quantitative targets. All requirements below are restricted to pedestrians on or close to the road.

- **SYS-PER-REQ1: The object detection component shall identify pedestrians with an accuracy of 0.93 when they are within 50 meters.**
- **SYS-PER-REQ2: The false negative rate of the object detection component shall not exceed 7% for pedestrians when they are within 50 meters.**
- **SYS-PER-REQ3: The false positive rate shall not exceed 0.01% for objects detected by the radar tracking component with a TTC < 4s** 
- **SYS-PER-REQ4: In a sequence of images from a video feed any object to be detected shall not be missed in more than 1 out of 5 frames.**
- **SYS-PER-REQ5: The position of pedestrians shall be determined within 50 cm of their actual position.**
- **SYS-PER-REQ6: The object detection component shall allow an inference speed of at least 10 FPS on the target platform.**

Rationale: SMIRK adapts the performance requirements specified by Gauerhof et al. (2020) for the SMIRK ODD. SYS-PER-REQ1 reuses the accuracy threshold from Example 7 in AMLAS. SYS-PER-REQ2 and SYS-PER-REQ3 are two additional requirements inspired by Henriksson et al. (2019). SYS-PER-REQ6 means that any further improvements to reaction time have a negligible impact on the total brake distance. 

## 3.3.2 Robustness Requirements
This section specifies robustness requirements corresponding to the ML safety requirements.

- **SYS-ROB-REQ1: The object detection component shall perform as required in all situations Ego may encounter within the defined ODD.**
- **SYS-ROB-REQ2: The ML component shall identify a person irrespective of their pose with respect to the camera.**

Rationale: SMIRK reuses robustness requirements for pedestrian detection from previous work. SYS-ROB-REQ1 is specified in Gauerhof et al. (2020). SYS-ROB-REQ2 is presented as Example 7 in AMLAS.

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

# 5 ML Assurance Scoping Argument Pattern [F] <a name="ml_assurance_scoping_pattern"></a>
The figure below shows the ML assurance scoping argument pattern using GSN. The pattern follows the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Assurance_Scoping_Argument_Pattern](/docs/figures/gsn-ml_assurance_scoping_argument_pattern.png) <a name="gsn-ml_assurance_scoping"></a>

The top claim, i.e., the starting point for the safety argument for the SMIRK ML-based object detection component, is that the system safety requirements that have been allocated to the component are satisfied in the ODD (G1.1). The safety claim for the object detection component is made within the context of the information that was used to establish the safety requirements allocation, i.e., the system description ([C]), the ODD ([B]), and ML component description ([D]). The allocated system safety requirements ([E]) are also provided as context. An explicit assumption is made that the allocated safety requirements have been correctly defined (A1.1), as this is part of the overall system safety process preceding AMLAS. Our claim to the validity of this assumption is presented in relation to the HARA described in [E]. As stated in AMLAS, "the primary aim of the ML Safety Assurance Scoping argument is to explain and justify the essential relationship between, on the one hand, the system-level safety requirements and associated hazards and risks, and on the other hand, the ML-specific safety requirements and associated ML performance and failure conditions."

The ML safety claim is supported by an argument split into two parts. First, the development of the ML component is considered with an argument that starts with the elicitation of the ML safety requirements argument. Second, the deployment of the ML component is addressed with a corresponding argument. 

# 6 ML Safety Assurance Scoping Argument [G] <a name="ml_assurance_scoping_argument"></a>
SMIRK instantiates the ML safety assurance scoping argument through the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). The set of artifacts constitutes the safety case for the ML-based SMIRK object detection component.

# 7 ML Safety Requirements Argument Pattern [I]
The figure below shows the ML safety requirements argument pattern using GSN. The pattern largely follows the example provided in AMLAS, but adapts it to the specific SMIRK case. The major difference is the introduction of G2.2 targeting false positives and the safety cage mechanism as the corresponding solution 2.2.

![GSN-ML-Safety_Reqts_Argument_Pattern](/docs/figures/gsn-ml_safety_reqts_argument_pattern.png) <a name="gsn-ml_safety_reqts_argument"></a>

The top claim is that system safety requirements that have been allocated to the ML component are satisfied by the model that is developed (G2.1). This is demonstrated through considering explicit ML safety requirements defined for the ML model [H]. The argument approach is a refinement strategy translating the allocated safety requirements into two concrete ML safety requirements (S2.1) provided as context (C2.1). Justification J2.1 explains how we allocated safety requirements to the ML component as part of the system safety process, including the hazard and risk analysis. 

Strategy 2.1 is refined into two subclaims about the validity of the ML safety requirements corresponding to false negatives and false positives, respectively. Furthermore, a third subclaim concerns the satisfaction of those requirements. G2.2 focuses on the ML safety requirement SYS-ML-REQ1, i.e., that the nominal functionality of the object detection system shall be satisfactory. G2.2 is considered in the context of the ML data (C2.2) and the ML model (C2.3), which in turn are supported by the ML Data Argument Pattern [R] and the ML Learning Argument Pattern [W]. The argumentation strategy (S2.2) builds on two subclaims related to two types of safety requirements with respect to safety-related outputs, i.e., performance requirements (G2.5 in context of C2.4) and robustness requirements (G2.6 in context of C2.5). The satisfaction of both G2.5 and G2.6 are addressed by the ML Verification Argument Pattern [BB]. G2.3 focuses on the ML safety requirement SYS-ML-REQ2, i.e., that the object detection component shall reject input that does not resemble the training data to avoid false positives. G2.3 is again considered in the context of the ML data (C2.2) and the ML model (C2.3). For SMIRK, the solution is the safety cage architecture (Sn2.1) developed  in the SMILE research program (Henriksson et al., 2021), further described in the [Machine Learning Component Specification](</docs/ML Component Specification.md#4-safety-cage-architecture>).

Subclaim G2.4 states that the ML safety requirements are a valid development of the allocated system safety requirements. The justification (J2.2) is that the requirements have been validated in cross-organizational workshops within the SMILE3 research project. We provide evidence through ML Safety Requirements Validation Results [J] originating in a Fagan inspection (Sn2.2).

# 8 ML Safety Requirements Validation Results [J]
The SMILE project conducted a [Fagan inspection](https://en.wikipedia.org/wiki/Fagan_inspection) of the ML safety requirements, i.e., a formal inspection consisting of the steps 1) Planning, 2) Overview, 3) Preparation, 4) Inspection meeting, 5) Rework, and 6) Follow-up. The Fagan inspection targeted the entire SRS.

1. Planning: The authors prepared the SRS and invited the required reviewers to an inspection meeting.
1. Overview: During one of the regular project meetings, the lead authors explained the fundamental structure of the SRS to the reviewers. The SRS inspection checklist was also introduced. Reviewers were also assigned particular inspection perspectives based on their individual expertise. All information was repeated in an email, as not all reviewers were present at the meeting.
1. Preparation: All reviewers conducted an individual inspection of the SRS, noting any questions, issues, and required improvements.
1. Inspection meeting: After sufficient time for the individual inspections, the lead authors and all reviewers met for a virtual meeting. The entire document was discussed, and the findings from the independent inspections were compared. All issues were compiled in an inspection protocol.
1. Rework: The lead authors updated the SRS according to the inspection protocol.
1. Follow-up: Selected reviewers verified that the previously found issues had been correctly resolved. 

The inspection protocol is available at TBD.

# 9 ML Safety Requirements Argument [K]
SMIRK instantiates the ML safety requirements argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Safety Requirements Argument Pattern [I]](</docs/System Requirements Specification.md#5-ml-assurance-scoping-argument-pattern-f->), as well as the following artifacts from preceding AMLAS activities:
- [Safety Requirements Allocated to ML Component](</docs/System Requirements Specification.md#32-safety-requirements-allocated-to-ml-component-e->) [E]
- [ML Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) [H]
- [ML Safety Requirements Validation Results](</docs/System Requirements Specification.md#8-ml-safety-requirements-validation-results-j>) [J]
