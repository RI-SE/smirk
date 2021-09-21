# SMIRK Documentation

In this folder, all documentation related to SMIRK is evolving. Everything is WIP.

- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [Data Management Specification](</docs/Data Management Specification.md>)
- Architecture Specification (To appear)
- [Machine Learning Component Specification](</docs/ML Component Specification.md>)
- Test Specification (To appear)
- Deployment Specification (To appear)
- ALTAI_Numbered_Questions_v1.0.pdf (used in [SEthics21 paper](https://arxiv.org/abs/2103.09051))

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
|     [D]   |     ML Component Description                       |          1      |                    | [MLCS Sec 2](</docs/ML Component Specification.md#ml_comp_desc>)    | In progress |
|     [E]   |     Safety Requirements Allocated to ML Component  |          2      |            1       | [SRS Sec 3.2](</docs/System Requirements Specification.md#ml_component_safety_reqts>)    | Done |
|     [F]   |     ML Assurance Scoping Argument Pattern          |          1      |                    | [SRS Sec 6](</docs/System Requirements Specification.md#ml_assurance_scoping_pattern>)    | Done |
|     [G]   |     ML Safety Assurance Scoping Argument           |                 |            1       | [SRS Sec 7](</docs/System Requirements Specification.md#ml_assurance_scoping_argument>)    | Done |
|     [H]   |     ML Safety Requirements                         |       3, 4, 5   |            2       | [SRS Sec 3.3](</docs/System Requirements Specification.md#ml_safety_reqts>) | Done |
|     [I]   |     ML Safety Requirements Argument Pattern        |          2      |                    | [SRS Sec 8](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#8-ml-safety-requirements-argument-pattern-i) | Done |
|     [J]   |     ML Safety Requirements Validation Results      |                 |            2       | [SRS Sec 9](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#9-ml-safety-requirements-validation-results-j) | Formal inspection needed |
|     [K]   |     ML Safety Requirements Argument                |                 |            2       | [SRS Sec 10](https://github.com/RI-SE/smirk/blob/main/docs/System%20Requirements%20Specification.md#10-ml-safety-requirements-argument-k) | Done |
|     [L]   |     Data Requirements                              |                 |            3       | [DMS Sec 2](</docs/Data Management Specification.md#data_rqts>) | Done |
|     [M]   | Data Requirements Justification Report             |                 |          3         | [DMS Sec 3](</docs/Data Management Specification.md#data_rqts_just>) | In progress |
|     [N]   | Development Data                                   |                 |          3         | TBD | In progress |
|     [O]   | Internal Test Data                                 |                 |          3         | TBD | In progress |
|     [P]   | Verification Data                                  |                 |          3         | TBD | In progress |
|     [Q]   |     Data Generation Log                            |                 |            3       | [DMS Sec 4](</docs/Data Management Specification.md#data_gen>) | In progress |
|     [R]   | ML Data Argument Pattern                           |        3        |                    | [DMS Sec 5](</docs/Data Management Specification.md#data_argument_pattern>) | Done |
|     [S]   | ML Data Validation Results                         |                 |          3         | [DMS Sec 6](</docs/Data Management Specification.md#data_validation_results>) | In progress |
|     [T]   | ML Data Argument                                   |                 |          3         | [DMS Sec 7](</docs/Data Management Specification.md#data_argument>) | Not started |
|     [U]   |     Model Development Log                          |                 |          4         | TBD | Not started |
|     [V]   | ML Model                                           |       5, 6      |          4         | TBD | In progress |
|     [W]   |     ML Learning Argument Pattern                   |          4      |                    | TBD | Not started |
|     [X]   |     Internal Test Results                          |                 |            4       | TBD | Not started |
|     [Y]   |     ML Learning Argument                           |                 |            4       | TBD | Not started |
|     [Z]   |     ML Verification Results                        |                 |            5       | TBD | Not started |
|     [AA]  |     Verification Log                               |                 |            5       | TBD | Not started |
|     [BB]  |     ML Verification Argument Pattern               |          5      |                    | TBD | Not started |
|     [CC]  |     ML Verification Argument                       |                 |            5       | TBD | Not started |
|     [DD]  |     Erroneous Behaviour Log                        |                 |            6       | TBD | Not started |
|     [EE]  |     Operational scenarios                          |         6       |                    | TBD | Not started |
|     [FF]  | Integration Testing Results                        |                 |          6         | TBD | Not started |
|     [GG]  | ML Deployment Argument Pattern                     |        6        |                    | TBD | Not started |
|     [HH]  |     ML Deployment Argument                         |                 |            6       | TBD | Not started |
