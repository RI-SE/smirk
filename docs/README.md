# SMIRK Documentation

In this folder, all documentation related to SMIRK is evolving. Everything is WIP.

- Software Requirements Specification (WIP)
- Architecture Specification (WIP)
- Test Specification (To appear)
- ALTAI_Numbered_Questions_v1.0.pdf (used in [SEthics21 paper](https://arxiv.org/abs/2103.09051))

## Safety Assurance

SMIRK evolves in compliance with [Guidance on the Assurance of Machine Learning in Autonomous Systems](https://www.york.ac.uk/assuring-autonomy/news/publications/amlas/) (AMLAS) published by the University of York. The figure below shows an overview of the AMLAS process and the six corresponding stages. 

![AMLAS process](/docs/figures/amlas_process.png) <a name="amlas"></a>

The table below is an index to navigate the artifacts mandated (cf. [ID]) by the AMLAS process. The input/output columns indicate in which AMLAS stage the artifact is used. The final column lists the location of the corresponding artifact for SMIRK.

|      ID   |     Title                                        |     Input to    |     Output from    |     Where?       |
|:---------:|--------------------------------------------------|:---------------:|:------------------:|------------------|
|     [A]   |     System Safety Requirements                     |         1, 6    |                    |     [SRS Sec 3](</docs/System Requirements Specification.md#system_safety_reqts>)    |
|     [B]   |     Description of Operating Environment of System |         1, 6    |                    |     [SRS Sec 4](</docs/System Requirements Specification.md#odd>)    |
|     [C]   |     System Description                             |         1, 6    |                    |     [SRS Sec 2](</docs/System Requirements Specification.md#system_reqts>)    |
|     [D]   |     ML Component Description                       |          1      |                    |     [SRS Sec 5](</docs/System Requirements Specification.md#ml_component_desc>)    |
|     [E]   |     Safety Requirements Allocated to ML Component  |          2      |            1       |     [SRS Sec 7](</docs/System Requirements Specification.md#ml_component_safety_reqts>)    |
|     [F]   |     ML Assurance Scoping Argument Pattern          |          1      |                    |     [SRS Sec 6](</docs/System Requirements Specification.md#ml_assurance_scoping_pattern>)    |
|     [G]   |     ML Safety Assurance Scoping Argument           |                 |            1       |     [SRS Sec 8](</docs/System Requirements Specification.md#ml_assurance_scoping_argument>)    |
|     [H]   |     ML Safety Requirements                         |       3, 4, 5   |            2       |                  |
|     [I]   |     ML Safety Requirements Argument Pattern        |          2      |                    |                  |
|     [J]   |     ML Safety Requirements Validation Results      |                 |            2       |                  |
|     [K]   |     ML Safety Requirements Argument                |                 |            2       |                  |
|     [L]   |     Data Requirements                              |                 |            3       |                  |
|     [M]   | Data Requirements Justification Report             |                 |          3         |                  |
|     [N]   | Development Data                                   |                 |          3         |                  |
|     [O]   | Internal Test Data                                 |                 |          3         |                  |
|     [P]   | Verification Data                                  |                 |          3         |                  |
|     [R]   |     ML Data Argument Pattern                       |          3      |                    |                  |
|     [Q]   |     Data Generation Log                            |                 |            3       |                  |
|     [R]   | ML Data Argument Pattern                           |        3        |                    |                  |
|     [S]   | ML Data Validation Results                         |                 |          3         |                  |
|     [T]   | ML Data Argument                                   |                 |          3         |                  |
|     [U]   |     Model Development Log                          |                 |          4         |                  |
|     [V]   | ML Model                                           |       5, 6      |          4         |                  |
|     [W]   |     ML Learning Argument Pattern                   |          4      |                    |                  |
|     [X]   |     Internal Test Results                          |                 |            4       |                  |
|     [Y]   |     ML Learning Argument                           |                 |            4       |                  |
|     [Z]   |     ML Verification Results                        |                 |            5       |                  |
|     [AA]  |     Verification Log                               |                 |            5       |                  |
|     [BB]  |     ML Verification Argument Pattern               |          5      |                    |                  |
|     [CC]  |     ML Verification Argument                       |                 |            5       |                  |
|     [DD]  |     Erroneous Behaviour Log                        |                 |            6       |                  |
|     [EE]  |     Operational scenarios                          |         6       |                    |                  |
|     [FF]  | Integration Testing Results                        |                 |          6         |                  |
|     [GG]  | ML Deployment Argument Pattern                     |        6        |                    |                  |
|     [HH]  |     ML Deployment Argument                         |                 |            6       |                  |
