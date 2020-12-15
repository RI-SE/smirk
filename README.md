# SMIRK

SMIRK is an experimental pedestrian emergency breaking ADAS facilitating research on quality assurance of critical components that rely on machine learning.

- Domain: Automotive, Advanced Driver-Assistance Systems (ADAS)
- Keywords: automotive, machine learning, computer vision, functional safety, SOTIF, quality assurance, AI testing 
- Responsible unit at RISE: Digital Systems/Mobility and Systems/Humanized Autonomy
- Related research projects: SMILEIII, SODA, AIQ Meta-Testbed
- License: MIT

## Description

SMIRK is a research prototype under development that facilitates research on verification and validation (V&V) of safety-critical systems embedding Machine Learning components. SMIRK responds to calls for a fully transparent ML-based Advanced Driver-Assistance System (ADAS) to act as a system-under-test in research on trusted AI [[1]](#1). SMIRK will provide pedestrian emergency braking. By combining trained and coded software, SMIRK will become a baseline Software-Under-Test (SUT) for ML testing research targeting automotive perception applications such as object detection and path planning. To ensure industrial relevance, SMIRK will implement a reference architecture while adhering to development practices mandated by contemporary automotive safety standards [[2]](#2).

## Branching Model

The SMIRK development follows the [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model. The model uses two infinite branches (master and develop) and two types of supporting branches (feature and hotfix branches).

- master - the main branch where the source code of HEAD always reflects a production-ready state.
- develop - where the main development is reflected. Merges with master.
- feature-x - used to develop new features for the upcoming release. Merges with develop.
-	hotfix-x - used when it is necessary to act immediately upon an undesired state of a live production version. Merges with master.

## References
<a id="1">[1]</a> https://ec.europa.eu/digital-single-market/en/news/assessment-list-trustworthy-artificial-intelligence-altai-self-assessment

<a id="2">[2]</a> https://www.iso.org/standard/70939.html
