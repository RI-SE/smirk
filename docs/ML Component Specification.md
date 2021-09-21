# Machine Learning Component Specification v0.1

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
<td>2021-09-21</th>
<td>Initial template.</th>
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
This document containts the ML component specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
This document describes the ML-based object detection component and the underlying neural network architecture for the perception model used in SMIRK. The object detection component detects pedestrians in input images, i.e., no other classes are detected in the input.

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DM: Data Management
- ML: Machine Learning
- ODD: Operational Design Domain
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
- Developers: TBD
- ML developers: The entire document is relevant.
- Testers: sections 2-6 are particularly important.
- Safety assessors: focus on headings that map to the AMLAS process.
- Other stakeholders: TBD

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)

# 2 ML Component Description [D] <a name="ml_comp_desc"></a>
This section describes the object detection component in SMIRK. 

# 3 Neural Network Architecture 
TBD

# 4 Safety Cage Architecture
TBD
