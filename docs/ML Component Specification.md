# Machine Learning Component Specification v0.2

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
<td>Markus Borg</td>
<td>2021-09-27</td>
<td>Toward a complete draft.</td>
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

# 5 ML Model Learning Argument Pattern [W]
The figure below shows the ML model learning argument pattern using GSN. The pattern closely resembles the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Model_Learning_Argument_Pattern](/docs/figures/gsn-model_learning_argument_pattern.png) <a name="gsn-ml_model_learning_argument"></a>

The top claim (G4.1) in this argument pattern is that the development of the learnt model [V] is sufficient. The strategy is to argue over the internal testing of the model and that the ML development was approriate (S4.1) in context of creating a valid model that meets practical constraints such as real-time performance and cost (C4.2). Sub-claim (G4.2) is that the ML model satisifies the ML safety requirements when using the internal test data [O]. We justify that the internal test results indicate that the ML model satisfies the ML safety requirements (J3.1) by presenting evidence from the internal test results [X].

Sub-claim G4.3 addresses the approach that was used when developing the model. The claim is supported by three claims regarding the type of model selected, the transfer learning process used, and the model parameters selected, respectively. First, G4.5 claims that the type of model is appropriate for the specified ML safety requirements and the other model constraints. Second, G4.6 claims that the process followed to allow transfer learning is appropriate. ML development processes, including transfer learning, are highly iterative thus rationales for development decisions must be recorded. Third, G4.7 claims that the parameters of the ML model are appropiately selected to tune performance toward the object detection task in the specified ODD. Rationales for any decisions in G4.5-G4.7 are recorded in the model development log [U].

