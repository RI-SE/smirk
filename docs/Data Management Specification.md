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

We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC. 

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
The SMIRK data collection campaign focuses on generation of annotated data in ESI Pro-SiVIC. All data generation is script-based and are fully reproducable. The following list presents the scripts used to play scenarios and capture corresponding annotated data:

- Casual female pedestrian crossing from the left [LINK]
- Casual female pedestrian crossing from the right [LINK]
- Casual male pedestrian crossing from the left [LINK]
- Casual male pedestrian crossing from the right [LINK]
- Business casual female pedestrian crossing from the left [LINK]
- Business casual female pedestrian crossing from the right [LINK]
- Business casual male pedestrian crossing from the left [LINK]
- Business casual male pedestrian crossing from the right [LINK]
- Child crossing from the left [LINK]
- Child crossing from the right [LINK]
- Male construction worker crossing from the left [LINK]
- Male construction worker crossing from the right [LINK]

Moreover, all of the above scenraios contain pedestrians standing still on the road and walking on the road toward or away from ego car.

The scripts equally spaced distributions of input data using the following variation points for the pedestrian:

- starting position (x, y)
- crossing angle
- walking or running speed 

## 4.2 Data Cleaning
Data needs to be cleaned after it has been collected: Outliers, conflicted and irrelevant data, in terms of the ODD, needs to be excluded along with invalid data.

## 4.3 Preprocessing
Normalization of data, e.g., make all images (for a perception model) the same size. If collecting from the real world, simulated data could be added both as disturbances in real world images and as synthetic data. GA, GANs can be used to automatically create “lookalike twins” of data to increase the size and diversity of the data-set.

## 4.4 Data Splitting
What goes where? Random split? Leave out some scripts for testing and verification, respectively?

# 5 ML Data Argument Pattern [R] <a name="data_argument_pattern"></a>
TBD.

# 6 ML Data Validation Results [S] <a name="data_validation_results"></a>
TBD.

# 7 ML Data Argument [T] <a name="data_argument"></a>
TBD.
