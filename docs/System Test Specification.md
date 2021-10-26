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
The testing process must be independent from the development. Neither developers nor ML developers can have access to this document.

- Developers: Must not have access to the document.
- ML developers: Must not have access to the document.
- Testers: The entire document is important.
- Safety assessors: The entire document is important.
- Other stakeholders: TBD

## 1.6 References ##
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)
- Borg, Bronson, Christensson, Olsson, Lennartsson, Sonnsjö, Ebadi, and Karsberg, 2021. Exploring the Assessment List for Trustworthy AI in the Context of Advanced Driver-Assistance Systems, In Proc. of the 2nd Workshop on Ethics in Software Engineering Research and Practice.
- Riccio, Jahangirova, Stocco, Humbatova, Weiss, and Tonella. Testing Machine Learning Based Systems: A Systematic Mapping, Empirical Software Engineering, 25, 5193-5254, 2020.
- Zhang, Harman, Ma, and Liu. Machine Learning Testing: Survey, Landscapes and Horizons. IEEE Transactions on Software Engineering, 2020.

# 2 ML Test Strategy <a name="strategy"></a>
This section describes the overall ML test strategy. The SMIRK ML-based object detection component is tested on multiple levels.

- Dataset testing: This level refers to automatic checks that verify that specific properties of the dataset are satisfied. As described in the [ML Data Validation Results](https://github.com/RI-SE/smirk/blob/main/docs/Data%20Management%20Specification.md#6-ml-data-validation-results-s-), the data validation includes automated testing of the Balance desiderata. Zhang et al. (2020) refer to dataset testing as Input testing.
- Model testing: Testing that the ML model provides the expected output. This is the primary focus of academic research on ML testing, and includes white-box, black-box, and data-box access levels during testing (Riccio et al., 2020). This is described in Section 3.
- Unit testing: Conventional unit testing on the level of Python classes. SMIRK provides a test suite for execution with the pytest framework.
- System testing: System-level testing of the SMIRK ADAS. All test cases are designed for execution in ESI Pro-SiVIC. The system testing targets the requirements in the [System Requirements Specification](</docs/System Requirements Specification.md>).

# 3 ML Model Test Cases
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

Results from running ML model testing are document in the [Protocols folder](https://github.com/RI-SE/smirk/blob/main/docs/protocols/).

# 4 System Test Cases

# 5 ML Verification Argument Pattern [BB]
The figure below shows the ML verification argument pattern using GSN. The pattern closely resembles the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Verification_Argument_Pattern](/docs/figures/gsn-ml_verification_argument_pattern.png) <a name="gsn-ml_verification_argument"></a>

The top claim (G5.1) corresponds to the bottom claim in the safety requirements argument pattern [I], i.e., that all ML safety requirements are satisfied. The argumentation builds on a sub-claim and an argumentation strategy. First, sub-claim G5.2 is that the verification of the ML model is independent of its development. The verification log [AA] specifies how this has been achieved for SMIRK (Sn5.1). Second, the strategy S5.1 argues that test-based verification is an appropriate approach to generate evidence that the ML safety requirements are met. The justification is that the SMIRK [test strategy](#strategy) follows the proposed organization in peer-reviewed literature on ML testing, which is a better fit than using less mature formal methods for ML models as complex as YOLO. 

Following the test-based verification approach, the sub-claim G5.3 argues that that the ML model satisfies the ML safety requirement when the verification data (C5.1) is applied. The testing claim is supported by three sub-claims. First, G5.4 argues that the test results demonstrate that the ML safety requirements are satisfied, for which Verification Test Results [Z] are presented as evidence. Second, G5.5 argues that the Verification Data [P] is sufficient to verify the intent of the ML safety requirements in the ODD. Third, G5.6 argues that the test platform is representative of the operational platform. Evidence for both G5.5 and G5.6 is presented in the Verification Log [AA].
