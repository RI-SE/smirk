# SMIRK
SMIRK is an experimental pedestrian emergency braking ADAS facilitating research on quality assurance of critical components that rely on machine learning.

![Logo](/docs/figures/smirk.png) <a name="logo"></a>

- Domain: Automotive, Advanced Driver-Assistance Systems (ADAS)
- Keywords: automotive, machine learning, computer vision, functional safety, SOTIF, quality assurance, AI testing 
- Responsible unit at RISE: Digital Systems/Mobility and Systems/Humanized Autonomy
- Related research projects: SMILEIII, SODA, AIQ Meta-Testbed, VALU3S
- License: [MIT](https://github.com/RI-SE/smirk/blob/main/LICENSE)

## Description

SMIRK is a research prototype under development that facilitates research on verification and validation (V&V) of safety-critical systems embedding Machine Learning components. SMIRK responds to calls for a fully transparent ML-based Advanced Driver-Assistance System (ADAS) to act as a system-under-test in research on trusted AI [[1]](#1). SMIRK will provide pedestrian emergency braking. By combining trained and coded software, SMIRK will become a baseline Software-Under-Test (SUT) for ML testing research targeting automotive perception applications such as object detection and path planning. To ensure industrial relevance, SMIRK will implement a reference architecture while adhering to development practices mandated by contemporary automotive safety standards [[2]](#2).

## Branching Model

The SMIRK development follows the popular [git-flow](https://nvie.com/posts/a-successful-git-branching-model/) branching model. The model uses two *infinite* branches (`master` and `develop`) and two types of supporting branches (`feature` and `hotfix` branches). Supporting branches shall be *ephemeral*, i.e., they should only last as long as the feature or hotfix itself is in development. Once completed, they shall be merged back into one of the infitine branches and/or discarded.

In the following examples, `feature-x` or `hotfix-x` shall be replaced with a short phrase describing the feature or hotfix.

- `master` - the main branch where the source code of HEAD always reflects a production-ready state.
- `develop` - where the main development is reflected. Merges into `master`.
- `feature-x` - used to develop new features for the upcoming release. Merges into `develop`.
-	`hotfix-x` - used when it is necessary to act immediately upon an undesired state of a live production version. Merges into `master`.

The repository administrators are responsible for deleting the remote copies of ephemeral branches and updating the version tag for the `master` branch.

External pull requests are welcome, but must be reviewed before they can be merged into the master branch. Reviewers may ask questions or make suggestions for edits and improvements before your feature can be merged. If your feature branch pull request is not accepted, make the necessary adjustments or fixes as indicated by the repository administrators and redo the pull request.

For a longer desciption of the branching model, please refer to our [examples](https://github.com/RI-SE/smirk/blob/main/branching.md).

## References
<a id="1">[1]</a> https://ec.europa.eu/digital-single-market/en/news/assessment-list-trustworthy-artificial-intelligence-altai-self-assessment

<a id="2">[2]</a> https://www.iso.org/standard/70939.html
