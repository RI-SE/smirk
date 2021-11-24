# Data Management Specification v0.91

Revision History
<table>
<tr>
<th>Author(s)</th>
<th>Date</th>
<th>Description</th>
<th>Version</th>
</tr>
<tr>
<td>Olof Lennartsson, Elias Sonnsjö</th>
<td>2021-05-20</th>
<td>Initial SMILE version.</th>
<td>0.1</th>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</td>
<td>2021-10-15</td>
<td>Version used when generating datasets.</td>
<td>0.2</td>
</tr>
<tr>
<td>Markus Borg, Kasper Socha</td>
<td>2021-11-02</td>
<td>Complete draft, except sampling details.</td>
<td>0.3</td>
</tr>
<tr>
<tr>
<td>Jens Henriksson</td>
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
<td>WIP</td>
<td>Updated according to 
<a href="https://github.com/RI-SE/smirk/blob/main/docs/protocols/DMS%20Inspection%20Protocol%202021-11-15.xlsx">inspection protocol</a>.
</td>
<td>0.91</td>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

# 1 Introduction
This data management specification (DMS) describes the overall approach to data management for SMIRK and the exlicit data requirements. SMIRK is a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML), i.e., an advanced driver-assistance system (ADAS). The ADAS is intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic. SMIRK, including the accompanying safety case, is developed with full transparancy under an open-source software (OSS) license.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC. As an alternative to longitudinal traffic observations and consideration of emergency statistics, we have analyzed the SMIRK operational design domain (ODD) by monitoring the presence of actors and objects in the ESI Pro-SiVIC "Object Catalog" and its development over the versions 2018-2021. We conclude that the demographics of pedestrians in the ODD is constituted of the following: adult males and females in either casual or business casual clothes, young boys wearing jeans and a sweatshirt, and male road workers. As other traffic is not within the ODD (e.g., cars, motorcycles, and bicycles), we consider the following basic shapes from the object catalog to as examples of out-of-distribution (OOD) objects (that still can appear in the ODD) for SMIRK to handle in operation: boxes, cones, pyramids, and spheres.

## 1.1 Purpose ##
This document describes the data management strategy for the pedestrian recognition component in SMIRK. The pedestrian recognition component detects pedestrians in input images based on output from the object detection provided by the radar sensor. In the SMIRK minimum viable product (MVP), no other classes but pedestrians are considered by the ML-based pedestrian recognition component. The document encompasses the entire lifecycle, i.e., data requirements and its justification report, data collection, data preprocessing, data validation, and data monitoring for SMIRK in operation.

The SMIRK *product goal* is to assist the driver on country roads in rural areas by performing emergency braking in the case of an imminent collision with a pedestrian. The *project goal* of the SMIRK development endeavor, as part of the research project SMILE3 is to provide a concrete ADAS case study as a basis for discussion - at the same time providing an open research prototype for the community. The goals are further elaborated in the [System Requirements Specification](</docs/System%20Requirements%20Specification.md#11-purpose>).

## 1.2 Document Conventions ##
The number of academic publications in the list of references is unconventional for techincal project doumentation. This is a conscious decision. SMIRK is developed as a prototype in the context of a research project with limited resources. As part of our research, we aim to integrate (sometimes scattered) pieces from the state-of-the-art literature. Synthesis is a fundamental tool in our research and we seek novel insights while focusing on refinement and integration. We actively choose to rely on reuse of design decisions from previously peer-reviewed publications. Building on previous work, i.e., [standing on the shoulders of others](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants), is a core concept in research that allows validation of previous work, incl. previously proposed requirements. When available, and unless open access publication models have been used, links to academic publications point to preprints on open repositories such as [arXiv](https://arxiv.org/) rather than peer-reviewed revisions behind paywalls.

Headings with a reference in brackets [X] refer to artifacts prescribed by the AMLAS process ([Guidance on the Assurance of Machine Learning in Autonomous Systems](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf)). Due to formatting limitations in GitHub MarkDown, all figure and table captions appear in italic font to distinguish them from the running text.

## 1.3 Glossary
- ADAS: Advanced Driver-Assistance Systems
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DM: Data Management
- GSN: Goal Structuring Notation
- ML: Machine Learning
- MVP: Minimum Viable Product
- ODD: Operational Design Domain
- OOD: Out Of Distribution
- OSS: Open-Source Software
- PAEB: Pedestrian Automatic Emergency Braking
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
The section is organized into internal stakeholders, i.e., roles that are directly involved in the SMIRK development, and external stakeholders who are linked indirectly but have significant contribution in the successful completion of the SMIRK project. External stakeholders also include the ML safety community at large. Note that AMLAS prescribes a split between testers that are involved during the development and testers that are "sufficiently independent from the development activities." We refer to these roles as *internal testers* and *independent testers*, respectively.

**Internal stakeholders**

The entire document is relevant to the internal development organization. Specific stakeholders are recommended to pay particular attention as follows. 
- Software developers: [Section 2 (Data Requirements)](#2-data-requirements-l-).
- ML developers: [Section 2 (Data Requirements)](#2-data-requirements-l-) and [Section 4 (Data Generation Log)](#4-data-generation-log-q-).
- Internal testers: [Section 2 (Data Requirements)](#2-data-requirements-l-) and [Section 4 (Data Generation Log)](#4-data-generation-log-q-).
- Independent testers: [Section 2 (Data Requirements)](#2-data-requirements-l-).

**External stakeholders**
- Safety assessors: Focus on headings that map to the AMLAS process, indicated with letters in brackets.
- Researchers: Academic and industrial reserachers active in ML safety are likely to find most value in [Section 2 (Data Requirements)](#2-data-requirements-l-).
- Standardization bodies and legislators: An overview of the safety argumentation is presented in [Section 5 (ML Data Argument Pattern)](#5-ml-data-argument-pattern-r-).
- Curious readers: For an overview of data management in SMIRK, read [Section 1 (Introduction)](#1-introduction).

## 1.5 References ##
The references are organized into 1) internal SMIRK documentation, 2) SMIRK data sets, 3) peer-reviewed publications, and 4) gray literature and white papers. When a reference listed under category 2) or 3) is used to motivate a design decision or a specific requirement, there is an explicit reference in the running text. Note that this DMS is self-contained, the references are provided for traceability to the underlying design rationales. Interested readers are referred to the discussions in the original sources.

**Internal SMIRK documentation**
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [System Architecture Description](</docs/System Architecture Description.md>)
- [ML Component Specification](</docs/ML Component Specification.md>)

**SMIRK data sets**
- Development Data [N]
- Internal Test Data [O]
- Verification Data [P]

**Peer-reviewed publications**
- Ashmore, Calinescu, and Paterson, 2021. [Assuring the Machine Learning Lifecycle: Desiderata, Methods, and Challenges](https://arxiv.org/abs/1905.04223), *ACM Computing Surveys*, 54(5).
- Gauerhof, Hawkins, David, Picardi, Paterson, Hagiwara, and Habli, 2020. [Assuring the Safety of Machine Learning for Pedestrian Detection at Crossings](https://link.springer.com/chapter/10.1007/978-3-030-54549-9_13). In *Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP).

**Gray literature and white papers**
- The Assurance Case Working Group (ACWG), 2018. [Goal Structuring Notation Community Standard](https://scsc.uk/r141B:1?t=1), Version 2, SCSC-141B. 
- [Safety First for Automated Driving (SaFAD)](https://www.daimler.com/documents/innovation/other/safety-first-for-automated-driving.pdf), 2019. Joint White Paper by Aptiv, Audi, Bayrische Motoren Werke; Beijing Baidu Netcom Science Technology, Continental Teves AG, Daimler, FCA US, HERE Global, Infineon Technologies, Intel, and Volkswagen.
- Thorn, Kimmel, and Chaka, 2018. [A Framework for Automated Driving System Testable Cases and Scenarios](https://trid.trb.org/view/1574670), Technical Report DOT HS 812 623, National Highway Traffic Safety Administration.

# 2 Data Requirements [L] <a name="data_rqts"></a>
This section specifies requirements on the data used to train and test the pedestrian recognition component in SMIRK. The data requirements are specified to comply with the [Machine Learning Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) in the System Requirements Specification. All data requirements are organized according to the assurance-related desiderata proposed by Ashmore *et al.* (2021), i.e., the key assurance requirements for the data management. The dataset used to train SMIRK must fulfill four desiderata that ensure that the data set is relevant, complete, balanced, and accurate.

The table below shows a requirements traceability matrix between ML Safety Requirements and Data Requirements. Entries in individual cells denote that the ML safety requirement is addressed, at least partly, by the corresponding data requirement.
![ML-Data Requirements Matrix](/docs/figures/ml-data_matrix.png) <a name="ML-Data Requirements Matrix"></a>

## 2.1 Relevant
This desideratum considers the intersection between the dataset and the supported dynamic driving task in the [ODD](</docs/System Requirements Specification.md#odd>). The SMIRK training data will not cover operational environments that are outside of the ODD, e.g., images collected in heavy snowfall. 

- DAT-REL-REQ1: All data samples shall represent images of a road from the perspective of a vehicle.
- DAT-REL-REQ2: The format of each data sample shall be representative of that which is captured using sensors deployed on the ego vehicle.
- DAT-REL-REQ3: Each data sample shall assume sensor positioning representative of the positioning used on the ego vehicle.
- DAT-REL-REQ4: All data samples shall represent images of a road that corresponds to the ODD.
- DAT-REL-REQ5: All data samples containing pedestrians shall include one single pedestrian.
- DAT-REL-REQ6: Pedestrians included in data samples shall be of a type that may appear in the ODD.
- DAT-REL-REQ7: All data samples representing non-pedestrian OOD objects shall be of a type that may appear in the ODD.

Rationale: SMIRK adapts the requirements from the Relevant desiderata specified by Gauerhof *et al.* (2020) for the SMIRK ODD. DAT-REL-REQ5 is added based on the corresponding fundamental restriction of the ODD of the SMIRK MVP. DAT-REL-REQ7 restricts data samples providing negative examples for testing.

## 2.2 Complete
This desideratum considers the sampling strategy across the input domain and its subspaces. Suitable distributions and combinations of features are particularly important. Ashmore *et al.* (2021) refer to this as the external perspective on the data.

- DAT-COM-REQ1: The data samples shall include a sufficient range of environmental factors within the scope of the ODD.
- DAT-COM-REQ2: The data samples shall include a sufficient range of pedestrians within the scope of the ODD.
- DAT-COM-REQ3: The data samples shall include images representing a sufficient range of distances to crossing pedestrians up to that required by the decision making aspect of the pedestrian recognition component.
- DAT-COM-REQ4: The data samples shall include examples with a sufficient range of levels of occlusion giving partial view of pedestrians crossing the road.
- DAT-COM-REQ5: The data samples shall include a sufficient range of examples reflecting the effects of identified system failure modes.

Rationale: SMIRK adapts the requirements from the Complete desiderata specified by Gauerhof *et al.* (2020) for the SMIRK ODD. 

## 2.3 Balanced
This desideratum considers the distribution of features in the dataset, e.g., the balance between the number of samples in each class. Ashmore *et al.* (2021) refer to this as an internal perspective on the data.

- DAT-BAL-REQ1: The data set shall have a comparable representation of samples for each relevant class and feature.
- DAT-BAL-REQ2: The data set shall contain both positive and negative examples.

Rationale: SMIRK adapts the requirements from the Relevant desiderata specified by Gauerhof *et al.* (2020) for the SMIRK ODD. Note that *comparable* in DAT-BAL-REQ1 shall not be interpreted as *equal share* in this context. For example, considering the gender of pedestrians, the ESI Pro-SiVIC object catalog does only contain male children and road workers. Furthermore, DAT-BAL-REQ2 is primarily included to align with Gauerhof *et al.* (2020) and to preempt related questions by safety assessors. In practice, the concept of negative examples when training object detection models are typically satisfied implicitly as the parts of the images that do not belong to the annotated class are *de facto* negatives.  

## 2.4 Accurate
This desideratum considers how measurement issues can affect the way that samples reflect the intended ODD, e.g., sensor accuracy and labeling errors. 

- DAT-ACC-REQ1: All bounding boxes produced shall be sufficiently large to include the entirety of the pedestrian.
- DAT-ACC-REQ2: All bounding boxes produced shall be no more than 10% larger in any dimension than the minimum sized box capable of including the entirety of the pedestrian.
- DAT-ACC-REQ3: All pedestrians present in the data samples shall be correctly labeled.

Rationale: SMIRK reuses the requirements from the Accurate desiderata specified by Gauerhof *et al.* (2020). 

# 3 Data Requirements Justification Report [M] <a name="data_rqts_just"></a>
The SMIRK data requirements have evolved during the Swedish [SMILE3 research project](https://www.ri.se/en/what-we-do/projects/smile-iii-safety-analysis-and-verificationvalidation-of-ml-based-systems), in turn based on two previous research projects on safety analysis and verification & validation of machine learning-based automotive systems. All SMIRK requirements have been individually reviewed by SMILE3 project partners and discussed in regular project meetings. Furthermore, we have organized dedicated workshops focusing on hazard and risk analysis and subsequent requirements engineering.

SMIRK requirements are based on examples from analogous systems presented in peer-reviewed publications, white papers, and technical reports from academic authors. Both system requirements and data requirements are largely reused from a research paper by Gauershof *et al.* (2020), describing requirements for a pedestrian detection system at UK crossings - peer-reviewed and accepted for publication in the *Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP)*. Moreover, we have reused requirements from the AMLAS examples and aligned the results with the SaFAD white paper.

For the SMIRK MVP, we have specified a very restricted ODD to support our efforts in requirements engineering for data. Based on several iterations with representatives from different organizations, we posit that the current data requirements fulfill the desiderata. A data set collected according to the requirements will be relevant, complete, balanced, and accurate. Representatives from the following organizations, all active in automotive R&D, have reviewed this work.

- [RISE Research Institutes of Sweden](https://www.ri.se/en)
- [Semcon](https://semcon.com/)
- [Infotiv](https://www.infotiv.se/en)
- [QRTech](https://www.qrtech.se/en/)
- [Combitech](https://www.combitech.com/)

# 4 Data Generation Log [Q] <a name="data_gen"></a>
This section descibres how the data used for the fine-tuning of the ML model in the pedestrian recognition component was generated. Based on the [data requirements](https://github.com/RI-SE/smirk/blob/main/docs/Data%20Management%20Specification.md#2-data-requirements-l-), we generate data for fine-tuning in ESI Pro-SIVIC. The data are split into three sets in accordance with AMLAS. 

- Development data: Covering both training and validation data used by developers to create models during ML development.
- Internal test data: Used by developers to test the model.
- Verification data: Used in the independent test activity, led by Infotiv, when the model is ready for release. 

## 4.1 Data Collection
The SMIRK data collection campaign focuses on generation of annotated data in ESI Pro-SiVIC. All data generation is script-based and fully reproducible. The following two lists present the scripts used to play scenarios and capture the corresponding annotated data. The first section describes positive examples [PX], i.e., humans that shall be classified as pedestrians. The second section describes examples that represent OOD shapes [NX], i.e., objects that shall not initiate PAEB in case of an imminent collision. These images, referred to as negative examples, shall either not be recognized as a pedestrian or be rejected by the SMIRK safety cage. 

For each listed item, there is a link to a YAML configuration file that is used by the Python script that generates the data in the ESI Pro-SiVIC output folder "Sensors". Ego car is always stationary during data collection, and pedestrians and objects move according to specific configurations. Finally, images are sampled from the camera at 10 frames per second with a resolution of 752x480 pixels. For each image, we add a separate image file containing the ground truth pixel-level annotation of the position of the pedestrian.

In total, we generate data representing 6 x 616 = 3,696 execution scenarios with positive examples and 4 x 40 = 160 execution scenarios with negative examples. In total, the data collection campaign generates roughly 120 GB of image data, annotations, and meta-data (including bounding boxes).

### 4.1.1 Positive examples:
We generate positive examples from humans with six visual appearances available in the ESI Pro-SiVIC object catalog.

- [P1] Casual female pedestrian [TBD: female_casual.yaml]
- [P2] Casual male pedestrian [TBD: male_casual.yaml]
- [P3] Business female pedestrian [TBD: female_business.yaml]
- [P4] Business male pedestrian [TBD: male_business.yaml]
- [P5] Child [TBD: child.yaml]
- [P6] Male construction worker [TBD: male_construction.yaml]

Each configuration file for positive examples specify the execution of 616 scenarios in ESI Pro-SiVIC. The configurations are organized into four groups (A-D). The pedestrians always follow rectilinear motion (a straight line) at a constant speed during scenario execution. Groups A and B describe pedestrians crossing the road, either from the left (Group A) or from the right (Group B). There are three variation points, i.e., 1) the speed of the pedestrian, 2) the angle at which the pedestrian crosses the road (see [SRS Sec 2.1](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#21-product-perspective)), and 3) the longitudinal distance between ego car and the pedestrian's starting point. In all scenarios, the distance between the starting point of the pedestrian and the edge of the road is 5 m. 

- A. Crossing the road from left to right (280 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Angle (degree): [30, 50, 70, 90, 110, 130, 150]
	- 3. Longitudinal distance (m): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

- B. Crossing the road from right to left (280 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Angle (degree): [30, 50, 70, 90, 110, 130, 150]
	- 3. Longitudinal distance (m): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

Groups C and D describe pedestrians moving parallel to the road, either toward ego car (Group C) or away (Group D). There are two variation points, i.e., 1) the speed of the pedestrian and 2) an offset from the road center. The pedestrian always moves 90 m, with a longitudinal distance between ego car and the pedestrian's starting point of 100 m for Group C (towards) and 10 m for Group D (away).

- C. Movement parallel to the road toward ego car (28 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Lateral offset (m): [-3, -2, -1, 0, 1, 2, 3]

- D. Movement parallel to the road away from ego car (28 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Lateral offset (m): [-3, -2, -1, 0, 1, 2, 3]

### 4.1.2 Negative examples:
We generate negative examples using four basic shapes available in the ESI Pro-SiVIC object catalog.

Negative examples:
- [N1] Sphere [TBD: sphere.yaml]
- [N2] Cube [TBD: cube.yaml]
- [N3] Cone [TBD: cone.yaml]
- [N4] Pyramid [TBD: pyramid.yaml]

All four configuration files for negative examples specify the execution of 10 scenarios in ESI Pro-SiVIC. The configurations represent a basic shape crossing the road from the left or right at an angle perpendicular to the road. Since basic shapes are not animated, we fix the speed at 4 m/s. In all scenarios, the distance between the starting point of the basic shape and the edge of the road is 5 m. The only variation point is the longitudinal distance between ego car and the objects' starting point. The objects always follow rectilinear motion (a straight line) at a constant speed during scenario execution.

- Longitudinal distance (m): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

## 4.2 Preprocessing
As the SMIRK data collection campaign relies on data generation in ESI Pro-SiVIC, the need for pre-processing differs from counterparts using naturalistic data. To follow convention, we refer to the data processing between data collection and model training as pre-processing - although post-processing would be a more accurate term for the SMIRK development. We have developed scripts that generate data sets representing the scenarios listed in Section 4.1. The scripts ensure that the crossing pedestrians and objects appear at the right distance with specified conditions and with controlled levels of occlusion. All output images share the same characteristics, thus no normalization is needed.

SMIRK includes a script to generate bounding boxes for training the object detection model. ESI Pro-SiVIC generates ground truth image segmentation on a pixel-level. [The script](TBD) is used to convert the output to the appropriate input format for model training. Note that the diversity of the synthetic imagery is limited, thus we do not train the model on the entire data set. As part of the model training described in the [ML Component Specification](</docs/ML Component Specification.md>), we analyze different sample sizes during the SMIRK ML development.

## 4.3 Data Splitting
The generated SMIRK data will be used in sequestered data sets as follows:

- Development data: [P2] and [P3]
- Internal test data: [P1], [P4], [N1], and [N2] 
- Verification data: [P5], [P6], [N3], and [N4]

# 5 ML Data Argument Pattern [R] <a name="data_argument_pattern"></a>
The figure below shows the ML data argument pattern using GSN. The pattern follows the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML_Data_Argument_Pattern](/docs/figures/gsn-ml_data_argument_pattern.png) <a name="gsn-ml_data_argument"></a>

The top claim is that the data used during the development and verification of the ML model is sufficient (G3.1). This claim is made for all three data sets: development data [N], internal test data [O], and verification data [P]. The argumentation strategy (S2.1) involves how the sufficiency of these data sets is demonstrated given the Data Requirements [L]. The strategy is supported by arguing over subclaims demonstrating sufficiency of the Data Requirements (G3.2) and that the Data Requirements are satisfied (G3.3). Claim G3.2 is supported by evidence in the form of a data requirements justification report [M]. As stated in AMLAS, "It is not possible to claim that the data alone can guarantee that the ML safety requirements will be satisfied, however the data used must be sufficient to enable the model that is developed to do so."

Claim G3.3 states that the generated data satisfies the data requirements in context of the decisions made during data collection. The details of the data collection, along with rationales, are recorded in the Data Collection Log [Q]. The argumentation strategy (S2.2) uses refinement mapping to the assurance-related desiderata of the data requirements. The refinement of the desiderata into concrete data requirements for the object detection component of SMIRK, given the ODD, is justified by an analysis of the expected traffic agents and objects that can appear in ESI Pro-SiVIC. For each subclaim corresponding to a desideratum, i.e., relevance (G3.4), completeness (G3.5), accuracy (G3.6), and balance (G3.7), there is evidence in a matching section in the ML Data Validation Report [S].

# 6 ML Data Validation Results [S] <a name="data_validation_results"></a>
The SMIRK ML data validation consists of two activities, a [Fagan inspection](https://en.wikipedia.org/wiki/Fagan_inspection) of the data requirements and an analysis of the data sets. Moreover, as the SMIRK data is generated in ESI Pro-SiVIC, we argue that the corresponding [scripts](https://github.com/RI-SE/smirk/tree/main/pedestrian-generator) result in data that implicitly complies with most of the data requirements.

First, the SMILE project conducted a Fagan inspection, i.e., a formal inspection, consisting of the steps 1) Planning, 2) Overview, 3) Preparation, 4) Inspection meeting, 5) Rework, and 6) Follow-up. The Fagan inspection targeted the entire DMS.

1. Planning: The authors prepared the DMS and invited the required reviewers to an inspection meeting.
1. Overview: During one of the regular project meetings, the lead authors explained the fundamental structure of the DMS to the reviewers. The partly relevant SRS inspection checklist was also introduced. Reviewers were also assigned particular inspection perspectives based on their individual expertise. All information was repeated in an email, as not all reviewers were present at the meeting.
1. Preparation: All reviewers conducted an individual inspection of the DMS, noting any questions, issues, and required improvements.
1. Inspection meeting: After sufficient time for the individual inspections, the lead authors and all reviewers met for a virtual meeting. The entire document was discussed, and the findings from the independent inspections were compared. All issues were compiled in an inspection protocol.
1. Rework: The lead authors updated the SRS according to the inspection protocol.
1. Follow-up: Selected reviewers verified that the previously found issues had been correctly resolved. 

The inspection protocol is available at TBD.

Second, the SMILE project analyzed the characteristics of the data sets. The analysis was based on automated data validation using <TBD, DESCRIBE THAT KASPER IS DOING>. Furthermore, SMILE reviewers manually analyzed a random sample of images from the data set <TBD, DESCRIBE HOW WE DO THIS>.

Finally, we argue that the script-based generation of data in ESI Pro-SiVIC leads to data compliant with the data requirements. Our argumentation follows the four desiderata introduced in [Section 2](https://github.com/RI-SE/smirk/blob/main/docs/Data%20Management%20Specification.md#2-data-requirements-l-)
- Relevant: DAT-REL-REQ1 to DAT-REL-REQ7 are implicitly met by the data generation scripts. Everything present in the data set has been explicitly added by the SMIRK developers in the scripts. Only relevant data samples captured using a forward-facing camera in a valid sensor position have been added to the scripts. No outlier objects exist in the data sets.
- Complete: DAT-COM-REQ is satisfied as the ODD is restricted to excellent driving conditions. The data set complies with DAT-COM-REQ2 since we explicitly cover six pedestrian types available in the ESI Pro-SiVIC object catalog. DAT-COM-REQ3 is satisfied through scripts that explicitly generate data that covers longitudinal distances between 10 meters and 100 meters. DAT-COM-REQ4 is met since the scripts ensure data collection from the point in time that pedestrians enter the camera's field of vision (a hand becomes available) until the pedestrian leaves (only a foot remains). DAT-COM-REQ5 is implicitly satisfied as the ideal camera in ESI Pro-SiVIC does not fail, i.e., there will be no dirt on the lens or cracks in the optics.
- Balanced: DAT-BAL-REQ1 and DAT-BAL-REQ2 are validated automatically using <TBD, DESCRIBE THAT KASPER IS DOING>.
- Accurate: DAT-ACC-REQ1 and DAT-ACC-REQ3 are implicitly met as ESI Pro-SiVIC generates the ground truth on pixel-level. DAT-ACC-REQ2 is also implicitly satisfied as we extract bounding boxes using a script that identifies the smallest possible rectangle around the pedestrian.

# 7 ML Data Argument [T] <a name="data_argument"></a>
SMIRK instantiates the ML Data Argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Data Argument Pattern [R]](</docs/Data Management Specification.md#data_argument_pattern>), as well as the following artifacts from preceding AMLAS activities:
- [ML Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) [H]
- [Data Requirements](</docs/Data Management Specification.md#data_rqts>) [L]
- [Data Requirements Justification Report](</docs/Data Management Specification.md#data_rqts_just>) [M]
- [Development Data](TBD) [N]
- [Internal Test Data](TBD) [O]
- [Verification Data](TBD) [P]
- [Data Generation Log](</docs/Data Management Specification.md#data_gen>) [Q]
- [ML Data Validation Results](</docs/Data Management Specification.md#data_validation_results>) [S]
