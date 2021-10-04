# System Test Specification v0.2

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
<td>2021-10-04</th>
<td>Initial template.</th>
<td>0.1</th>
</tr>
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
This document containts the system test specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
This document describes the test strategy for the ML-based object detection component. The object detection component detects pedestrians in input images, i.e., no other classes are detected in the input.

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DM: Data Management
- ML: Machine Learning
- ODD: Operational Design Domain
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
The testing process must be independent from the development. Neither developers nor ML developers can have access to this document.

- Developers: Must not have access to the document.
- ML developers: Must not have access to the document.
- Testers: The entire document is important.
- Safety assessors: The entire document is important.
- Other stakeholders: TBD

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)

# 2 ML Test Strategy <a name="strategy"></a>
This section describes the overall ML test strategy.

# 3 ML Model Test Case Specifications

# 4 System Test Case Specifications

# 5 ML Verification Argument Pattern [BB]
The figure below shows the ML verification argument pattern using GSN. The pattern closely resembles the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Verification_Argument_Pattern](/docs/figures/gsn-ml_verification_argument_pattern.png) <a name="gsn-ml_verification_argument"></a>

The top claim (G5.1) corresponds to the bottom claim in the safety requirements argument pattern [I], i.e., that all ML safety requirements are satisfied. The argumentation builds on a sub-claim and an argumentation strategy. First, sub-claim G5.2 is that the verification of the ML model is independent of its development. The verification log [AA] specifies how this has been achieved for SMIRK (Sn5.1). Second, the strategy S5.1 argues that test-based verification is an appropriate approach to generate evidence that the ML safety requirements are met. The justification is that the SMIRK [test strategy](#real-cool-heading) follows the proposed organization in peer-reviewed literature on ML testing, which is a better fit than using less mature formal methods for ML models as complex as YOLO. 

Following the test-based verification approach, the sub-claim G5.3 argues that that the ML model satisfies the ML safety requirement when the verification data (C5.1) is applied. The testing claim is supported by three sub-claims. First, G5.4 argues that the test results demonstrate that the ML safety requirements are satisfied, for which Verification Test Results [Z] are presented as evidence. Second, G5.5 argues that the Verification Data [P] is sufficient to verify the intent of the ML safety requirements in the ODD. Third, G5.6 argues that the test platform is representative of the operational platform. Evidence for both G5.5 and G5.6 is presented in the Verification Log [AA].
