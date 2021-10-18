# Data Management Specification v0.2

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
<td>WIP</td>
<td>Working toward the first complete draft.</td>
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
This document contains the data management specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC. As an alternative to longitudinal traffic observations and consideration of emergency statistics, we have analyzed the SMIRK ODD by monitoring the presence of actors and objects in the ESI Pro-SiVIC "Object Catalog" and its development over the versions 2018-2021. We conclude that the demographics of pedestrians in the ODD is constituted of the following: adult males and females in either casual or business casual clothes and young boys wearing jeans and a sweatshirt. As other traffic is not within the ODD (e.g., cars, motorcycles, and bicycles), we consider the following basic shapes to be likely to appear when SMIRK is in operation: boxes, cones, pyramids, and spheres.

## 1.1 Purpose ##
This document describes the data management strategy for the object detection component in SMIRK. The object detection component detects pedestrians in input images, i.e., no other classes are detected in the input.

The document encompasses the entire lifecycle, i.e., data requirements and its justification report, data collection, data preprocessing, data validation, and data monitoring for SMIRK in operations.

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DM: Data Management
- ML: Machine Learning
- ODD: Operational Design Domain
- TTC: Time To Collission

## 1.4 Intended Audience and Reading Suggestions ##
- Developers: the entire document is relevant.
- Testers: sections 2-6 are particularly important.
- Safety assessors: focus on headings that map to the AMLAS process.
- Other stakeholders: read section 2 to understand the expectations on the SMIRK training data.

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- Development Data [N]
- Internal Test Data [O]
- Verification Data [P]
- Ashmore, Calinescu, and Paterson, 2021. [Assuring the Machine Learning Lifecycle: Desiderata, Methods, and Challenges](https://arxiv.org/abs/1905.04223), ACM Comput. Surv. 54(5).
- Gauerhof, Hawkins, David, Picardi, Paterson, Hagiwara, and Habli, 2020. Assuring the Safety of Machine Learning for Pedestrian Detection at Crossings. In Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP).
- [Safety First for Automated Driving (SaFAD)](https://www.daimler.com/documents/innovation/other/safety-first-for-automated-driving.pdf), 2019. Joint White Paper by Aptiv, Audi, Bayrische Motoren Werke; Beijing Baidu Netcom Science Technology, Continental Teves AG, Daimler, FCA US, HERE Global, Infineon Technologies, Intel, and Volkswagen.

# 2 Data Requirements [L] <a name="data_rqts"></a>
This section specifies requirements on the data used to train and test the object detection component in SMIRK. The data requirements are specified to comply with the [Machine Learning Safety Requirements](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#33-machine-learning-safety-requirements-h-) in the System Requirements Specification. All data requirements are organized according to the assurance-related desiderata proposed by Ashmore et al. (2021),  i.e., the key assurance requirements for the data management. The dataset used to train SMIRK must fulfill four desiderata that ensure that the data set is relevant, complete, balanced, and accurate.

The table below shows a requirements traceability matrix beween ML Safety Requirements and Data Requirements. Entries in individual cells denote that the ML safety requirement is addressed, at least partly, by the corresponding data requirement.
![ML-Data Requirements Matrix](/docs/figures/ml-data_matrix.png) <a name="ML-Data Requirements Matrix"></a>

## 2.1 Relevant
This desiderata considers the intersection between the dataset and the supported dynamic driving task in the intended ODD. The SMIRK training data will not cover operational environments that are outside of the ODD, e.g., images collected in heavy snowfall. 

- DAT-REL-REQ1: All data samples shall represent images of a road from the perspective of a vehicle.
- DAT-REL-REQ2: The format of each data sample shall be representative of that which is captured using sensors deployed on the ego vehicle.
- DAT-REL-REQ3: Each data sample shall assume sensor positioning which is representative of that which is used on the ego vehicle.
- DAT-REL-REQ4: All data samples shall represent images of a road that corresponds to the ODD.
- DAT-REL-REQ5: All data samples containing pedestrians shall include one single pedestrian.
- DAT-REL-REQ6: Pedestrians included in data samples shall be of a type that may appear in the ODD.
- DAT-REL-REQ7: All data samples containing non-pedestrian objects shall be of a type that may appear in the ODD.

Rationale: SMIRK adapts the requirements from the Relevant desiderata specified by Gauerhof et al. (2020) for the SMIRK ODD. DAT-REL-REQ5 is added to based on the corresponding fundamental restriction of the SMIRK ODD. DAT-REL-REQ7 restricts data samples providing negative training examples.

## 2.2 Complete
This desiderata considers the sampling strategy across the input domain and its subspaces. Suitable distributions and combinations of features are particularly important. Ashmore et al. (2021) refer to this as the external perspective on the data.

- DAT-COM-REQ1: The data samples shall include sufficient range of environmental factors within the scope of the ODD.
- DAT-COM-REQ2: The data samples shall include sufficient range of pedestrians within the scope of the ODD.
- DAT-COM-REQ3: The data samples shall include images representing a sufficient range of distances to crossing detestrians up to that required by the decision making aspect of the perception pipeline.
- DAT-COM-REQ4: The data samples shall include examples with a sufficient range of levels of occlusion giving partial view of pedestrians crossing the road.
- DAT-COM-REQ5: The data samples shall include a sufficient range of examples reflecting the effects of identified system failure modes.

Rationale: SMIRK adapts the requirements from the Complete desiderata specified by Gauerhof et al. (2020) for the SMIRK ODD. 

## 2.3 Balanced
This desiderata considers the distribution of features in the dataset, e.g., the balance between the number of samples in each class. Ashmore et al. (2021) refer to this as an internal perspective on the data.

- DAT-BAL-REQ1: The data set shall have a comparable representation of samples for each relevant class and feature.
- DAT-BAL-REQ2: The data set shall have an equal share of positive and negative examples.

Rationale: SMIRK adapts the requirements from the Relevant desiderata specified by Gauerhof et al. (2020) for the SMIRK ODD. 

## 2.4 Accurate
This desiderata considers how measurement issues can affect the way that samples reflect the intended ODD, e.g., sensor accuracy and labelling errors. 

- DAT-ACC-REQ1: All bounding boxes produced shall be sufficiently large to include the entirety of the pedestrian.
- DAT-ACC-REQ2: All bounding boxes produced shall be no more than 10% larger in any dimension than the minimum sized box capable of including the entirety of the pedestrian.
- DAT-ACC-REQ3: All pedestrians present in the data samples must be correctly labelled.

Rationale: SMIRK reuses the requirements from the Accurate desiderata specified by Gauerhof et al. (2020). 

# 3 Data Requirements Justification Report [M] <a name="data_rqts_just"></a>
The SMIRK data requirements have evolved during the Swedish [SMILE3 research project](https://www.ri.se/en/what-we-do/projects/smile-iii-safety-analysis-and-verificationvalidation-of-ml-based-systems), in turn based on two previous research projects on safety analysis and verification & validation of machine learning-based automotive systems. All SMIRK requirements have been individually reviewed by SMILE3 project partners and discussed in regular project meetings. Furthermore, we have organized dedicated workshops focusing on hazard and risk analysis and subsequent requirements engineering.

SMIRK requirements are based on examples from analaguous systems presented in peer-reviewed publications, white papers, and technical reports from academic authors. Both system requirements and data requirements are largely reused from a research paper by Gauershof et al. (2020), describing requirements for a pedestrian detection system at UK crossings - peer-reviewed and accepted for publication in the Proc. of the 39th International Conference on ComputerSafety, Reliability and Security (SAFECOMP). Moreover, we have reused requirements from the AMLAS examples and from the SaFAD white paper.

SMIRK has specified a very restricted ODD to support our efforts in requirements engineering for data. Based on several iterations with representatives from different organizations, we posit that the current data requirements fulfil the desiderata. A data set collected according to the requirements will be relevant, complete, balanced, and accurate. Representatives from the following organizations, all active in automotive R&D, have reviewed this work.

- RISE Research Institutes of Sweden
- Semcon
- Infotiv
- QRTech
- Combitech

# 4 Data Generation Log [Q] <a name="data_gen"></a>
The SMIRK vision component uses transfer learning as it is pre-trained on publicly available image data from the [COCO dataset](https://cocodataset.org/). Pretraining on COCO dataset provides features from real-world imagary, from basic shapes to more complex features. Subsequently, the SMIRK vision component is [fine-tuned](https://www.tensorflow.org/tutorials/images/transfer_learning) for the task of pedestrian detection in the specific ODD. Based on the [data requirements](https://github.com/RI-SE/smirk/blob/main/docs/Data%20Management%20Specification.md#2-data-requirements-l-), we generate data for fine-tuning. The data are split into three sets in accordance with AMLAS. 

- Development data: Covering both training and validation data used by developers to create models during ML development.
- Internal test data: Used by developers to test the model.
- Verification data: Used by the independent testers at Infotiv when the model is ready for release. 

## 4.1 Data Collection
The SMIRK data collection campaign focuses on generation of annotated data in ESI Pro-SiVIC. All data generation is script-based and is fully reproducable. The following two lists present the scripts used to play scenarios and capture corresponding annotated data. The first section describes positive examples [PX], i.e., humans that shall be classified as pedestrians. The second section describes negative examples [NX], i.e., objects that shall not be classified as pedestrians. For each listed item, there is a link to a YAML configuration file that is used by the Python script that generates the data in the ESI Pro-SiVIC output folder "Sensors". Ego car is always stationary during data collection, and pedestrian and objects move according to specific configurations. Finally, images are sampled from the camera at 10 frames per second with a resolution of 752x480 pixels. For each image, we add a separate image file containing the ground truth pixel-level annotation of the position of the pedestrian.

In total, we generate data representing 6 x 616 = 3,696 execution scenarios with positive examples and 4 x 40 = 160 execution scenarios with negative examples. In total, the data collection campaign generates roughly 120 GB of worth of image data, annotations, and meta-data (including bounding boxes).

### 4.1.1 Positive examples:
We generate positive example from humans with six visual appearances available in the ESI Pro-SiVIC object catalog.

- [P1] Casual female pedestrian [female_casual.yaml]
- [P2] Casual male pedestrian [male_casual.yaml]
- [P3] Business female pedestrian [female_business.yaml]
- [P4] Business male pedestrian [male_business.yaml]
- [P5] Child [child.yaml]
- [P6] Male construction worker [male_construction.yaml]

All configuration files for positive examples specify the execution of 616 scenarios in ESI Pro-SiVIC. The configurations are organized into four groups (A-D). The pedestrians always follow rectilinear motion (a straight line) at a constant speed during scenario execution. Groups A and B describe pedestrians crossing the road, either from the left (Group A) or from the right (Group B). There are three variation points, i.e., 1) the speed of the pedestrian, 2) the angle at which the pedestrian crosses the road (see [SRS Sec 2.1](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#21-product-perspective)), and 3) the longitudinal distance between ego car and the pedestrian's starting point. In all scenarios, the distance between the starting point of the pedestrian and the edge of the road is 5 m. 

- A. Crossing the road from left to right (280 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Angle (degree): [30, 50, 70, 90, 110, 130, 150]
	- 3. Longitudinal distance (m): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

- B. Crossing the road from right to left (280 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Angle (degree): [30, 50, 70, 90, 110, 130, 150]
	- 3. Longitudinal distance (m): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

Groups C and D describe pedestrians moving in parallel to the road, either toward ego car (Group C) or away (Group D). There are two variation points, i.e., 1) the speed of the pedestrian and 2) an offset from the road center. The longitudinal distance between ego car and the pedestrian's starting point is always 10 m and the pedestrian always move 90 m.

- C. Movement parallel to the road toward ego car (28 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Lateral offset (m): [-3, -2, -1, 0, 1, 2, 3]

- D. Movement parallel to the road away from ego car (28 scenario configurations)
	- 1. Speed (m/s): [1, 2, 3, 4]
	- 2. Lateral offset (m): [-3, -2, -1, 0, 1, 2, 3]

### 4.1.2 Negative examples:
We generate negative examples using four basic shapes available in the ESI Pro-SiVIC object catalog.

Negative examples:
- [N1] Sphere [sphere.yaml]
- [N2] Cube [cube.yaml]
- [N3] Cone [cone.yaml]
- [N4] Pyramid [pyramid.yaml]

All four configuration files for negative examples specify the execution of 10 scenarios in ESI Pro-SiVIC. The configurations represent a basic shape crossing the road either from left or right. Since basic shapes are not animated, we fix the speed at 4 m/s. In all scenarios, the distance between the starting point of the basic shape and the edge of the road is 5 m. The only variation point is the longitudinal distance between ego car and the objects's starting point. The objects always follow rectilinear motion (a straight line) at a constant speed during scenario execution.

- Longitudinal distance (m): [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

## 4.2 Preprocessing
As the SMIRK data collection campaign relies on data generation in ESI Pro-SiVIC, the need for pre-processing differs from counterparts using using naturalistic data. To follow convention, we refer to the data processing between data collection and model training as pre-processing - although post-processing would be a more correct term in SMIRK. We have developed scripts that generate data sets representing the scenarios listed in Section 4.1. The scripts ensure that the crossing pedestrians and objects appear at the right distance with specified conditions and without occlusion. All output images are share the same characteristics, thus no normalization is needed.

SMIRK includes a script to generate bounding boxes for training the object detection model. Pro-SiVIC generates ground truth image segmentation on a pixel-level. [The script](TBD) is used to convert the output to the approriate input format for model training. TBD...

DESCRIBE SAMPLING HERE?

## 4.3 Data Splitting
The generated SMIRK data will be used in sequestered data sets as follows:

- Development data: [P2], [P3], and [N1]
- Internal test data: [P1], [P4], and [N2] 
- Verification data: [P5], [P6], and [N3]

# 5 ML Data Argument Pattern [R] <a name="data_argument_pattern"></a>
The figure below shows the ML data argument pattern using GSN. The pattern follows the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML_Data_Argument_Pattern](/docs/figures/gsn-ml_data_argument_pattern.png) <a name="gsn-ml_data_argument"></a>

The top claim is that the data used during the development and verification of the ML model is sufficient (G3.1). This claim is made for all three data sets: development data [N], internal test data [O], and verification data [P]. The argumentation strategy (S2.1) involves how the sufficiency of these data sets are demonstrated given the Data Requirements [L]. The strategy is supported by arguing over to subclaims demonstrating sufficiency of the Data Requirements (G3.2) and that the Data Requirements are satisfied (G3.3). Claim G3.2 is supported by evidence in the form of a data requirements justification report [M]. As stated in AMLAS, "It is not possible to claim that the data alone can guarantee that the ML safety requirements will be satisfied, however the data used must be sufficient to enable the model that is developed to do so."

Claim G3.3 states that the generated data satisfies the data requirements in context of the decisions made during data collection. The details of the data collection, along with rationales, are recorded in the Data Collection Log [Q]. The argumentation strategy (S2.2) uses refinement mapping to the assurance-related desiderata of the data requirements. The refinement of the desiderata into concrete data requirements for the object detection component of SMIRK, given the ODD, is justified by an analysis of the expected traffic agents and objects that can appear in ESI Pro-SiVIC. For each subclaim corresponding to a desiderata, i.e., relevance (G3.4), completeness (G3.5), accuracy (G3.6), and balance (G3.7), there is evidence in a matching section in the ML Data Validation Report [S].

# 6 ML Data Validation Results [S] <a name="data_validation_results"></a>
TBD.

# 7 ML Data Argument [T] <a name="data_argument"></a>
SMIRK instantiates the ML Data Argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Data Argument Pattern [R]](</docs/Data Management Specification.md#data_argument_pattern>), as well as the following artefacts from preceding AMLAS activities:
- [ML Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) [H]
- [Data Requirements](</docs/Data Management Specification.md#data_rqts>) [L]
- [Data Requirements Justification Report](</docs/Data Management Specification.md#data_rqts_just>) [M]
- [Development Data](TBD) [N]
- [Internal Test Data](TBD) [O]
- [Verification Data](TBD) [P]
- [Data Generation Log](</docs/Data Management Specification.md#data_gen>) [Q]
- [ML Data Validation Results](</docs/Data Management Specification.md#data_validation_results>) [S]
