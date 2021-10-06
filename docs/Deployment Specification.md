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

The top claim (G6.1) is that the ML safety requirements SYS-ML-REQ1 and SYS-ML-REQ2 are satified when deployed to the ego car in which SMIRK operates. The argumentation strategy S6.1 is two-fold. First, sub-claim G6.2 is that the ML safety requirements are satisfied under all defined operating scenarios when the ML component is integrated into SMIRK in the context (C6.1) of the specified operational scenarios [EE]. Justification J6.1 explains that the scenarios were identified through an analysis of the SMIRK ODD. G6.2 has another sub-claim (G6.4) that the integration test results [FF] show that SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied. 

Second, sub-claim G6.3 argues that SYS-ML-REQ1 and SYS-ML-REQ2 continue to be satisfied during the operation of ego car. 

e safety requirements argument pattern [I], i.e., that all ML safety requirements are satisfied. The argumentation builds on a sub-claim and an argumentation strategy. First, sub-claim G5.2 is that the verification of the ML model is independent of its development. The verification log [AA] specifies how this has been achieved for SMIRK (Sn5.1). Second, the strategy S5.1 argues that test-based verification is an appropriate approach to generate evidence that the ML safety requirements are met. The justification is that the SMIRK test strategy follows the proposed organization in peer-reviewed literature on ML testing, which is a better fit than using less mature formal methods for ML models as complex as YOLO.

Following the test-based verification approach, the sub-claim G5.3 argues that that the ML model satisfies the ML safety requirement when the verification data (C5.1) is applied. The testing claim is supported by three sub-claims. First, G5.4 argues that the test results demonstrate that the ML safety requirements are satisfied, for which Verification Test Results [Z] are presented as evidence. Second, G5.5 argues that the Verification Data [P] is sufficient to verify the intent of the ML safety requirements in the ODD. Third, G5.6 argues that the test platform is representative of the operational platform. Evidence for both G5.5 and G5.6 is presented in the Verification Log [AA].

