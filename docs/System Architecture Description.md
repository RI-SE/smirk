# System Architecture Description v0.99

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
<td>2021-10-29</th>
<td>Initialized using an adaptation of the ISO/IEC/IEEE 42010 template.</th>
<td>0.1</th>
</tr>
<tr>
<td>Jens Henriksson, Piotr Tomaszewski</th>
<td>2021-11-01</th>
<td>Migrated existing content from joint work on MS Teams.</th>
<td>0.2</th>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</th>
<td>2022-02-01</th>
<td>Toward a complete draft.</th>
<td>0.3</th>
</tr>
<tr>
<td>Markus Borg</th>
<td>2022-03-14</th>
<td>Complete draft.</th>
<td>0.9</th>
</tr>
<tr>
<td>Markus Borg, Kasper Socha, Jens Henriksson</th>
<td>2022-06-16</th>
<td>Beta Release - Ready for peer-review</th>
<td>0.99</th>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the architecture description for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic. SMIRK, including the accompanying safety case, is developed with full transparency under an open-source software (OSS) license. We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
The SMIRK *product goal* is to assist the driver on country roads in rural areas by performing emergency braking in the case of an imminent collision with a pedestrian. The level of automation offered by SMIRK corresponds to SAE Level 1 - Driver Assistance, i.e., "the driving mode-specific execution by a driver assistance system of either steering or acceleration/deceleration." SMIRK is developed with a focus on evolvability, thus future versions might include steering and thus comply with SAE Level 2. This document provides the foundation for the SMIRK minimum viable product (MVP), i.e., an implementation limited to a highly restricted operational design domain (ODD).

The *project goal* of the SMIRK development endeavor, as part of the research project SMILE3, is twofold. First, the project team will benefit substantially from having a concrete example of ADAS development as a basis for discussion. We will all learn how challenging it is to perform safety case development for ML-based perception systems by practically doing it for the SMIRK MVP. Nothing can substitute the experience of a hands-on engineering effort. Second, SMIRK will be provided as a completely open research prototype that can be used as a case under study in future research studies. As we keep expanding the ODD beyond the MVP limitations, the SMIRK ADAS can be used to study various aspects of AI engineering. For our subsequent research projects, we expect to primarily study the efficiency and effectiveness of various solution proposals related to software testing, verification, and validation.

## 1.2 Document Conventions ##
Names in bold font in the architecture views represent entities that can be found in the logical view.

## 1.3 Glossary
- ADAS: Advanced Driver-Assistance Systems
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- ML: Machine Learning
- ODD: Operational Design Domain
- PAEB: Pedestrian Automatic Emergency Braking
- SOTIF: Safety of the Intended Functionality (ISO/PAS 21448)
- SRS: System Requirements Specification
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
The section is organized into internal stakeholders, i.e., roles that are directly involved in the SMIRK development, and external stakeholders who are linked indirectly but have significant contribution in the successful completion of the SMIRK project. External stakeholders also include the ML safety community at large. Note that AMLAS prescribes a split between testers that are involved during the development and testers that are "sufficiently independent from the development activities." We refer to these roles as *internal testers* and *independent testers*, respectively.

**Internal stakeholders**

The entire document is relevant to the internal development organization. Specific stakeholders are recommended to pay particular attention as follows. 
- Software developers: [Section 3 (Architecture Views)](#3-architecture-views)
- ML developers: [Section 3 (Architecture Views)](#3-architecture-views)
- Internal testers: [Section 3 (Architecture Views)](#3-architecture-views) and [Section 3.5 (Scenarios)](#35-scenarios).
- Independent testers: [Section 3.5 (Scenarios)](#35-scenarios).

**External stakeholders**
- Safety assessors: [Section 3.5 (Scenarios)](#35-scenarios).
- Researchers: Academic and industrial reserachers active in ML safety are likely to find the most value in [Section 3 (Architecture Views)](#3-architecture-views).
- Standardization bodies and legislators: [Section 3.5 (Scenarios)](#35-scenarios).
- Curious readers: [Section 3.5 (Scenarios)](#35-scenarios).

## 1.5 Product Scope ##
SMIRK is an ADAS that is intended to co-exist with other ADAS in a vehicle. We expect that sensors and actuators will be shared among different systems. SMIRK currently implements its own perception system based on radar and camera input. In future versions, it is likely that a central perception system operating on the vehicle will provide reliable input to SMIRK. This is not yet the case for the SMIRK MVP and this version of the SRS does not specify any requirements related to shared resources. The SMIRK scope is further explained through the context diagram in the [System Requirements Specification](</docs/System Requirements Specification.md>).

## 1.6 References ##
The references are organized into 1) internal SMIRK documentation, 2) peer-reviewed publications, and 3) gray literature and white papers. 

**Internal SMIRK documentation**
- [System Requirements Specification](</docs/System Requirements Specification.md>) (SRS)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)

**Peer-reviewed publications**
- Kruchten, 1995. The 4+1 View Model of Architecture. IEEE Software, 12(6), pp. 42-50.

**Gray literature and white papers**
- Hillard, 2014. Architecture Description Template For Use With ISO/IEC/IEEE 42010:2011, version 2.2. [link](http://www.iso-architecture.org/42010/templates/)
- International Organization for Standardization, [ISO/PAS 21448:2019](https://www.iso.org/standard/70939.html) Road vehicles — Safety of the intended functionality 

# 2 Architecture Viewpoints
SMIRK is a pedestrian emergency braking ADAS. The system uses input from two sensors (camera and radar/LiDAR), implements a deep neural network trained for pedestrian detection and recognition. To minimize hazardous false positives, SMIRK implements a SMILE safety cage to reject input that is out-of-distribution.

If the radar detects an imminent collision between the ego car and an object, SMIRK will evaluate if the object is a pedestrian. If SMIRK is confident that the object is a pedestrian, it will apply emergency braking.

The primary purpose of SMIRK is to act as a proof-of-concept ADAS with a complete safety case for research purposes. To allow this, SMIRK is designed to operate in a highly restricted ODD that covers a straight rural road, good conditions, no other vehicles, and potentially a single pedestrian walking along or across the road. A complete description is available in the [Operational Design Domain](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#4-operational-design-domain-b-) in the SRS.

Based on a stakeholder analysis in the SMILE3 project, this architecture description considers the following stakeholders:
- Researchers who want to study the design of SMIRK.
- Safety assessors who want to investigate the general design in the light of the safety case.
- Software developers building or evolving SMIRK.
- ML developers designing and tuning the ML perception model.
- Hardware developers interested in the SMIRK sensors, incl. replacing them or adding sensor fusion.
- Simulator developers looking for ways to port SMIRK to their virtual prototyping environments.
- Testers developing test plans for SMIRK.
- System integrators who are about to include SMIRK in other systems, incl. co-existence with other ADAS.

Explicitly defined architecture viewpoints support effective communication of certain aspects and layers of a system architecture. The different viewpoints of the identified stakeholders are covered by the established 4+1 view of architecture by Kruchten (1995). In the next section, we describe the SMIRK architecture from the 1) logical viewpoint, 2) process viewpoint, 3) development viewpoint, 4) physical viewpoint, and a set of illustrative 5) scenarios.

# 3 Architecture Views
Kruchten (1995) developed the 4+1 view model to support documentation and communication of software-intensive systems. The model is a generic tool that does not restrict its users in terms of notations, tools or design methods. For SMIRK, we describe the logical view using a simple illustration with limited embedded semantics.  The illustration is complemented by detailed textual explanations. The process view, development view, and the physical view are presented through bulleted lists. Scenarios are illustrated with figures and explanatory text.

## 3.1 Logical View
The SMIRK logical view is constituted by a description of the entities that realize the PAEB.

![Logical_View](/docs/figures/logical_view.png) <a name="logical_view"></a>

*Figure 1: SMIRK logical view.*

SMIRK interacts with three external resources, i.e., hardware sensors and actuators in ESI Pro-SiVIC:
	- A) Mono **Camera** (752x480 (WVGA), sensor dimension 3.13 cm x 2.00 cm, focal length 3.73 cm, angle of view 45 degrees)
	- B) **Radar** unit (providing object tracking and relative lateral and longitudinal speeds)
	- C) **Ego Car** (Audi A4 for which we are mostly concerned with the brake system)

SMIRK consists of the following constituents.
- Software components implemented in Python:
	- D) **Radar Logic** (calculating TTC based on relative speeds)
	- E) **Perception Orchestrator** (the overall perception logic)
	- F) **Rule Engine** (part of the safety cage, implementing heuristics such as pedestrians do not fly in the air)
	- G) **Uncertainty Manager** (main part of the safety cage, implementing logic to avoid false positives)
	- H) **Brake Manager** (calculating and sending brake signals to the ego car)
- Trained Machine Learning models:
	- I) **Pedestrian Detector** (a YOLOv5 model trained using PyTorch)
	- J) **Anomaly Detector** (a third party component from [Seldon](https://github.com/SeldonIO/alibi-detect))

We refer to E), F), G), I), and J) as the **Pedestrian Recognition Component**, i.e., the ML-based component for which we present a safety case.

## 3.2 Process View
The process view deals with the dynamic aspects of SMIRK including an overview of the run time behavior of the system. The overall SMIRK flow is as follows:

1. The **Radar** detects an object and sends the signature to the **Radar Logic** class.
1. The **Radar Logic** class calculates the TTC. If a collision between the ego car and the object is imminent, i.e., TTC is less than 4 seconds assuming constant motion vectors, the **Perception Orchestrator** is notified.
1. The **Perception Orchestrator** forwards the most recent image from the **Camera** to the **Pedestrian Detector** to evaluate if the detected object is a pedestrian.
1. The **Pedestrian Detector** performs a pedestrian detection in the image and returns the verdict (True / False) to the **Pedestrian Orchestrator**. 
1. If there appears to be a pedestrian on a collision course, the **Pedestrian Orchestrator** forwards the image and the radar signature to the **Uncertainty Manager** in the safety cage.
1. The **Uncertainty Manager** sends the image to the **Anomaly Detector** and requests an analysis of whether the camera input is Out-Of-Distribution (OOD) or not.
1. The **Anomaly Detector** analyzes the image in the light of the training data and returns its verdict (True / False).
1. If there indeed appears to be an imminent collision with a pedestrian, the **Uncertainty Manager** all available information is forwarded to the **Rule Engine** for a sanity check.
1. The **Rule Engine** does a sanity check based on heuristics, e.g., in relation to laws of physics, and returns a verdict (True / False).
1. The **Uncertainty Manager** aggregates all information and, if the confidence is above a threshold, notifies the **Brake Manager** that collision with a pedestrian is imminent.
1. The **Brake Manager** calculates a safe brake level and sends the signal to **Ego Car** to commence PAEB.

## 3.3 Development View
The development view illustrates SMIRK from the perspective of the developers. A focus area in the SMIRK development project is to enable a high level of pipeline automation. The training data for the ML-based perception detection is generated using ESI Pro-SiVIC. TBD: Kasper to describe the design choices from the developers persepctive and the pipeline. 

## 3.4 Physical View
The physical view presents the system from a system engineer's point of view. As SMIRK is designed to be deployed in a simulated environment, i.e., ESI Pro-SiVIC, we present only a simple physical view based on the separation into 1) sensors, 2) decision algorithms, and 3) actuators as prescribed in ISO/PAS 21448 SOTIF. The left part of the figure shows the sensors, i.e., the radar unit and the mono camera. In the center part, the decision algorithms of the perception system is presented. YOLOv5 and the anomaly detector are described in the [Machine Learning Component Specification](</docs/ML Component Specification.md>). Finally, the right part of the figure shows the brakes simulated in ESI Pro-SiVIC.

![Physical_View](/docs/figures/physical_view.png) <a name="physical_view"></a>

*Figure 2: SMIRK physical view.*

## 3.5 Scenarios
Scenarios demonstrate the architecture through a small set of use cases. The figures below depict six standard PAEB scenarios. In the figures, *v* shows the speed of the car and the pedestrian, respectively. If the constant motion vectors would result in a collision, SMIRK shall commence PAEB when the TTC is less than 4 seconds.

Scenario 1 - Pedestrian crossing the road from the right.

![Scenario1](/docs/figures/scenario1.png) <a name="scenario1"></a>

Scenario 2 - Pedestrian crossing the road from the left. 

![Scenario2](/docs/figures/scenario2.png) <a name="scenario2"></a>

Scenario 3 - Pedestrian moving on the road toward the car. 

![Scenario3](/docs/figures/scenario3.png) <a name="scenario3"></a>

Scenario 4 - Pedestrian moving on the road away from the car. 

![Scenario4](/docs/figures/scenario4.png) <a name="scenario4"></a>

Scenario 5 - Pedestrian standing still on the road. 

![Scenario5](/docs/figures/scenario5.png) <a name="scenario5"></a>

Scenario 6 - Pedestrian crossing the road from the right with the angle θ.

![Scenario6](/docs/figures/scenario6.png) <a name="scenario6"></a>

# 4 Architecture Decisions and Rationale
Tradeoffs between quality requirements motivate architectural design decisions. We elaborate on quality prioritization in the [SRS](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#15-product-scope).
