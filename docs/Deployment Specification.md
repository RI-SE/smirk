# Deployment Specification v1.0

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
<td>Markus Borg</td>
<td>2022-06-16</td>
<td>Complete draft.</td>
<td>0.9</td>
</tr>
<tr>
<td>Markus Borg, Kasper Socha, Jens Henriksson</th>
<td>2022-06-16</th>
<td>Beta Release - Ready for peer-review</th>
<td>0.99</th>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</th>
<td>2022-12-19</th>
<td>Production Release - Peer-reviewed by Software Quality Journal according to Issue <a href="https://github.com/RI-SE/smirk/issues/27">#27</a>.</th>
<td>1.0</th>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the deployment specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC. As we run both the simulator and SMIRK on the same workstation, the deployment specification of the SMIRK MVP is different compared to the platform that would be used in a real vechicle, e.g., the NVIDIA DRIVE platform.

## 1.1 Purpose ##
This document describes the deployment of SMIRK on the experimental platform that runs ESI Pro-SiVIC. The pedestrian recognition component detects pedestrians in input images from the camera when the radar sensor indicates the risk of an immediate collision with an external object. In the SMIRK minimum viable product (MVP), no other classes but pedestrians are considered by the ML-based pedestrian recognition component. The document encompasses the entire lifecycle, i.e., data requirements and its justification report, data collection, data preprocessing, data validation, and data monitoring for SMIRK in operation.

The SMIRK *product goal* is to assist the driver on country roads in rural areas by performing emergency braking in the case of an imminent collision with a pedestrian. The *project goal* of the SMIRK development endeavor, as part of the research project SMILE3 is to provide a concrete ADAS case study as a basis for discussion - at the same time providing an open research prototype for the community. The goals are further elaborated in the [System Requirements Specification](</docs/System%20Requirements%20Specification.md#11-purpose>).

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts prescribed by the AMLAS process ([Guidance on the Assurance of Machine Learning in Autonomous Systems](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf)). Due to formatting limitations in GitHub MarkDown, all figure and table captions appear in italic font to distinguish them from the running text.

## 1.3 Glossary
- ADAS: Advanced Driver-Assistance Systems
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- AP: Average Precision
- FN: False Negatives
- FP: False Positives
- GSN: Goal Structuring Notation
- ML: Machine Learning
- MVP: Minimum Viable Product
- ODD: Operational Design Domain
- OOD: Out Of Distribution
- OSS: Open-Source Software
- PAEB: Pedestrian Automatic Emergency Braking

## 1.4 Intended Audience and Reading Suggestions ##
The section is organized into internal stakeholders, i.e., roles that are directly involved in the SMIRK development, and external stakeholders who are linked indirectly but have significant contribution in the successful completion of the SMIRK project. External stakeholders also include the ML safety community at large. Note that AMLAS prescribes a split between testers that are involved during the development and testers that are "sufficiently independent from the development activities." We refer to these roles as *internal testers* and *independent testers*, respectively.

**Internal stakeholders**

The entire document is relevant to the internal development organization. Specific stakeholders are recommended to pay particular attention as follows. 
- Software developers: The entire document is relevant.
- ML developers: The entire document is relevant.
- Internal testers: The entire document is relevant.
- Independent testers: The entire document is relevant.

**External stakeholders**
- Safety assessors: Focus on headings that map to the AMLAS process, indicated with letters in brackets.
- Researchers: Academic and industrial reserachers active in ML safety are likely to find the most value in the headings that map to the AMLAS process.
- Standardization bodies and legislators: An overview of the safety argumentation is presented in [Section 5 (ML Deployment Argument Pattern)](#5-ml-deployment-argument-pattern-gg-).
- Curious readers: The entire document is relevant

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)
- [ML Component Specification](</docs/ML Component Specification.md>)

# 3 Operating Environment <a name="env"></a>

# 4 Erroneous Behaviour Log [DD]
The development of the ML-based Pedestrian Recognition Component is undertaken in the context of assumptions that are made about the system to which it will be integrated and its ODD. The **safety cage** is a conrete mechanism implemenented to monitor that the assumptions reamain valid during SMIRK operation, i.e., it provides out-of-distribution detection. ML engineering always results in some level of uncertainty associated with the outputs produced by the ML models. During development, the safety cage supported our analysis of *erroneous output* from the [YOLOv5 model](https://github.com/RI-SE/smirk/releases/download/v1.0/pedestrian-detection-model.pt) embedded in the Pedestrian Recognition Component. Furthermore, the safety cage provided insights into what shall be considered *erroneous input* to the YOLOv5 model. As the SMIRK MVP has a restricted ODD, common types of noise and hardware sensor issues are out of scope - as are adversarial attacks. Still, this section reports the predicted and documented erroneous behaviours overall identified during development, as prescribed by AMLAS.

The [Internal Test Results [X]](https://github.com/RI-SE/smirk/blob/main/docs/protocols/Internal%20Test%20Results%20[X]%202022-06-16.pdf) and the [ML Verification Results [Z]](https://github.com/RI-SE/smirk/blob/main/docs/protocols/ML%20Verification%20Results%20[Z]%202022-06-16.pdf) show that the AP@0.5 are considerably lower for occluded pedestrians. As occlusion is an acknowledged challenge for object detection this is an expected result. The ML Verification Results also reveal that the number of FPs and FNs for the children is relatively high, resulting in slightly lower AP@0.5. We found that the problem with children is primarily far away, explained by the few pixels available for the object detection at long distances. While the SMIRK fulfils the robustness requirements within the ODD, we recognize this perception issue in the erroneous behavior log.

During the iterative SMIRK development, it became evident that OOD detection using the autoencoder was inadequate at close range. Figure 1 shows reconstruction errors (on the y-axis) for all objects in the validation subset of the development data at A) all distances, B) > 10 m, C) > 20 m, and D) > 30 m. The visualization clearly shows that the autoencoder cannot convincingly distinguish the cylinders from the pedestrians at all distances (in subplot A), different objects appear above the threshold), but the OOD detection is more accurate when objects at close distance are excluded (subplot D) displays high accuracy). Based on validation of the four distances, comparing the consequences of the trade-off between safety cage availability and accuracy, the design decision for SMIRK's autoencoder is to only perform OOD detection for objects that are at least 10 m away. We explain the less accurate behaviour at close range by limited training data, a vast majority of images contain pedestrians at a larger distance - which is reasonable since the SMIRK ODD is limited to rural country roads.

![VAE_Distance](/docs/figures/vae_distance.png) <a name="vae_distance"></a>

*Figure 1: Reconstruction errors for different objects on the validation subset of the development data at different distances from ego car (magenta=cylinder, yellow=female business casual, green=male business, orange=male casual). The dashed lines show the threshold for rejecting objects. In SMIRK, we use alternative B) in the safety cage.*

# 5 ML Deployment Argument Pattern [GG]
The figure below shows the ML deployment argument pattern using GSN. Since SMIRK is developed for a simulated environment, the pattern is adapted accordingly.

![GSN-ML-Deployment_Argument_Pattern](/docs/figures/gsn-ml_deployment_argument_pattern.png) <a name="gsn-ml_deployment_argument"></a>

*Figure 2: SMIRK ML Deployment Argument Pattern.*

The top claim (G6.1) is that the ML safety requirements SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied when deployed to the ego car in which SMIRK operates. The argumentation strategy S6.1 is two-fold. First, sub-claim G6.2 is that the ML safety requirements are satisfied under all defined operating scenarios when the ML component is integrated into SMIRK in the context (C6.1) of the specified operational scenarios [EE]. Justification J6.1 explains that the scenarios were identified through an analysis of the SMIRK ODD. G6.2 has another sub-claim (G6.4) that the integration test results [FF] show that SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied. 

Second, sub-claim G6.3 argues that SYS-ML-REQ1 and SYS-ML-REQ2 continue to be satisfied during the operation of SMIRK. The supporting argumentation strategy (S6.3) relates to the design of SMIRK and is again two-fold. First, sub-claim G6.6 argues that the operational achievement of the deployed component satisfies the ML safety requirements. Second, sub-claim G6.5 argues that the design of SMIRK into which the ML component is integrated ensures that SYS-ML-REQ1 and SYS-ML-REQ2 are satisfied throughout operation. The argumentation strategy (S6.4) is based on demonstrating that the design is robust by taking into account identified erroneous behavior in the context (C5.1) of the Erroneous Behavior Log [DD]. More specifically, the argumentation entails that predicted erroneous behavior will not result in the violation of the ML safety requirements. This is supported by two sub-claims, i.e., that the system design provides sufficient monitoring of erroneous inputs and outputs (G6.7) and that the system design provides acceptable response to erroneous inputs and outputs (G6.8). Both G6.7 and G6.8 are addressed by the safety cage architecture that monitors input through out-of-distribution detection and rejects anomalies accordingly. The acceptable system response is to avoid emergency braking and instead let the human driver control ego car. 

# 6 ML Deployment Argument [HH]
SMIRK instantiates the ML Deployment Argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Deployment Argument Pattern [GG]](</docs/System%20Test%20Specification.md#4-ml-deployment-argument-pattern-gg>), as well as the following artefacts from preceding AMLAS activities:

- [System Safety Requirements](</docs/System Requirements Specification.md#31-system-safety-requirements-a->) [A]
- [Environment Description](</docs/System Requirements Specification.md#4-operational-design-domain-b->) [B]
- [System Description](</docs/System Requirements Specification.md#2-system-description-c->) [C]
- [ML Model](https://github.com/RI-SE/smirk/releases/download/v1.0/pedestrian-detection-model.pt) [V]
- [Erroneous Behaviour Log](</docs/Deployment Specification.md#4-erroneous-behaviour-log-dd>) [DD]
- [Operational Scenarios](</docs/System Requirements Specification.md#41-operational-scenarios-ee>) [EE]
- [Integration Testing Results](https://github.com/RI-SE/smirk/blob/main/docs/protocols/Integration%20Testing%20Results%20[FF]%202022-06-16.pdf) [FF]
