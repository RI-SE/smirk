# SMIRK
SMIRK is an experimental pedestrian emergency braking ADAS facilitating research on quality assurance of critical components that rely on machine learning.

![Logo](/docs/figures/smirk.png) <a name="logo"></a>

- Domain: Automotive, Advanced Driver-Assistance Systems (ADAS)
- Keywords: automotive, machine learning, computer vision, functional safety, SOTIF, quality assurance, AI testing 
- Responsible unit at RISE: Digital Systems/Mobility and Systems/Humanized Autonomy
- Related research projects: SMILEIII, SODA, AIQ Meta-Testbed, VALU3S
- License: [GPL3-0](https://github.com/RI-SE/smirk/blob/main/LICENSE)

## Description
SMIRK is a research prototype under development that facilitates research on verification and validation (V&V) of safety-critical systems embedding Machine Learning (ML) components. SMIRK responds to calls for a fully transparent ML-based Advanced Driver-Assistance System (ADAS) to act as a system-under-test in research on trusted AI [[1]](#1). SMIRK provides pedestrian emergency braking. By combining trained and coded software, SMIRK is intended to become a baseline Software-Under-Test (SUT) for ML testing research targeting automotive perception applications such as object detection and path planning. To ensure industrial relevance, SMIRK will implement a reference architecture while adhering to development practices mandated by contemporary automotive safety standards [[2]](#2) and we is complemented by a fully transparent safety case.

## Purpose and Limitations
The SMIRK safety case is restricted to the novel challenges introduced by ML. The development adheres to the overall process described in the publicly available  specification *ISO/PAS 21448:2019 Road vehicles — Safety of the intended functionality* and we provide ML assurance by following the methodology for *Assurance of Machine Learning for use in Autonomous Systems* (AMLAS). Demonstrating compliance with the quintessential automotive software standard *ISO 26262:2018 Road vehicles — Functional safety* is out of the scope of this research project. We make the simplified assumption that the overall development context embedded the development of the ML-based SMIRK ADAS fulfills all aspects of ISO 26262, e.g., regarding processes, practices, and tools. While we will use third party open-source software in SMIRK (both incorporated as assets in the product and as tool support for software testing), we will not provide any safety assurance of external tools - instead we assume that the development organization has the capability to do so.

## Disclaimer
SMIRK is developed for use in simulated environments. Under no circumstances shall SMIRK be used in real vehicles operating in the physical world. You assume all responsibility and risk for the use of the SMIRK or any resources available on or through this GitHub repository. RISE Research Institutes of Sweden does not assume any liability for the materials, information and opinions provided on, or available through, this web page. No advice or information given by RISE Research Institutes of Sweden or its employees shall create any warranty. Reliance on such advice, information or the content of this web page is solely at your own risk, including without limitation any safety guidelines, resources or precautions related to the installation, operation, maintenance or evolution of SMIRK or any other information related to safety that may be available on or through this web page. RISE Research Institutes of Sweden disclaims any liability for injury, death or damages resulting from the use thereof. 

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

## Quickstart
Create a python 3.7 virtual environment with your preferred tool e.g. using conda:

```
$ conda create -n=smirk-env python=3.7
$ conda activate smirk-env
```

Installation in interactive mode currently requires [poetry](https://python-poetry.org/). Once poetry is installed SMRIK can be installed as follows:

```
$ git clone https://github.com/RI-SE/smirk && cd smirk
$ poetry install
```

This will allow you to use the smirk CLI command to reproduce the smirk results or try your own configurations.

Use the `-h` option to see additional help.

```
$ smirk -h

Usage: smirk [OPTIONS] COMMAND [ARGS]...

  Experimental pedestrian emergency breaking ADAS facilitating research
  on quality assurance of critical components that rely on machine
  learning.

Options:
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  detect    Training and evaluation of pedestrian detection models.
  generate  Data generation
  safety    Outlier detection training and evaluation.
  test      System simulator testing.
```

The `-h` option is available for sub-commands as well e.g.:

```
$ smirk detect eval -h

Usage: smirk detect eval [OPTIONS]

  Evalute pedestrian detection model.

Options:
  -d, --data DIRECTORY  Path to dataset directory  [required]
  -w, --weights FILE    Path to model weights  [required]
  --conf FLOAT          Confidence threshold  [required]
  --batch-size INTEGER  Batch size
  -h, --help            Show this message and exit.
```

Further instructions on reproducing the results and running custom experiments will be provided in the [docs](/docs/README.md).

## References
<a id="1">[1]</a> https://futurium.ec.europa.eu/en/european-ai-alliance/pages/altai-assessment-list-trustworthy-artificial-intelligence)

<a id="2">[2]</a> https://www.iso.org/standard/70939.html
