# Data Management Specification 

Revision History
<table>
<tr>
<th>Olof Lennartsson</th>
<th>2021-05-20</th>
<th>Initial SMILE version.</th>
<th>0.1</th>
</tr>
<tr>
<td></td>
<td></td>
<td></td>
<td></td>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document describes the data management (DM) strategy used when developing SMIRK in the research project SMILE III. This strategy is built upon RQ3 from
the research proposal. Using the literature, the strategy has been built upon previous studies on how to ensure robustness and safety in safety-critical
machine learning models. A fundamental data-set is created from the requirements of the data. The neural network (NN) is trained on this data set.

Pro-Sivic/CARLA is used to simulate the specific cases, to test how well the NN can generalize and detect hazards. Using the output of the safety cage,
that is placed around the NN, corner cases can be detected. The corner cases will be saved in a data bank. The information given by the data bank can
then be used to investigate if the requirements are properly defined. Once the requirements fulfill the operational design domain (ODD), the corner
cases in the data bank will be used to fine-tune the NN [3]. The process is repeated iteratively until the NN achieves a satisfactory magnitude of some
specific metrics.

## 1.1 Purpose ##
TBD.

## 1.2 Document Conventions ##
Headings with a reference in brackets [X] refer to artifacts mandated by the AMLAS process.

## 1.3 Glossary
- AMLAS Guidance on the Assurance of Machine Learning in Autonomous Systems
- ML: Machine Learning

## 1.4 Intended Audience and Reading Suggestions ##

## 1.6 References ##
- Development Data [N]
- Internal Test Data [O]
- Verification Data [P]
- [1] C. Thomas A. Pereira. Challenges of Machine Learning Applied to Safety-Critical Cyber-Physical Systems. 2020.
- [2] Rob Ashmore, Radu Calinescu, and Colin Paterson. Assuring the Machine Learning Lifecycle: Desiderata, Methods, and Challenges. 2019.
arXiv: 1905.04223 [cs.LG].
- [3] A. Freytag C. Käding E. Rodner and J. Denzler. Fine-tuning Deep Neural Networks in Continuous Learning Scenarios. 2016.
- [4] Edward Schwalb. Analysis of Safety of The Intended Use (SOTIF).

# 2 Data Requirements [L] <a name="data_rqts"></a>
The initial dataset, used to train the NN-model in the first iteration, is a representation of the ODD. How exact of a representation it is, is hard to
measure before development. However, as the system behavior is dependent on the definition of the ODD, control of the initial dataset is needed (This is
further discussed in Chapter 3 Data Acquisition). To guide the definition of requirements in general R. Ashmore et. al. [2] provides a good description
of this. It is also discussed in A. Pereira’s work [1]. The specification of the data needs to be determined so that one knows what classes are relevant in terms of the ODD. All classes need to be represented in the data set. All classes need to be represented in the data-set. The data-set must cover critical scenarios and known scenarios. According to SOTIF [4], all possible situations the system may encounter can be divided into four categories, safe/unsafe known and safe/unsafe unknown ones. All known scenarios must be included in the data-set. The classes must be evenly distributed [2].

# 3 Data Requirements Justification Report [M] <a name="data_rqts_just"></a>
TBD.

# 4 Data Generation Log [Q] <a name="data_gen"></a>

## 4.1 Data Collection
Collect data from a simulation or the real world. In SMILEIII we will collect it from Pro-Sivic/CARLA. The main benefit with using simulators is that the data is usually annotated programmatically by the simulation software.

## 4.2 Data Cleaning
Data needs to be cleaned after it has been collected: Outliers, conflicted and Irrelevant data, in terms of the ODD, needs to be excluded along with data that have fatal errors.

## 4.3 Preprocessing
Normalization of data, e.g., make all images (for a perception model) the same size. If collecting from the real world, simulated data could be added both as disturbances in real world images and as synthetic data. GA, GANs can be used to automatically create “lookalike twins” of data to increase the size and diversity of the data-set.

# 5 ML Data Argument Pattern [R] <a name="data_argument_pattern"></a>
TBD.

# 6 ML Data Validation Results [S] <a name="data_validation_results"></a>
TBD.

# 7 ML Data Argument [T] <a name="data_argument"></a>
TBD.

# 8 Collecting Complementary Online Data
This section describes an overall approach for how to continuously expand the data-sets using the safety cage and a data-bank.

## 8.1 Data-bank
When a data set is defined, the NN is trained. After training, the NN is deployed in a simulation where it is exposed to the different cases defined in
the ODD. A safety cage is used to measure how well the NN is generalizing on the different scenarios. The safety cage output will indicate how well
the NN is generalizing on a specific data type and as an indication or safety measure.

The data-bank is a set of data points, representing failed/passed scenarios run within the simulator. When an example is stored in the data-bank is explained further down.

## 8.2 Safety Cage
The safety cage for SMILEIII is yet to be defined. From SMILEII one can conclude that the safety cage must act as an indicator of how well images,
in this case, are classified. The safety cage can mediate this with different metrics. Such as classification score, AROC, or anomaly score. By analyzing
this output from a classified data type, one can determine if the NN is generalizing ”good enough” or not. Good enough will be a design parameter,
usually defined as a threshold and determined by the safety owner/tester. By implementing the safety cage, the outcome can be any of the three
for a given simulated scenario:

- Alternative 1: Rejected based on anomaly score. The data type is classified with a metric value that doesn’t fulfill the requirements to be regarded as safe/certain. That data type will be rejected to the data-bank.
- Alternative 2: Accepted based on anomaly score. The data is classified with a metric value that fulfills the requirements to be regarded as safe/certain. This type of data will be accepted and not to be sent to the data-bank.
- Alternative 3: Rejected based on misclassification. The data is classified with a metric value that fulfills the requirements to be regarded as safe/certain, however, the simulation provides that the situation is a false positive/false negative (FP/FN). This means that the model is certain of something that actually is false. This type of classification errors must be detected and the NN should be fine-tuned on this as well. The data type that generated such behavior must be sent to the data-bank.

## 8.3 Preprocessing of Data in Data-Bank
When a batch of corner cases is captured in the data-bank, it can be a good opportunity to expand the set by different types of augmenting techniques. It can be filtering or modified by GAs and GANs. How this will be done will be investigated later in the SMILEIII project.

# 9 Using the Data-bank in Development
Here, two ways of using the data-bank will be presented. The first one handles a less mature system and the second one will be the final procedure to use when enhancing the model on corner cases. Both are iterative processes.

## 9.1 Requirement/Initial Data refinement (Low Level)
To ensure a well-defined ODD one needs to be prepared to update it. Once the ODD is defined it can’t be left unchanged if the model is clearly missing the ability to generalize on classes that are not regarded as corner cases. The ODD may be too weak, or the representation in the initial data lacking information. Using this technique might ensure a stronger representation of the known scenarios.

## 9.2 Fine-tuning of Neural Network (High Level)
The preprocessed data in the data-bank works as a second data set in the following iteration. To increase the model performance the second data set is used to fine tune NN. The fine-tuning procedure will be incremental. For every iteration, a number of corner cases will be sent to the data-bank. It is then used to fine tune NN [4].

# 10 Summary
suggested. The details are not set, as for specific GA/GANs to modify the data, thresholds and precision targets. However, a more general strategy is presented.

The safety of the NN must be ensured by utilizing the corner cases that are recognized in the safety cage. The safety cage is yet to be developed by QRTECH. The safety cage filters different corner cases to a data-bank where these will be preprocessed and analyzed. From data in the bank, a new data set is generated which will be used to fine-tune the NN.
