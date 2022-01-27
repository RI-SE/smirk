# SMIRK Documentation

The following documents are available in this folder.

- [System Requirements Specification](</docs/System Requirements Specification.md>) (SRS)
- [Data Management Specification](</docs/Data Management Specification.md>) (DMS)
- [System Architecture Description](https://github.com/RI-SE/smirk/blob/main/docs/System%20Architecture%20Description.md) (SAD)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>) (MLCS)
- [System Test Specification](</docs/System Test Specification.md>) (STS)
- [Deployment Specification](</docs/Deployment Specification.md>) (DS)

Supplementary documents
- [Numbered ALTAI questions](</docs/support/ALTAI_Numbered_Questions_v1.0.pdf>) from the Assessment List for Trustworthy Artificial Intelligence. The European Commission published ALTAI to support self-assessment. The questions were used in a paper on [AI ethics](https://arxiv.org/abs/2103.09051).

## Safety Assurance

SMIRK evolves in compliance with [Guidance on the Assurance of Machine Learning in Autonomous Systems](https://www.york.ac.uk/assuring-autonomy/guidance/amlas/) (AMLAS) published by the University of York. The figure below shows an overview of the AMLAS process and the six corresponding stages. 

![AMLAS process](/docs/figures/amlas_process.png) <a name="amlas"></a>

The table below is an index to navigate the artifacts mandated (cf. [ID]) by the AMLAS process. The input/output columns indicate in which AMLAS stage the artifact is used. The final column lists the location of the corresponding artifact for SMIRK.

The set of artifacts listed constitutes the safety case for the ML-based object detection component of SMIRK, i.e., it instantiates the [ML Assurance Scoping Pattern](</docs/System Requirements Specification.md#ml_assurance_scoping_pattern>).

|      ID   |     Title                                        |     Input to    |     Output from    |     Where?       |     Status       |
|:---------:|--------------------------------------------------|:---------------:|:------------------:|------------------|------------------|
|     [A]   |     System Safety Requirements                     |         1, 6    |                    | [SRS Sec 3.1](</docs/System Requirements Specification.md#system_safety_reqts>)    | Done |
|     [B]   |     Description of Operating Environment of System |         1, 6    |                    | [SRS Sec 4](</docs/System Requirements Specification.md#odd>)    | Done |
|     [C]   |     System Description                             |         1, 6    |                    | [SRS Sec 2](</docs/System Requirements Specification.md#system_reqts>)    | Done |
|     [D]   |     ML Component Description                       |          1      |                    | [MLCS Sec 2](</docs/ML Component Specification.md#ml_comp_desc>)    | Outlier detection missing |
|     [E]   |     Safety Requirements Allocated to ML Component  |          2      |            1       | [SRS Sec 3.2](</docs/System Requirements Specification.md#ml_component_safety_reqts>)    | Done |
|     [F]   |     ML Assurance Scoping Argument Pattern          |          1      |                    | [SRS Sec 6](</docs/System Requirements Specification.md#ml_assurance_scoping_pattern>)    | Done |
|     [G]   |     ML Safety Assurance Scoping Argument           |                 |            1       | [SRS Sec 7](</docs/System Requirements Specification.md#ml_assurance_scoping_argument>)    | Done |
|     [H]   |     ML Safety Requirements                         |       3, 4, 5   |            2       | [SRS Sec 3.3](</docs/System Requirements Specification.md#ml_safety_reqts>) | Done |
|     [I]   |     ML Safety Requirements Argument Pattern        |          2      |                    | [SRS Sec 8](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#7-ml-safety-requirements-argument-pattern-i) | Done |
|     [J]   |     ML Safety Requirements Validation Results      |                 |            2       | [SRS Sec 9](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#8-ml-safety-requirements-validation-results-j) | Done |
|     [K]   |     ML Safety Requirements Argument                |                 |            2       | [SRS Sec 10](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#10-ml-safety-requirements-argument-k) | Done |
|     [L]   |     Data Requirements                              |                 |            3       | [DMS Sec 2](</docs/Data Management Specification.md#data_rqts>) | Done |
|     [M]   | Data Requirements Justification Report             |                 |          3         | [DMS Sec 3](</docs/Data Management Specification.md#data_rqts_just>) | Done |
|     [N]   | Development Data                                   |                 |          3         | TBD | Hosting needed |
|     [O]   | Internal Test Data                                 |                 |          3         | TBD | Hosting needed |
|     [P]   | Verification Data                                  |                 |          3         | TBD | Hosting needed |
|     [Q]   | Data Generation Log                            |                 |            3       | [DMS Sec 4](</docs/Data Management Specification.md#data_gen>) | Links and validation needed |
|     [R]   | ML Data Argument Pattern                           |        3        |                    | [DMS Sec 5](</docs/Data Management Specification.md#data_argument_pattern>) | Done |
|     [S]   | ML Data Validation Results                         |                 |          3         | [DMS Sec 6](</docs/Data Management Specification.md#data_validation_results>) | Formal inspection needed |
|     [T]   | ML Data Argument                                   |                 |          3         | [DMS Sec 7](</docs/Data Management Specification.md#data_argument>) | Done |
|     [U]   | Model Development Log                          |                 |          4         | [MLCS Sec 3](</docs/ML%20Component%20Specification.md#3-model-development-log-u>) | In progress |
|     [V]   | ML Model                                           |       5, 6      |          4         | TBD | In progress |
|     [W]   | ML Learning Argument Pattern                   |          4      |                    | [MLCS Sec 5](</docs/ML%20Component%20Specification.md#5-ml-model-learning-argument-pattern-w>) | Done |
|     [X]   | Internal Test Results                          |                 |            4       | [Protocols](https://github.com/RI-SE/smirk/blob/main/docs/protocols/) | In progress |
|     [Y]   | ML Learning Argument                           |                 |            4       | [MLCS Sec 6](</docs/ML%20Component%20Specification.md#6-ml-learning-argument-y>) | Done |
|     [Z]   | ML Verification Results                        |                 |            5       | [Protocols](https://github.com/RI-SE/smirk/blob/main/docs/protocols/) | In progress |
|     [AA]  | Verification Log                               |                 |            5       | TBD | In progress |
|     [BB]  | ML Verification Argument Pattern               |          5      |                    | [STS Sec 5](</docs/System%20Test%20Specification.md#5-ml-verification-argument-pattern-bb>) | Done |
|     [CC]  | ML Verification Argument                       |                 |            5       | [STS Sec 6](https://github.com/RI-SE/smirk/blob/main/docs/System%20Test%20Specification.md#6-ml-verification-argument-cc) | Done |
|     [DD]  | Erroneous Behaviour Log                        |                 |            6       | TBD | Not started |
|     [EE]  | Operational scenarios                          |         6       |                    | [STS Sec 4.1](https://github.com/RI-SE/smirk/blob/main/docs/System%20Test%20Specification.md#41-operational-scenarios-ee) | Done |
|     [FF]  | Integration Testing Results                        |                 |          6         | [Protocols](https://github.com/RI-SE/smirk/blob/main/docs/protocols/) | Not started |
|     [GG]  | ML Deployment Argument Pattern                     |        6        |                    | [DS Sec 5](</docs/Deployment%20Specification.md#5-ml-deployment-argument-pattern-bb>) | Done |
|     [HH]  | ML Deployment Argument                         |                 |            6       | TBD | Not started |
