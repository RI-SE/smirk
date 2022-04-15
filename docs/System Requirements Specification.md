# System Requirements Specification v0.96

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
<td>2021-05-13</th>
<td>Initialized using IEEE SRS template.</th>
<td>0.1</th>
</tr>
<tr>
<td>Markus Borg</td>
<td>2021-09-03</td>
<td>Initial version to discuss at AMLAS workshop.</td>
<td>0.2</td>
</tr>
<tr>
<td>Markus Borg, Jens Henriksson</td>
<td>2021-10-18</td>
<td>Complete draft.</td>
<td>0.3</td>
</tr>
<tr>
<td>Jens Henriksson, Kasper Socha</td>
<td>2021-11-05</td>
<td>Updated after internal review.</td>
<td>0.4</td>
</tr>
<tr>
<td>Markus Borg</td>
<td>2021-11-08</td>
<td>Ready for Fagan inspection.</td>
<td>0.9</td>
</tr>
<tr>
<td>Markus Borg</td>
<td>2021-11-23</td>
<td>Updated according to 
<a href="https://github.com/RI-SE/smirk/blob/main/docs/protocols/SRS%20Inspection%20Protocol%202021-11-15.xlsx">inspection protocol</a>.
</td>
<td>0.91</td>
</tr>
<tr>
<td>Markus Borg</td>
<td>2022-02-16</td>
<td>Updated according to Issues <a href="https://github.com/RI-SE/smirk/issues/8">#8</a>, <a href="https://github.com/RI-SE/smirk/issues/9">#9</a>, and <a href="https://github.com/RI-SE/smirk/issues/10">#10</a>.
</td>
<td>0.92</td>
</tr>
<tr>
<td>Markus Borg</td>
<td>2022-03-05</td>
<td>Updated according to Issues <a href="https://github.com/RI-SE/smirk/issues/11">#11</a> and <a href="https://github.com/RI-SE/smirk/issues/12">#12</a>.
</td>
<td>0.93</td>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</td>
<td>2022-03-15</td>
<td>Updated according to Issues <a href="https://github.com/RI-SE/smirk/issues/13">#13</a> and <a href="https://github.com/RI-SE/smirk/issues/14">#14</a>.
</td>
<td>0.94</td>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</td>
<td>2022-04-14</td>
<td>Updated according to Issues <a href="https://github.com/RI-SE/smirk/issues/16">#16</a> and <a href="https://github.com/RI-SE/smirk/issues/17">#17</a>.
</td>
<td>0.95</td>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</td>
<td>2022-04-15</td>
<td>Updated according to Issues <a href="https://github.com/RI-SE/smirk/issues/13">#13</a>, <a href="https://github.com/RI-SE/smirk/issues/14">#14</a>, and <a href="https://github.com/RI-SE/smirk/issues/19">#19</a>.
</td>
<td>0.96</td>
</tr>
</table>

# 1 Introduction
This system requirements specification (SRS) contains the system requirements for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic. SMIRK, including the accompanying safety case, is developed with full transparency under an open-source software (OSS) license. We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
The SMIRK *product goal* is to assist the driver on country roads in rural areas by performing emergency braking in the case of an imminent collision with a pedestrian. The level of automation offered by SMIRK corresponds to SAE Level 1 - Driver Assistance, i.e., "the driving mode-specific execution by a driver assistance system of either steering or acceleration/deceleration." SMIRK is developed with a focus on evolvability, thus future versions might include steering and thus comply with SAE Level 2. This document provides the foundation for the SMIRK minimum viable product (MVP), i.e., an implementation limited to a highly restricted operational design domain (ODD).

The *project goal* of the SMIRK development endeavor, as part of the research project SMILE3, is twofold. First, the project team will benefit substantially from having a concrete example of ADAS development as a basis for discussion. We will all learn how challenging it is to perform safety case development for ML-based perception systems by practically doing it for the SMIRK MVP. Nothing can substitute the experience of a hands-on engineering effort. Second, SMIRK will be provided as a completely open research prototype that can be used as a case under study in future research studies. As we keep expanding the ODD beyond the MVP limitations, the SMIRK ADAS can be used to study various aspects of AI engineering. For our subsequent research projects, we expect to primarily study the efficiency and effectiveness of various solution proposals related to software testing, verification, and validation.

## 1.2 Document Conventions ##
This document largely follows the structure proposed in [IEEE 830-1998 - IEEE Recommended Practice for Software Requirements Specifications](https://standards.ieee.org/standard/830-1998.html) and the [template](https://www.modernanalyst.com/Resources/Templates/tabid/146/ID/497/Karl-Wiegers-Software-Requirements-Specification-SRS-Template.aspx) provided by Wiegers. While the standard has been replaced by [ISO/IEC/IEEE 29148:2011](https://www.iso.org/standard/45171.html), the old standard serves the SMIRK development well.

The number of academic publications in the list of references is unconventional for techincal project doumentation. This is a conscious decision. SMIRK is developed as a prototype in the context of a research project with limited resources. As part of our research, we aim to integrate (sometimes scattered) pieces from the state-of-the-art literature. Synthesis is a fundamental tool in our research and we seek novel insights while focusing on refinement and integration. We actively choose to rely on reuse of design decisions from previously peer-reviewed publications. Building on previous work, i.e., [standing on the shoulders of others](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants), is a core concept in research that allows validation of previous work, incl. previously proposed requirements. When available, and unless open access publication models have been used, links to academic publications point to preprints on open repositories such as [arXiv](https://arxiv.org/) rather than peer-reviewed revisions behind paywalls.

Headings with a reference in brackets [X] refer to artifacts prescribed by the AMLAS process ([Guidance on the Assurance of Machine Learning in Autonomous Systems](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf)). Due to formatting limitations in GitHub MarkDown, all figure and table captions appear in italic font to distinguish them from the running text. Explanatory text copied verbatim from public documents are highlighted using the quote formatting available in GitHub Markdown.

## 1.3 Glossary
- ADAS: Advanced Driver-Assistance Systems
- API: Application Programming Interface
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DDS: Data Distribution Service
- DNN: Deep Neural Network
- FPS: Frames Per Second
- GSN: Goal Structuring Notation
- HARA: Hazard and Risk Analysis
- ML: Machine Learning
- MVP: Minimum Viable Product
- ODD: Operational Design Domain
- OOD: Out Of Distribution
- OSS: Open-Source Software
- PAEB: Pedestrian Automatic Emergency Braking
- SAE: (Formerly) Society of Automotive Engineers. Now known as [SAE International](https://www.sae.org/).
- TCP: Transmission Control Protocol
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
The section is organized into internal stakeholders, i.e., roles that are directly involved in the SMIRK development, and external stakeholders who are linked indirectly but have significant contribution in the successful completion of the SMIRK project. External stakeholders also include the ML safety community at large. Note that AMLAS prescribes a split between testers that are involved during the development and testers that are "sufficiently independent from the development activities." We refer to these roles as *internal testers* and *independent testers*, respectively.

**Internal stakeholders**

The entire document is relevant to the internal development organization. Specific stakeholders are recommended to pay particular attention as follows. 
- Software developers: [Section 3 (System Requirements)](#3-system-requirements)
- ML developers: [Section 3.2 (Safety Requirements Allocated to ML Component)](#32-safety-requirements-allocated-to-ml-component-e-)
- Internal testers: [Section 3 (System Requirements)](#3-system-requirements).
- Independent testers: [Section 3 (System Requirements)](#3-system-requirements) and [Section 4 (Operational Design Domain)](#4-operational-design-domain-b-).

**External stakeholders**
- Safety assessors: Focus on headings that map to the AMLAS process, indicated with letters in brackets.
- Researchers: Academic and industrial reserachers active in ML safety are likely to find the most value in [Section 3 (System Requirements)](#3-system-requirements).
- Standardization bodies and legislators: An overview of the safety argumentation is presented in [Section 5 (ML Assurance Scoping Argument Pattern)](#5-ml-assurance-scoping-argument-pattern-f-).
- Curious readers: For an overview of SMIRK, read [Section 1 (Introduction)](#1-introduction) and [Section 2 (System Description)](#2-system-description-c-).

## 1.5 Product Scope ##
SMIRK is an ADAS that is intended to co-exist with other ADAS in a vehicle. We expect that sensors and actuators will be shared among different systems. SMIRK currently implements its own perception system based on radar and camera input. In future versions, it is likely that a central perception system operating on the vehicle will provide reliable input to SMIRK. This is not yet the case for the SMIRK MVP and this version of the SRS does not specify any requirements related to shared resources. The SMIRK scope is further explained through the context diagram in [Section 2.1](#21-product-perspective).

Product development inevitably necessitates quality trade-offs. While we have not conducted a systematic quality requirements prioritization, such as an analytical hierarchy process workshop (Kassab and Kilicay-Ergin, 2015), this section shares our general aims with SMIRK. The software product quality model defined in the ISO/IEC 25010 standard consists of eight characteristics. Furthermore, as recommend in requirements engineering research (Horkoff, 2019), we add the two novel quality characteristics explainability and fairness. For each characteristic, we share how important it is considered during the development and assign it a low, medium or high priority. Our priorities influence architectural decisions in SMIRK and support elicitation of architecturally significant requirements (Chen et al., 2012).

- **Functional suitability**: No matter how functionally restricted the SMIRK MVP is, it must meet the stated and implied needs of a prototype ADAS. This quality characteristic is fundamentally important. **[High priority]**
- **Performance efficiency**: When deployed in the simulated environment, SMIRK must be able to process input, conduct ML inference, and possibly commission emergency braking in realistic driving scenarios. As a real-time system, SMIRK must be sufficiently fast and finding when performance efficiency reached excessive levels is vital in the requirements engineering process. **[Medium priority]**
- **Compatibility**: A product goal is to make SMIRK compatible with other ADAS. So far we have not explored this further, thus this is a primarily an ambition beyond the MVP development. **[Low priority]**
- **Usability**: SMIRK is an ADAS that operates in the background and ideally never intervenes in the dynamic driving task. SMIRK does not have a user interface for the direct driver interaction. **[Low priority]**
- **Reliability**: A top priority in the SMIRK development that motivates the application of AMLAS. Note, however, that safety is not covered in the ISO/IEC 25010 product quality model but in its complementary quality-in-use model. **[High priority]**
- **Security**: Not prioritized in the SMIRK MVP. ISO/PAS 21448 is limited to "reasonably foreseeable misuse" but does not address antagonistic attacks. While safety and security shall be co-engineered, we leave this quality characteristic as future work. **[Low priority]**
- **Maintainability**: As mentioned in [Section 1.1 Purpose](#11-purpose), evolvability from the SMIRK MVP is a key concern. Consequently, maintainability is important, although not more important than functional suitability and reliability. **[Medium priority]**
- **Portability**: We aim to develop SMIRK in a manner that allows porting the ADAS to both other simulated environments and to physical demonstration platforms in future projects. We consider this  quality characteristic during the SMIRK development, but it is not a primary concern. **[Low priority]**
- **Explainability**: Explainability is an important characteristic for any cyber-physical system, but the challenge grows with the introduction of DNNs. There is considerable research momentum on “Explainable AI” and we expect that new findings will be applicable to SMIRK. For the MVP development, however, our explainability focus is restricted to the auditability resulting in following AMLAS. **[Medium priority]**
- **Fairness**: Obviously a vital quality characteristic for a PAEB ADAS that primarily impacts the data requirements specified in the [Data Management Specification](</docs/Data Management Specification.md>). We have elaborated on SMIRK fairness in an academic publication (Borg et al., 2021). **[High priority]**

## 1.6 References ##
The references are organized into 1) internal SMIRK documentation, 2) peer-reviewed publications, and 3) gray literature and white papers. When a reference listed under category 2) or 3) is used to motivate a design decision or a specific requirement, there is an explicit reference in the running text. Note that this SRS is self-contained, the references are provided for traceability to the underlying design rationales. Interested readers are referred to the discussions in the original sources.

**Internal SMIRK documentation**
- [Data Management Specification](</docs/Data Management Specification.md>)
- [System Architecture Description](</docs/System Architecture Description.md>)

**Peer-reviewed publications**
- Ben Abdessalem, Nejati, Briand, and Stifter, 2016. [Testing Advanced Driver Assistance Systems using Multi-objective Search and Neural Networks](https://core.ac.uk/download/pdf/42923634.pdf), in *Proc. of the 31st IEEE Conference on Automated Software Engineering*, pp. 63-74.
- Borg, Bronson, Christensson, Olsson, Lennartsson, Sonnsjö, Ebadi, and Karsberg, 2021. [Exploring the Assessment List for Trustworthy AI in the Context of Advanced Driver-Assistance Systems](https://arxiv.org/abs/2103.09051), In *Proc. of the 2nd IEEE/ACM International Workshop on Ethics in Software Engineering Research and Practice*, pp. 5-12.
- Chen, Babar, and Nuseibeh, 2012. [Characterizing Architecturally Significant Requirements](https://core.ac.uk/download/pdf/59350157.pdf), *IEEE Software*, 30(2), pp. 38-45.
- Gauerhof, Hawkins, David, Picardi, Paterson, Hagiwara, and Habli, 2020. [Assuring the Safety of Machine Learning for Pedestrian Detection at Crossings](https://link.springer.com/chapter/10.1007/978-3-030-54549-9_13). In *Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP)*.
- Hawkins, Paterson, Picardi, Jia, Calinescu, and Habli, 2021. [Guidance on the Assurance of Machine Learning in Autonomous Systems (AMLAS)](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf), v1.1, Techincal Report, University of York.
- Henriksson, Berger, Borg, Tornberg, Englund, Sathyamoorthy, and Ursing, 2019. [Towards Structured Evaluation of Deep Neural Network Supervisors](https://arxiv.org/abs/1903.01263), In *Proc. of the International Conference On Artificial Intelligence Testing*, pp. 27-34.
- Henriksson, Berger, Borg, Tornberg, Sathyamoorthy, and Englund, 2021. [Performance Analysis of Out-of-Distribution Detection on Trained Neural Networks](https://arxiv.org/abs/2103.15580). *Information and Software Technology*, 130.
- Horkoff, 2019. [Non-functional Requirements for Machine Learning: Challenges and New Directions](http://www.cse.chalmers.se/~jenho/PaperFiles/NFRsforMLRENext.pdf). In *Proc. of the 2019 IEEE 27th International Requirements Engineering Conference*, pp. 386-391.
- Kassab and Kilicay-Ergin, 2015. [Applying Analytical Hierarchy Process to System Quality Requirements Prioritization](https://link.springer.com/article/10.1007/s11334-015-0260-8). *Innovations in Systems and Software Engineering*, 11(4), pp. 303-312.

**Gray literature and white papers**
- International Organization for Standardization, [ISO/PAS 21448:2019](https://www.iso.org/standard/70939.html) Road vehicles — Safety of the intended functionality 
- Object Management Group (OMG), [Data Distribution Service (DDS)](https://www.dds-foundation.org/what-is-dds-3/), Last checked: 2021-09-09.
- The Assurance Case Working Group (ACWG), 2018. [Goal Structuring Notation Community Standard](https://scsc.uk/r141B:1?t=1), Version 2, SCSC-141B. 
- Thorn, Kimmel, and Chaka, 2018. [A Framework for Automated Driving System Testable Cases and Scenarios](https://trid.trb.org/view/1574670), Technical Report DOT HS 812 623, National Highway Traffic Safety Administration.

# 2 System Description [C] <a name="system_reqts"></a>
SMIRK is an OSS ML-based ADAS. The SMIRK MVP is a research prototype that provides PAEB that adheres to development practices mandated by the candidate standard ISO 21448. To ensure industrial relevance, SMIRK builds on the reference architecture from PeVi, an ADAS studied in previous work (Ben Abdessalem *et al.*, 2016). SMIRK uses a radar sensor and a camera to detect pedestrians on collision course and commissions emergency braking when needed. The system combines Python source code, a radar sensor providing object detection, and a trained deep neural network (DNN) for pedestrian detection and recognition. SMIRK demonstrates safety-critical ML-based driving automation on SAE Level 1.

The SMIRK system architecture is further described in the [System Architecture Description](</docs/System Architecture Description.md>).

## 2.1 Product Perspective ##
SMIRK is designed to send a brake signal when a collision with a pedestrian is imminent. Figures 1 to 7 illustrate the overall function provided by SMIRK, i.e., they should be interpreted as high-level descriptions of the product. Figures 1-2 depict two standard scenarios in which pedestrians the pedestrian crosses the road. Figures 3-4 show two scenarios with a pedestrian walking on the road, toward and away from ego car, respectively. Figure 5 shows a stationary pedestrian on the road, i.e., a scenario known to be difficult for some pedestrian detection systems. Figure 5 presents a general scenario to highlight that SMIRK can handle arbitrary angles, i.e., not only perpendicular movement. Finally, Figure 7 stresses that SMIRK is robust against false positives, also know as "braking for ghosts." Trajectories are illustrated with blue arrows accompanied by a speed (*v*) and possibly an angle (*θ*). *c* and *p* in the superscript denotes car and pedestrian, respectively, and *0* in the subscript indicates initial speed.

![Scenario1](/docs/figures/scenario1.png) <a name="scenario1"></a>

*Figure 1: Example scenario with pedestrian crossing the road from the right.*

![Scenario2](/docs/figures/scenario2.png) <a name="scenario2"></a>

*Figure 2: Example scenario with pedestrian crossing the road from the left.*

![Scenario3](/docs/figures/scenario3.png) <a name="scenario3"></a>

*Figure 3: Example scenario with pedestrian moving on the road toward ego car.*

![Scenario4](/docs/figures/scenario4.png) <a name="scenario4"></a>

*Figure 4: Example scenario with pedestrian moving on the road away from ego car.*

![Scenario5](/docs/figures/scenario5.png) <a name="scenario5"></a>

*Figure 5: Example scenario with a stationary pedestrian on the road.*

![Scenario6](/docs/figures/scenario6.png) <a name="scenario6"></a>

*Figure 6: Example scenario illustrating a pedestrian crossing the road at an arbitrary angle.*

![Scenario7](/docs/figures/scenario7.png) <a name="scenario7"></a>

*Figure 7: Example scenario illustrating that ego car shall not commence PAEB for false positives.*

The figure below shows a SMIRK context diagram. The sole purpose of SMIRK is PAEB. The design of SMIRK assumes that it will be deployed in a vehicle with complementary ADAS, e.g., large animal detection, lane keeping assistance, and various types of collision avoidance (cf. "Other ADAS 1 - N"). We also expect that sensors and actuators will be shared between ADAS. For the SMIRK MVP, however, we do not elaborate any further on ADAS co-existence and we do not adhere to any particular higher-level automotive architecture. In the same vein, we do not assume a central perception system that fuses various types of sensor input for individual ADAS such as SMIRK to use. SMIRK uses a standalone ML model trained for pedestrian detection and recognition. In the SMIRK terminology, to mitigate confusion, the radar *detects* objects and the ML-based pedestrian recognition component *identifies* potential pedestrians in the camera input. Solid lines in the figure show how SMIRK interacts with sensors and actuators in ego car. Dashed lines indicate how other ADAS might use sensors and actuators.

![Context](/docs/figures/context_diagram.png) <a name="context"></a>

*Figure 7: SMIRK context diagram.*

## 2.2 Product Functions ##
SMIRK comprises implementations of four algorithms and uses external vehicle functions. In line with ISO 21448, we organize all constituents into the categories sensors, algorithms, and actuators.

Sensors:
- Radar detection and tracking of objects in front of the vehicle (further details in the [System Architecture Description](</docs/System Architecture Description.md#31-logical-view>)).
- A forward-facing mono-camera (further details in the [System Architecture Description](</docs/System Architecture Description.md#31-logical-view>)).

Algorithms:
- Time-to-collision (TTC) calculation for objects on collision course (threshold 4 s).
- Pedestrian detection and recognition based on the camera input where the radar detected an object. 
- Out-of-distribution (OOD) detection of never-seen-before input (part of the [safety cage mechanism](</docs/ML%20Component%20Specification.md#4-outlier-detection-for-the-safety-cage-architecturesafety-cage>)). 
- A braking module that commissions emergency braking. In the MVP, maximum braking power is always used.

Actuators:
- Brakes (provided by ESI Pro-SiVIC, not elaborated further).

The figure below illustrates detection of a pedestrian on a collision course, i.e., automatic emergency braking shall be commenced. The ML-based functionality of pedestrian detection and recognition, including the corresponding OOD detection, is embedded in the **Pedestrian Recognition Component**.

![pedestrian_detection](/docs/figures/pedestrian_detection.png) <a name="pedestrian_detection"></a>

*Figure 8: Illustrative example of pedestrian detection.*

## 2.3 External Interface Requirements ##
SMIRK and ESI Pro-SiVIC communicate through two different python APIs provided by ESI, the Pro-SiVIC TCP remote controls API, and the Pro-SiVIC DDS API. OMG Data Distribution Service (DDS) is a middleware protocol and API standard for data-centric connectivity from the Object Management Group. In summary,

- SMIRK is developed for ESI Pro-SiVIC 2020.0 64-bit.
- All dynamic Pro-SiVIC setup is communicated as Pro-SiVIC commands over TCP.
- Scenarios are started over TCP.	
- All subsequent data communication, i.e., live data during the simulation, is transferred over DDS through the Python API.

# 3 System Requirements
This section specifies the SMIRK system requirements, organized into system safety requirements and ML safety requirements. ML safety requirements are further refined into performance requirements and robustness requirements. The requirements are largely inspired by Gauerhof *et al.* (2020).

## 3.1 System Safety Requirements [A] <a name="system_safety_reqts"></a>
This section specifies the highest level SMIRK requirement.

- **SYS-SAF-REQ1: SMIRK shall commence automatic emergency braking if and only if collision with a pedestrian on collision course is imminent.**

Rationale: This is the main purpose of SMIRK. If possible, ego car will stop and avoid a collision. If a collision is inevitable, ego car will reduce speed to decrease the impact severity. Hazards introduced from false positives, i.e., braking for ghosts, are mitigated under ML Safety Requirements.

## 3.2 Safety Requirements Allocated to ML Component [E] <a name="ml_component_safety_reqts"></a>
Based on a Hazard Analysis and Risk Assessment (HARA), two categories of hazards were identified. First, SMIRK might miss pedestrians and fail to commence emergency braking - we refer to this as a *missed pedestrian*. Second, SMIRK might commence emergency braking when it should not - we refer to this as an instance of *ghost braking*. A summary of the HARA is presented below.

- **Missed pedestrian hazard**: The severity of the hazard is very high (high risk of fatality). Controllability is high since the driver can brake ego car.
- **Ghost braking hazard**: The severity of the hazard is high (can be fatal). Controllability is very low since the driver would have no chance to counteract the braking. 
 
To conclude, we refine SYS-SAF-REQ1 in the next section to specify requirements in relation to the missed pedestrian hazard. Furthermore, the ghost braking hazard necessitates the introduction of SYS-ML-REQ2.

## 3.3 Machine Learning Safety Requirements [H] <a name="ml_safety_reqts"></a>
This section refines SYS-SAF-REQ into two separate requirements corresponding to missed pedestrians and ghost braking, respectively.

- **SYS-ML-REQ1: The pedestrian recognition component shall identify pedestrians in all valid scenarios when the radar tracking component returns a TTC < 4s for the corresponding object.**
- **SYS-ML-REQ2: The pedestrian recognition component shall reject false positive input that does not resemble the training data.**

Rationale: SYS-SAF-REQ1 is interpreted in the light of missed pedestrians and ghost braking and then broken down into the separate ML safety requirements SYS-ML-REQ1 and SYS-ML-REQ2. The former requirement deals with the "if" aspect of SYS-SAF-REQ1 whereas its "and only if" aspect is targetted by SYS-SAF-REQ2. SMIRK follows the reference architecture from Ben Abdessalem *et al.* (2016) and SYS-ML-REQ1 uses the same TTC threshold (4 seconds, confirmed with the original authors). We have confirmed that the TTC threshold is valid for SMIRK in its [Operational Design Domain](#odd). SYS-ML-REQ2 motivates the primary contribution of the SMILE projects, i.e., an out-of-distribution detection mechanism that we refer to as a safety cage.

## 3.3.1 Performance Requirements
This section specifies performance requirements corresponding to the ML safety requirements with a focus on quantitative targets for the pedestrian recognition component. All requirements below are restricted to pedestrians on or close to the road.

**For objects detected by the radar tracking component with a TTC < 4s, the following requirements must be fulfilled:**

- **SYS-PER-REQ1: The pedestrian recognition component shall identify pedestrians with a true positive rate of 93% when they are within 80 m.**
- **SYS-PER-REQ2: The false negative rate of the pedestrian recognition component shall not exceed 7% within 50 m.**
- **SYS-PER-REQ3: The false positive per image of the pedestrian recognition component shall not exceed 0.1% within 80 m.** 
- **SYS-PER-REQ4: In any sequence of 5 consecutive frames from a 10 FPS video feed, no pedestrian within 80 m shall be missed in more than 20% of the frames.**
- **SYS-PER-REQ5: For pedestrians within 80 m, the pedestrian recognition component shall determine the position of pedestrians within 50 cm of their actual position.**
- **SYS-PER-REQ6: The pedestrian recognition component shall allow an inference speed of at least 10 FPS in the ESI Pro-SiVIC simulation.**

Rationale: SMIRK adapts the performance requirements specified by Gauerhof *et al.* (2020) for the SMIRK ODD. SYS-PER-REQ1 reuses the threshold from Example 7 in AMLAS, but clarifies that we consider accuracy as the true positive rate. SYS-PER-REQ2 and SYS-PER-REQ3 are two additional requirements inspired by Henriksson *et al.* (2019). Note that SYS-PER-REQ3 relies on the metric false positive per image rather than false positive rate as true negatives do not exist for object detection. SYS-PER-REQ6 means that any further improvements to reaction time have a negligible impact on the total brake distance. 

## 3.3.2 Robustness Requirements
This section specifies robustness requirements corresponding to the ML safety requirements.

**For pedestrians present within 80 m of ego car, captured in the field of view of the camera:**

- **SYS-ROB-REQ1: The pedestrian recognition component shall perform as required in all situations ego car may encounter within the defined ODD.**
- **SYS-ROB-REQ2: The pedestrian recognition component shall identify pedestrians irrespective of their upright pose with respect to the camera.**
- **SYS-ROB-REQ3: The pedestrian recognition component shall identify pedestrians irrespective of their size with respect to the camera.**
- **SYS-ROB-REQ4: The pedestrian recognition component shall identify pedestrians irrespective of their appearance with respect to the camera.**

Rationale: SMIRK reuses robustness requirements for pedestrian detection from previous work. SYS-ROB-REQ1 is specified in Gauerhof *et al.* (2020). SYS-ROB-REQ2 is presented as Example 7 in AMLAS, which has been limited to upright poses, i.e., SMIRK is not designed to work for pedestrians sitting or lying on the road. SYS-ROB-REQ3 and SYS-ROB-REQ4 are additions identified during the [Fagan inspection](/docs/protocols/SRS%20Inspection%20Protocol%202021-11-15.xlsx). 

# 4 Operational Design Domain [B] <a name="odd"></a>
This section specifies the SMIRK operational design domain (ODD). The ODD specification is based on the taxonomy developed by NHTSA (Thorn *et al.*, 2018) and the introductory text for each ODD category originates in the same technical report. Note that the ODD is deliberately restricted to allow rapid prototyping of a SMIRK MVP.

## 4.1 Physical Infrastructure
>Physical infrastructure refers to facilities and systems that serve a country, city, or area and enable its economy to function. Physical infrastructure is typically characterized by technical structures, such as roads, bridges, tunnels, water supply, sewers, electrical grids, telecommunications, etc., that are for the most part interrelated. ADAS features may depend on such infrastructure elements, which are a critical part of the ODD environment. (Thorn *et al.*, 2018)

*Table 1: Roadway Types.*
<table>
<thead>
  <tr>
    <th colspan="2">Roadway Types</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Divided highway</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Undivided highway</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Arterial</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Urban</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Rural</td>
    <td>Y (open green fields)</td>
  </tr>
  <tr>
    <td>Parking (surface lots, structures, private/public)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Bridges</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Multi-lane/single lane</td>
    <td>Single lane</td>
  </tr>
  <tr>
    <td>Managed lanes (HOV, HOT, etc.)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>On-off ramps</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Emergency evacuation routes</td>
    <td>N</td>
  </tr>
  <tr>
    <td>One way</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Private roads</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Reversible lanes</td>
    <td>N</td>
  </tr>
  <tr>
    <td colspan="2">Intersection Types</td>
  </tr>
  <tr>
    <td>signaled</td>
    <td>N</td>
  </tr>
  <tr>
    <td>U-turn</td>
    <td>N</td>
  </tr>
  <tr>
    <td>4-way vs. 3-way vs. 2-way</td>
    <td>N</td>
  </tr>
  <tr>
    <td>stop sign</td>
    <td>N</td>
  </tr>
  <tr>
    <td>roundabout</td>
    <td>N</td>
  </tr>
  <tr>
    <td>merge lanes</td>
    <td>N</td>
  </tr>
  <tr>
    <td>left turn across traffic, one-way to one-way</td>
    <td>N</td>
  </tr>
  <tr>
    <td>right turn</td>
    <td>N</td>
  </tr>
  <tr>
    <td>multiple turn lane</td>
    <td>N</td>
  </tr>
  <tr>
    <td>crosswalk</td>
    <td>N</td>
  </tr>
  <tr>
    <td>toll plaza</td>
    <td>N</td>
  </tr>
  <tr>
    <td>railroad crossing</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
</table>

*Table 2: Roadway Surfaces.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Surfaces</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Asphalt</td>
    <td>Y</td>
  </tr>
  <tr>
    <td>Concrete<br></td>
    <td>N</td>
  </tr>
  <tr>
    <td>Mixed</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Grating</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Brick</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Dirt</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Gravel</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Scraped road</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Partially occluded</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Speed bumps</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Potholes</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Grass</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 3: Roadway Edges and Markings.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Edges and Markings</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Lane markers</td>
    <td>Clear markers</td>
  </tr>
  <tr>
    <td>Temporary lane markers</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Shoulder (paved or gravel)</td>
    <td>Gravel</td>
  </tr>
  <tr>
    <td>Lane barriers</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Grating</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Rails</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Curb</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Cones</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 4: Roadway Geometry.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Geometry</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Straightaways</td>
    <td>Y</td>
  </tr>
  <tr>
    <td>Curves</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Hills</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Lateral crests</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Corners (regular, blind)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Negative obstacles</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Lane width</td>
    <td>4-8 m</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
</tbody>
</table>

## 4.2 Operational Constraints
>There are several operational constraints that need to be considered when designing and testing ADAS applications. These include elements such as dynamic changes in speed limits, traffic characteristics, construction, etc. For example, an ADAS entering a school zone is subjected to lower speed limits and must respond appropriately to ensure the safety of its passengers and other road users. (Thorn *et al.*, 2018)

*Table 5: Speed Limits.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Speed Limits</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Minimum Speed Limit</td>
    <td>0 km/h</td>
  </tr>
  <tr>
    <td>Maximum Speed Limit</td>
    <td>70 km/h</td>
  </tr>
  <tr>
    <td>Relative to Surrounding Traffic</td>
    <td>No surrounding traffic</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 6: Traffic Conditions.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Traffic Conditions</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Traffic density</td>
    <td>No other traffic</td>
  </tr>
  <tr>
    <td>Altered (Accident emergency vehicle, construction, closed road, special event)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.3 Objects
>For an ADAS to properly navigate within an ODD, it must detect and respond to certain objects. This category of the ODD identifies objects that can reasonably be expected to exist within the ODD. For example, a pedestrian may be expected at an intersection but rarely on a freeway. (Thorn *et al.*, 2018)

*Table 7: Signage.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Signage</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Signs (e.g., stop, yield, pedestrian, railroad, school zone, etc.)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Traffic Signals (regular, flashing, school zone, fire dept. zone)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Crosswalks</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Railroad crossing</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Stopped buses</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Construction signage</td>
    <td>N</td>
  </tr>
  <tr>
    <td>First responder signals  </td>
    <td>N</td>
  </tr>
  <tr>
    <td>Distress signals</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Roadway user signals</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Hand signals</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
</tbody>
</table>

*Table 8: Roadway Users.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Roadway Users</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Vehicle types (cars, light trucks, large trucks, buses, motorcycles, wide-load, emergency vehicles, construction or farming equipment, horse-drawn carriages/buggies)</td>
    <td>No other vehicles</td>
  </tr>
  <tr>
    <td>Stopped vehicles</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other automated vehicles</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Pedestrians</td>
    <td>0-1 pedestrians, either stationary or moving with a constant speed (<15 km/h) and direction </td>
  </tr>
  <tr>
    <td>Cyclists</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 9: Non-Roadway Users Obstacles.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Non-Roadway Users Obstacles</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Animals (e.g., dogs, deer, etc.)</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Shopping carts</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Debris (e.g., pieces of tire, trash, ladders)</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.4 Connectivity
>Connectivity and automation are increasingly being integrated into cars and trucks with the objective of improving safety, mobility, and providing a better driving experience. Connectivity is an enabling technology that may define where an ADS feature can operate. For example, low-speed shuttles may depend on traffic light signal phase and timing messages to reduce the dependence on sensors alone to detect the signal. (Thorn *et al.*, 2018)

SMIRK does not rely on any external connectivity. All items below are either N or N/A.

*Table 10: Vehicles.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Vehicles</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>V2I and V2V communications</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Emergency vehicles</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 11: Remote Fleet Management System.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Remote Fleet Management System</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Does the system require an operations center?</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Does remote operation expand ODD or support fault handling?</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 12: Infrastructure Sensors.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Infrastructure Sensors</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Work zone alerts</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Vulnerable road user</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Routing and incident management</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 13: Digital Infrastructure.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Digital Infrastructure</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>GPS</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>3-D Maps</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Pothole Locations</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Weather Data</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Infrastructure Data</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.5 Environmental Conditions
>Environmental conditions play a crucial role in the safe operation of a variety of ADAS applications, and pose one of the biggest challenges to deployment
, particularly early deployment. The environment can impact visibility, sensor fidelity, vehicle maneuverability, and communications systems. Today, ADAS technologies are tested most often in clear, rather than adverse, weather conditions. (Thorn *et al.*, 2018)
 
 *Table 14: Weather.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Weather</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Wind</td>
    <td>Calm winds (< 0.5 m/s)</td>
  </tr>
  <tr>
    <td>Rain</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Snow</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Sleet</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Temperature</td>
    <td>Between 5 and 30 degree Celsius</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 15: Weather-Induced Roadway Conditions.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Weather-Induced Roadway Conditions</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Standing Water</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Flooded Roadways</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Icy Roads</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Snow on Road</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 16: Particulate Matter.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Particulate Matter</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Fog</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Smoke</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Smog</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Dust/Dirt</td>
    <td>N</td>
  </tr>
  </tr>
    <tr>
    <td>Mud</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 17: Illumination.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Illumination</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Day (sun: Overhead, Back-lighting and Frontlighting)</td>
    <td>Y, overhead sun</td>
  </tr>
  <tr>
    <td>Dawn</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Dusk</td>
    <td>N</td>
  </tr>
    <tr>
    <td>Night</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Street lights</td>
    <td>N</td>
  </tr>
  <tr>
    <td>Headlights (Regular & High-Beam)</td>
    <td>Turned off</td>
  </tr>
  <tr>
    <td>Oncoming vehicle lights (Overhead Lighting, Back-lighting & Front-lighting)</td>
    <td>N/A, no other traffic</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

## 4.6 Zones
>ADAS features may be limited spatially by zones. The boundaries of these zones may be fixed or dynamic, and conditions that define a boundary may be based on complexity, operating procedures, or other factors. One example is work zones, which can confuse ADAS as the road configuration (pavement markings and new lane alignments) differs from typical conditions. In a work zone, cones may replace double yellow lines, bollards may replace curbs, and construction 
worker hand signals may overrule traffic lights. (Thorn *et al*, 2018)

SMIRK does not rely on any zone specifics. All items below are either N or N/A.

*Table 18: Geofencing.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Geofencing</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>CBDs</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>School Campuses</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Retirement Communities</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Fixed Route</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 19: Traffic Management Zones.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Traffic Management Zones</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Temporary Closures</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Dynamic Traffic Signs</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Variable Speed Limits</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Temporary or Non-Existent Lane Marking</td>
    <td>N/A</td>
  </tr>
  <tr>
  <td>Human-Directed Traffic</td>
    <td>N</td>
  </tr>
  <tr>
  <td>Loading and Unloading Zones</td>
    <td>N</td>
  </tr>
  <tr>
  <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 20: School/Construction Zones.*
<table> 
  <thead>
  <tr>
    <th colspan="2">School/Construction Zones</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Dynamic speed limit</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Erratic pedestrian</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Vehicular behaviors</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 21: Regions/States.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Regions/States</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Legal/Regulatory</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Enforcement Considerations</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Tort</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

*Table 22: Interference Zones.*
<table> 
  <thead>
  <tr>
    <th colspan="2">Interference Zones</th>
  </tr>
  </thead>
  <tbody>
  <tr>
    <td>Tunnels</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Parking Garage</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Dense Foliage</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Limited GPS</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Atmospheric Conditions</td>
    <td>N/A</td>
  </tr>
  <tr>
    <td>Other</td>
    <td>N</td>
  </tr>
  </tbody>
</table>

# 5 ML Assurance Scoping Argument Pattern [F] <a name="ml_assurance_scoping_pattern"></a>
The figure below shows the ML assurance scoping argument pattern using goal structuring notation (GSN). The pattern follows the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Assurance_Scoping_Argument_Pattern](/docs/figures/gsn-ml_assurance_scoping_argument_pattern.png) <a name="gsn-ml_assurance_scoping"></a>

*Figure 9: SMIRK ML Assurance Scoping Argument Pattern.*

The top claim, i.e., the starting point for the safety argument for the SMIRK ML-based pedestrian recognition component, is that the system safety requirements that have been allocated to the pedestrian recognition component are satisfied in the ODD (G1.1). The safety claim for the pedestrian recognition component is made within the context of the information that was used to establish the safety requirements allocation, i.e., the system description ([C]), the ODD ([B]), and the ML component description ([D]). The allocated system safety requirements ([E]) are also provided as context. An explicit assumption is made that the allocated safety requirements have been correctly defined (A1.1), as this is part of the overall system  safety process preceding AMLAS. Our claim to the validity of this assumption is presented in relation to the HARA described in [E]. As stated in AMLAS, "the primary aim of the ML Safety Assurance Scoping argument is to explain and justify the essential relationship between, on the one hand, the system-level safety requirements and associated hazards and risks, and on the other hand, the ML-specific safety requirements and associated ML performance and failure conditions."

The ML safety claim is supported by an argument split into two parts. First, the development of the ML component is considered with an argument that starts with the elicitation of the ML safety requirements argument. Second, the deployment of the ML component is addressed with a corresponding argument. 

# 6 ML Safety Assurance Scoping Argument [G] <a name="ml_assurance_scoping_argument"></a>
SMIRK instantiates the ML safety assurance scoping argument through the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). The set of artifacts constitutes the safety case for SMIRK's ML-based pedestrian recognition component.

# 7 ML Safety Requirements Argument Pattern [I]
The figure below shows the ML safety requirements argument pattern using GSN. The pattern largely follows the example provided in AMLAS, but adapts it to the specific SMIRK case. The major difference is the introduction of G2.2 targeting ghost braking and the safety cage mechanism as the corresponding solution 2.2.

![GSN-ML-Safety_Reqts_Argument_Pattern](/docs/figures/gsn-ml_safety_reqts_argument_pattern.png) <a name="gsn-ml_safety_reqts_argument"></a>

*Figure 10: SMIRK ML Safety Requirements Argument Pattern.*

The top claim is that system safety requirements that have been allocated to the ML component are satisfied by the model that is developed (G2.1). This is demonstrated through considering explicit ML safety requirements defined for the ML model [H]. The argument approach is a refinement strategy translating the allocated safety requirements into two concrete ML safety requirements (S2.1) provided as context (C2.1). Justification J2.1 explains how we allocated safety requirements to the ML component as part of the system safety process, including the HARA. 

Strategy S2.1 is refined into two subclaims about the validity of the ML safety requirements corresponding to missed pedestrians and ghost braking, respectively. Furthermore, a third subclaim concerns the satisfaction of those requirements. G2.2 focuses on the ML safety requirement SYS-ML-REQ1, i.e., that the nominal functionality of the pedestrian recognition component shall be satisfactory. G2.2 is considered in the context of the ML data (C2.2) and the ML model (C2.3), which in turn are supported by the ML Data Argument Pattern [R] and the ML Learning Argument Pattern [W]. The argumentation strategy (S2.2) builds on two subclaims related to two types of safety requirements with respect to safety-related outputs, i.e., performance requirements (G2.5 in context of C2.4) and robustness requirements (G2.6 in context of C2.5). The satisfaction of both G2.5 and G2.6 are addressed by the ML Verification Argument Pattern [BB]. G2.3 focuses on the ML safety requirement SYS-ML-REQ2, i.e., that the pedestrian recognition component shall reject input that does not resemble the training data to avoid ghost braking. G2.3 is again considered in the context of the ML data (C2.2) and the ML model (C2.3). For SMIRK, the solution is the safety cage architecture (Sn2.1) developed  in the SMILE research program (Henriksson *et al.*, 2021), further described in the [Machine Learning Component Specification](</docs/ML Component Specification.md#4-safety-cage-architecture>).

Subclaim G2.4 states that the ML safety requirements are a valid development of the allocated system safety requirements. The justification (J2.2) is that the requirements have been validated in cross-organizational workshops within the SMILE3 research project. We provide evidence through ML Safety Requirements Validation Results [J] originating in a Fagan inspection (Sn2.2).

# 8 ML Safety Requirements Validation Results [J]
The SMILE3 project conducted a [Fagan inspection](https://en.wikipedia.org/wiki/Fagan_inspection) of the ML safety requirements, i.e., a formal inspection consisting of the steps 1) Planning, 2) Overview, 3) Preparation, 4) Inspection meeting, 5) Rework, and 6) Follow-up. The Fagan inspection targeted the entire SRS.

1. Planning: The authors prepared the SRS and invited the required reviewers to an inspection meeting.
1. Overview: During one of the regular project meetings, the lead authors explained the fundamental structure of the SRS to the reviewers. The SRS inspection checklist was also introduced. Reviewers were also assigned particular inspection perspectives based on their individual expertise. All information was repeated in an email, as not all reviewers were present at the meeting.
1. Preparation: All reviewers conducted an individual inspection of the SRS, noting any questions, issues, and required improvements.
1. Inspection meeting: After sufficient time for the individual inspections, the lead authors and all reviewers met for a virtual meeting. The entire document was discussed, and the findings from the independent inspections were compared. All issues were compiled in an inspection protocol.
1. Rework: The lead authors updated the SRS according to the inspection protocol.
1. Follow-up: Selected reviewers verified that the previously found issues had been correctly resolved. 

The [inspection protocol](https://github.com/RI-SE/smirk/blob/main/docs/protocols/SRS%20Inspection%20Protocol%202021-11-15.xlsx) is available.

# 9 ML Safety Requirements Argument [K]
SMIRK instantiates the ML safety requirements argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Safety Requirements Argument Pattern [I]](</docs/System Requirements Specification.md#5-ml-assurance-scoping-argument-pattern-f->), as well as the following artifacts from preceding AMLAS activities:
- [Safety Requirements Allocated to ML Component](</docs/System Requirements Specification.md#32-safety-requirements-allocated-to-ml-component-e->) [E]
- [ML Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) [H]
- [ML Safety Requirements Validation Results](</docs/System Requirements Specification.md#8-ml-safety-requirements-validation-results-j>) [J]
