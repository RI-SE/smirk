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
![AMLAS process](/docs/figures/srs_odd_physical.png) <a name="amlas"></a>

## 4.2 Operational Constraints
![AMLAS process](/docs/figures/srs_odd_operational.png) <a name="amlas"></a>

## 4.3 Objects
![AMLAS process](/docs/figures/srs_odd_objects.png) <a name="amlas"></a>

## 4.4 Connectivity
N/A

## 4.5 Environmental Conditions
![AMLAS process](/docs/figures/srs_odd_environmental.png) <a name="amlas"></a>

## 4.6 Zones
![AMLAS process](/docs/figures/srs_odd_zones.png) <a name="amlas"></a>

# 5 ML Component Description [D] <a name="ml_component_desc"></a>

# 6 ML Assurance Scoping Argument Pattern [F] <a name="ml_assurance_scoping_pattern"></a>

# 7 Safety Requirements Allocated to ML Component [E] <a name="ml_component_safety_reqts"></a>

# 8 ML Safety Assurance Scoping Argument [G] <a name="ml_assurance_scoping_argument"></a>
