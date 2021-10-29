# System Architecture Description v0.1

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
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the architecture description for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC. 

## 1.1 Purpose ##
SMIRK assists the driver on country roads by performing emergency braking in the case of an imminent collision with a pedestrian. The level of automation offered by SMIRK corresponds to SAE Level 1 - Driver Assistance, i.e., "the driving mode-specific execution by a driver assistance system of either steering or acceleration/deceleration." SMIRK is developed with a focus on evolvability, thus future versions might include steering and thus comply with SAE Level 2.

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
- Testers: TBD
- Safety assessors: TBD
- Other stakeholders: TBD

## 1.5 Product Scope ##
SMIRK is an ADAS that is intended to co-exist with other ADAS in a vechicle. We expect that sensors and actuators will be shared among different systems. SMIRK implements its own perception based on radar and camera input. In future versions, it is likely that a central perception system operating on the vehicle will provide SMIRK with input. This is not yet the case. 

## 1.6 References ##
TBD

# 2 Architecture Viewpoints

## 2.1 Concerns Stakeholders

## 2.2 Model Kinds

## 2.3 Operations on Views

# 3 Architecture Views
According to the 4+1 View by Kruchten.

# 3.1 Logical View

# 3.2 Process View

# 3.3 Development View

# 3.4 Physical View

# 3.5 Scenarios

# 4 Architecture Decisions and Rationale