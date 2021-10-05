# Deployment Specification v0.1

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
<td>2021-10-05</th>
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
This document containts the deployment specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
This document describes the deployment of SMIRK on the experimental plattform that runs ESI Pro-SiVIC.

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DM: Data Management
- ML: Machine Learning
- ODD: Operational Design Domain

## 1.4 Intended Audience and Reading Suggestions ##
- Developers: The entire document is relevant.
- ML developers: The entire document is relevant.
- Testers: The entire document is relevant.
- Safety assessors: The entire document is relevant.
- Other stakeholders: TBD

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)

# 3 Operating Environment <a name="env"></a>

# 4 ML Deployment Argument Pattern [GG]
The figure below shows the ML deployment argument pattern using GSN. Since SMIRK is developed for a simulated environment, the pattern is adapted accordingly.

![GSN-ML-Deployment_Argument_Pattern](/docs/figures/gsn-ml_deployment_argument_pattern.png) <a name="gsn-ml_deployment_argument"></a>

