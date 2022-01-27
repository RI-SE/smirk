# System Test Specification v0.3

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
<td>Olof Lennertsson, Elias Sonnsjö</th>
<td>2021-10-26</th>
<td>Draft version of ML model test cases.</th>
<td>0.2</th>
</tr>
<tr>
<td>Markus Borg</th>
<td>WIP</th>
<td>Toward a complete draft.</th>
<td>0.3</th>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the system test specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system that relies on machine learning (ML). SMIRK is an Advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic.

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
The testing process must be independent of the development. Neither developers nor ML developers can have access to this document.

- Developers: Must not have access to the document.
- ML developers: Must not have access to the document.
- Testers: The entire document is important.
- Safety assessors: The entire document is important.
- Other stakeholders: TBD

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [Data Management Specification](</docs/Data Management Specification.md>)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)
- Borg, Bronson, Christensson, Olsson, Lennartsson, Sonnsjö, Ebadi, and Karsberg, 2021. Exploring the Assessment List for Trustworthy AI in the Context of Advanced Driver-Assistance Systems, In Proc. of the 2nd Workshop on Ethics in Software Engineering Research and Practice.
- Hauer, Schmidt, Holzmüller, and Pretschner, 2019. Did We Test All Scenarios for Automated and Autonomous Driving Systems?. In Proc. of the 2019 IEEE Intelligent Transportation Systems Conference, pp. 2950-2955.
- ISO/IEC/IEEE, 2018. [ISO/IEC/IEEE 29148:2018](https://www.iso.org/standard/72089.html) Systems and Software Engineering - Life Cycle Processes - Requirements Engineering.
- Masuda, 2017. Software Testing Design Techniques Used in Automated Vehicle Simulations. In Proc. of the 2017 IEEE International Conference on Software Testing, Verification and Validation Workshops, pp. 300-303.
- Riccio, Jahangirova, Stocco, Humbatova, Weiss, and Tonella. Testing Machine Learning Based Systems: A Systematic Mapping, Empirical Software Engineering, 25, 5193-5254, 2020.
- Tao, Li, Wotowa, Felbinger, and Nica, 2019. On the Industrial Application of Combinatorial Testing for Autonomous Driving Functions. In Proc. of the 2019 IEEE International Conference on Software Testing, Verification and Validation Workshops, pp. 234-240. 
- Zhang, Harman, Ma, and Liu, 2020. Machine Learning Testing: Survey, Landscapes and Horizons. IEEE Transactions on Software Engineering.

# 2 ML Test Strategy <a name="strategy"></a>
This section describes the overall ML test strategy. The SMIRK ML-based object detection component is tested on multiple levels.

- Dataset testing: This level refers to automatic checks that verify that specific properties of the dataset are satisfied. As described in the [ML Data Validation Results](https://github.com/RI-SE/smirk/blob/main/docs/Data%20Management%20Specification.md#6-ml-data-validation-results-s-), the data validation includes automated testing of the Balance desiderata. Zhang et al. (2020) refer to dataset testing as Input testing.
- Model testing: Testing that the ML model provides the expected output. This is the primary focus of academic research on ML testing, and includes white-box, black-box, and data-box access levels during testing (Riccio et al., 2020). SMIRK model testing is done independently from model development and results in ML Verification Results [X] as described in Section 3.
- Unit testing: Conventional unit testing on the level of Python classes. SMIRK provides a test suite for execution with the pytest framework. Unit testing is conducted by the SMIRK developers and the results are reported on GitHub. This level of testing is not elaborated any further in this document.
- System testing: System-level testing of the SMIRK ADAS based on a set of Operational Scenarios [EE]. All test cases are designed for execution in ESI Pro-SiVIC. The system testing targets the requirements in the [System Requirements Specification](</docs/System Requirements Specification.md>). This level of testing results in Integration Testing Results [FF] as described in Section 4.

# 3 ML Model Testing [AA]
This section corresponds to the Verification Log in AMLAS Step 5, i.e., Model Verification Assurance. Here we explicitly document the ML Model testing strategy, i.e., the range of tests undertaken and bounds and test parameters motivates by SMIRK system requirements. 

The testing of the SMIRK ML model is based on assessing the object detection accuracy for the sequestered verification dataset. A fundamental aspect of the verification argument is that this dataset was never used in any way during the development of the ML model. To further ensure the independence of the ML verification, engineers from [Infotiv](https://www.infotiv.se/), part of the SMILE3 research consortium, led the verification activities. Infotiv led the corresponding V\&V work package and were not in any way involved in the development of the ML model. As described in the [Machine Learning Component Specification](</docs/ML Component Specification.md>), the ML development was led by [Semcon](https://semcon.com/) with support from [RISE Research Institutes of Sweden](https://www.ri.se/en).

The ML model test cases provide results for both 1) the entire verification dataset and 2) nine slices of the dataset that are deemed particularly important. The selection of slices was motivated by either an analysis of the available technology or ethical considerations, especially from the perspective of AI fairness (Borg et al., 2021).

Consequently, we measure the performance for the following sets of data. Identifiers in parentheses show direct connections to requirements.
1. The entire verification dataset
1. Pedestrians close to the ego car (longitudinal distance <50 m) (SYS-PER-REQ1, SYS-PER-REQ2)
1. Pedestrians far from the ego car (longitudinal distance >= 50m)
1. Running pedestrians (speed >= 3 m/s) (SYS-ROB-REQ2)
1. Walking pedestrians (speed > 0 m/s but < 3 m/s) (SYS-ROB-REQ2)
1. Pedestrians standing still (speed = 0 m/s) (SYS-ROB-REQ2)
1. Occluded pedestrians (entering or leaving the field of view) (DAT-COM-REQ4)
1. Male pedestrians (DAT-COM-REQ2)
1. Female pedestrians (DAT-COM-REQ2)
1. Children (DAT-COM-REQ2)

TBD: Describe how we measure the results on verification dataset and all slices. Intersection over union or perhaps https://dbolya.github.io/tide/

Results from running ML model testing, i.e., ML Verification Results [Z], are documented in the [Protocols folder](https://github.com/RI-SE/smirk/blob/main/docs/protocols/).

# 4 System Testing
System-level testing of SMIRK involves integrating the ML model into the object detection component and the complete PAEB ADAS. We do this by defining a set of Operational Scenarios [EE] for which we assess the satisfaction of the [ML Safety Requirements](</docs/System Requirements Specification.md#ml_safety_reqts>). The results from the system-level testing, i.e., the Integration Testing Results [FF], are documented in the [Protocols folder](https://github.com/RI-SE/smirk/blob/main/docs/protocols/).

## 4.1 Operational scenarios [EE] ##
ISO/IEC/IEEE 29148:2018 defines an operational scenario as "a description of an imagined sequence of events that includes the interaction of the product or service with its environment and users, as well as interaction among its product or service components." Consequently, the set of operational scenarios used for testing SMIRK on the system level must represent the diversity of real scenarios that may be encountered when SMIRK is in operation. Furthermore, for testing purposes, it is vital that the set of defined scenarios are meaningful with respect to verification of SMIRK's safety requirements.

As SMIRK is designed to operate in ESI Pro-SiVIC, the difference between defining operational scenarios in text and implementation scripts to execute the same scenarios in the simulated environment is very small. We will not define any operational scenarios that cannot be scripted for execution in ESI Pro-SiVIC. To identify a meaningful set of operational scenarios, we use equivalence partitioning as proposed by Masuda (2017) as one approach to limit the number of test scenarios to execute in vehicle simulators. Originating in the equivalence classes, we use combinatorial testing to reduce the set of operational scenarios. Using combinatorial testing to create test cases for system testing of a PAEB testing in a vehicle simulator has previously been reported by Tao et al. (2019). We create operational scenarios that provide complete pair-wise testing of SMIRK considering the identified equivalence classes.

Based on an analysis of the [ML Safety Requirements](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#33-machine-learning-safety-requirements-h-) and the [Data Requirements](https://github.com/RI-SE/smirk/blob/main/docs/Data%20Management%20Specification.md#2-data-requirements-l-), we define operational scenarios addressing SYS-ML-REQ1 and SYS-ML-REQ2 separately. For each subset of operational scenarios, we identify key variation dimensions (i.e., parameters in test scenario generation) and split dimensions into equivalence classes using explicit ranges. Note that ESI Pro-SiVIC enables limited configurability of basic shapes compared to pedestrians, thus the corresponding number of operational scenarios is lower.

**Operational Scenarios for SYS-ML-REQ1:**
- Pedestrian starting point (lateral offset from the road in meters): Left side of the road (-5 m), On the road (0 m), Right side of the road (5 m)
- Longitudinal distance from ego car (offset in meters): Close (<25m), Medium distance (25-50 m), Far away (>50 m)
- Pedestrian appearance: Male casual, Female casual, Male business, Female business, Male worker, Child
- Pedestrian speed (m/s): Stationary (0 m/s), Slow (1 m/s), Fast (3 m/s)
- Pedestrian crossing angle (degrees): Toward ego car (0), Diagonal toward (45), Perpendicular (90), Diagonal away (135), Away from car (180)
- Ego car speed (m/s): Slow (<10 m/s), Medium (10-15 m/s), Fast (15-20 m/s)

The dimensions and ranges listed above result in 2,430 possible combinations. Using combinatorial testing, we create a set of 18 operational scenarios that provides pair-wise coverage of all equivalence classes.

**Operational Scenarios for SYS-ML-REQ2:**
- Object starting point (lateral offset from the road in meters): Left side of the road (-5 m), On the road (0 m), Right side of the road (5 m)
- Longitudinal distance from ego car (offset in meters): Close (<25m), Medium distance (25-50 m), Far away (>50 m)
- Object appearance: Sphere, Cube, Cone, Pyramid
- Object speed (m/s): Stationary (0 m/s), Slow (1 m/s), Fast (3 m/s)
- Ego car speed (m/s): Slow (<10 m/s), Medium (10-15 m/s), Fast (15-20 m/s)

The dimensions and ranges listed above result in 324 possible combinations. Using combinatorial testing, we create a set of 14 operational scenarios that provides pair-wise coverage of all equivalence classes.

For each operational scenario, two test parameters represent ranges of values, i.e., the longitudinal distance between ego car and the pedestrian and the speed of ego car. For these two test parameters, we identify a combination of values that result in a collision unless the SMIRK system initiates emergency braking. 

The complete set of operational scenarios, realized as 32 executable test scenarios in ESI Pro-SiVIC, are available in TODO: upload the test scripts.

## 4.2 System Test Cases ##
The system test cases are split into three categories. First, each operational scenario identified in Section 4.1 constitutes one system test case, i.e., Test Cases 1-32. Second, to increase the diversity of the test cases in the simulated environment, we complement the straitly reproducible Test Cases 1-32 with test case counterparts adding random jitter to the parameters. For test cases 1-32, we create analogous test cases that randomly add jitter in the range from -10\% to +10\% to all numerical values. Partial random testing has been proposed by Masuda (2017) in the context of test scenarios execution in vehicle simulators. Note that introducing random jitter to the test input does not lead to the test oracle problem, as we can automatically assess whether there is a collision between ego car and the pedestrian in ESI Pro-SiVIC or not (TC-RAND-[1-18]. Furthermore, for the test cases related to false positives, we know that emergency braking shall not commence. Consequently, the entries in the "Then" column are straightforward.

| Test Case ID   | Type                 | Given               | When       | Then         |
|----------------|----------------------|---------------------|------------|--------------|
| TC-OS-[1-18]   | Operational Scenario | Scenario [1-18]     | Pedestrian crosses the street | PAEB commences, no collision |
| TC-OS-[19-32]   | Operational Scenario | Scenario [19-32]     | Object crosses the street | PAEB does not commence |
| TC-RAND-[1-18] | Random Testing       | TC-OS-[1-18]+jitter | Pedestrian crosses the street | PAEB commences, no collision |
| TC-RAND-[19-32] | Random Testing       | TC-OS-[19-32]+jitter | Object crosses the street | PAEB does not commence |

The third category is requirements-based testing. Requirements-based testing is used to gain confidence that the functionality specified in the ML Safety Requirements has been implemented correctly (Hauer et al., 2019). The table below lists all system test cases, of all three categories, using the [Given-When-Then structure](https://en.wikipedia.org/wiki/Given-When-Then) as used in behavior-driven development. The top-level safety requirement SYS-SAF-REQ1 will be verified by testing of all underlying requirements, i.e., its constituent detailed requirements.

| Test Case ID | Requirement | Given    | When       | Then         |
|--------------|-------------|----------|------------|--------------|
| TC-REQ1-A    | SYS-ML-REQ1 | Scenario | Pedestrian | No collision |
| TC-REQ1-B    | SYS-ML-REQ1 | Scenario | Pedestrian | No collision |
| TC-REQ2-A    | SYS-ML-REQ2 | Scenario | Pedestrian | No collision |
| TC-REQ2-B    | SYS-ML-REQ2 | Scenario | Pedestrian | No collision |
| TC-REQ2-C    | SYS-ML-REQ2 | Scenario | Pedestrian | No collision |
|              |             |          |            |              |

# 5 ML Verification Argument Pattern [BB]
The figure below shows the ML verification argument pattern using GSN. The pattern closely resembles the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Verification_Argument_Pattern](/docs/figures/gsn-ml_verification_argument_pattern.png) <a name="gsn-ml_verification_argument"></a>

The top claim (G5.1) corresponds to the bottom claim in the safety requirements argument pattern [I], i.e., that all ML safety requirements are satisfied. The argumentation builds on a sub-claim and an argumentation strategy. First, sub-claim G5.2 is that the verification of the ML model is independent of its development. The verification log [AA] specifies how this has been achieved for SMIRK (Sn5.1). Second, the strategy S5.1 argues that test-based verification is an appropriate approach to generate evidence that the ML safety requirements are met. The justification is that the SMIRK [test strategy](#strategy) follows the proposed organization in peer-reviewed literature on ML testing, which is a better fit than using less mature formal methods for ML models as complex as YOLO. 

Following the test-based verification approach, the sub-claim G5.3 argues that the ML model satisfies the ML safety requirement when the verification data (C5.1) is applied. The testing claim is supported by three sub-claims. First, G5.4 argues that the test results demonstrate that the ML safety requirements are satisfied, for which Verification Test Results [Z] are presented as evidence. Second, G5.5 argues that the Verification Data [P] is sufficient to verify the intent of the ML safety requirements in the ODD. Third, G5.6 argues that the test platform is representative of the operational platform. Evidence for both G5.5 and G5.6 is presented in the Verification Log [AA].

# 6 ML Verification Argument [CC]
SMIRK instantiates the ML Verification Argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Verification Argument Pattern [BB]](</docs/System%20Test%20Specification.md#5-ml-verification-argument-pattern-bb>), as well as the following artefacts from preceding AMLAS activities:

- [ML Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) [H]
- [Verification Data](TBD) [P]
- [ML Model](TBD) [V]
