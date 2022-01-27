# Deployment Specification v0.2

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
<tr>
<td>Markus Borg</th>
<td>WIP</th>
<td>Toward a complete draft.</th>
<td>0.2</th>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the deployment specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
This document describes the deployment of SMIRK on the experimental platform that runs ESI Pro-SiVIC.

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

The top claim (G6.1) is that the ML safety requirements SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied when deployed to the ego car in which SMIRK operates. The argumentation strategy S6.1 is two-fold. First, sub-claim G6.2 is that the ML safety requirements are satisfied under all defined operating scenarios when the ML component is integrated into SMIRK in the context (C6.1) of the specified operational scenarios [EE]. Justification J6.1 explains that the scenarios were identified through an analysis of the SMIRK ODD. G6.2 has another sub-claim (G6.4) that the integration test results [FF] show that SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied. 

Second, sub-claim G6.3 argues that SYS-ML-REQ1 and SYS-ML-REQ2 continue to be satisfied during the operation of SMIRK. The supporting argumentation strategy (S6.3) relates to the design of SMIRK and is again two-fold. First, sub-claim G6.6 argues that the operational achievement of the deployed component satisfies the ML safety requirements. Second, sub-claim G6.5 argues that the design of SMIRK into which the ML component is integrated ensures that SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied throughout operation. The argumentation strategy (S6.4) is based on demonstrating that the design is robust by taking into account identified erroneous behavior in the context (C5.1) of the Erroneous Behavior Log [DD]. More specifically, the argumentation entails that predicted erroneous behavior will not result in the violation of the ML safety requirements. This is supported by two sub-claims, i.e., that the system design provides sufficient monitoring of erroneous inputs and outputs (G6.7) and that the system design provides acceptable response to erroneous inputs and outputs (G6.8). Both G6.7 and G6.8 are addressed by the safety cage architecture that monitors input through out-of-distribution detection and rejects anomalies accordingly. The acceptable system response is to avoid emergency braking and instead let the human driver control ego car. 

# 5 ML Deployment Argument [HH]
SMIRK instantiates the ML Deployment Argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Deployment Argument Pattern [GG]](</docs/System%20Test%20Specification.md#4-ml-deployment-argument-pattern-gg>), as well as the following artefacts from preceding AMLAS activities:

- [System Safety Requirements](</docs/System Requirements Specification.md#31-system-safety-requirements-a->) [A]
- [Environment Description](</docs/System Requirements Specification.md#4-operational-design-domain-b->) [B]
- [System Description](</docs/System Requirements Specification.md#2-system-description-c->) [C]
- [ML Model](TBD) [V]
- [Erroneous Behaviour Log](TBD) [DD]
- [Operational Scenarios](</docs/System Requirements Specification.md#41-operational-scenarios-ee>) [EE]
- [Integration Testing Results](TBD) [FF]
