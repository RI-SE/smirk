# Machine Learning Component Specification v0.99

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
<td>2021-09-21</th>
<td>Initial template.</th>
<td>0.1</th>
</tr>
<tr>
<td>Markus Borg</td>
<td>2021-09-27</td>
<td>Toward a complete draft.</td>
<td>0.2</td>
</tr>
<tr>
<td>Markus Borg</td>
<td>2022-06-16</td>
<td>Complete draft.</td>
<td>0.9</td>
</tr>
<tr>
<td>Markus Borg, Kasper Socha, Jens Henriksson</th>
<td>2022-06-16</th>
<td>Beta Release - Ready for peer-review</th>
<td>0.99</th>
</tr>
</table>

# 1 Introduction <a name="introduction"></a>
This document contains the machine learning (ML) component specification for SMIRK – a pedestrian automatic emergency braking (PAEB) system. SMIRK is an advanced driver-assistance system (ADAS), intended to act as one of several systems supporting the driver in the dynamic driving task, i.e., all the real-time operational and tactical functions required to operate a vehicle in on-road traffic. SMIRK, including the accompanying safety case, is developed with full transparancy under an open-source software (OSS) license. We develop SMIRK as a demonstrator in a simulated environment provided by ESI Pro-SiVIC.

## 1.1 Purpose ##
This document describes the ML-based pedestrian recognition component used in SMIRK. Two established third-party OSS libraries are important constituents. First, the document describes how the object detection architecture [YOLOv5](https://github.com/ultralytics/yolov5) by Ultralytics is used and trained for the SMIRK operational design domain (ODD). Second, we introduce how the safety cage architecture is realized using out-of-distribution (OOD) detection provided by SeldonIO's [Alibi Detect](https://github.com/SeldonIO/alibi-detect). Third, we provide the ML model learning argument patterns in line with the Guidance on the Assurance of Machine Learning in Autonomous Systems (AMLAS).

## 1.2 Document Conventions ##
The number of academic publications in the list of references is unconventional for technical project doumentation. This is a conscious decision. SMIRK is developed as a prototype in the context of a research project with limited resources. As part of our research, we aim to integrate (sometimes scattered) pieces from the state-of-the-art literature. Synthesis is a fundamental tool in our research and we seek novel insights while focusing on refinement and integration. We actively choose to rely on reuse of design decisions from previously peer-reviewed publications. Building on previous work, i.e., [standing on the shoulders of others](https://en.wikipedia.org/wiki/Standing_on_the_shoulders_of_giants), is a core concept in research that allows validation of previous work, incl. previously proposed requirements. When available, and unless open access publication models have been used, links to academic publications point to preprints on open repositories such as [arXiv](https://arxiv.org/) rather than peer-reviewed revisions behind paywalls.

Headings with a reference in brackets [X] refer to artifacts prescribed by the AMLAS process ([Guidance on the Assurance of Machine Learning in Autonomous Systems](https://www.york.ac.uk/media/assuring-autonomy/documents/AMLASv1.1.pdf)). Due to formatting limitations in GitHub MarkDown, all figure and table captions appear in italic font to distinguish them from the running text. Explanatory text copied verbatim from public documents are highlighted using the quote formatting available in GitHub Markdown.

## 1.3 Glossary
- AMLAS: Guidance on the Assurance of Machine Learning in Autonomous Systems
- DNN: Deep Neural Network
- ML: Machine Learning
- ODD: Operational Design Domain
- OOD: Out-Of-Distribution
- OSS: Open Source Software
- YOLO: You Only Look Once

## 1.4 Intended Audience and Reading Suggestions ##
The section is organized into internal stakeholders, i.e., roles that are directly involved in the SMIRK development, and external stakeholders who are linked indirectly but have significant contribution in the successful completion of the SMIRK project. External stakeholders also include the ML safety community at large. Note that AMLAS prescribes a split between testers that are involved during the development and testers that are "sufficiently independent from the development activities." We refer to these roles as *internal testers* and *independent testers*, respectively.

**Internal stakeholders**
- Software developers: [Section 2 (ML Component Description)](#2-ml-component-description-d-) provides an overview of the ML component.
- ML developers: The entire document is relevant.
- Internal testers: The entire document is relevant for ML testers. Other testers should read [Section 2 (ML Component Description)](#2-ml-component-description-d-) for an overview.
- Independent testers: The entire document is relevant for ML testers. Other testers should read [Section 2 (ML Component Description)](#2-ml-component-description-d-) for an overview.

**External stakeholders**
- Safety assessors: Focus on headings that map to the AMLAS process, indicated with letters in brackets.
- Researchers: Academic and industrial reserachers active in ML safety are likely to find the most value in [Section 2 (ML Component Description)](#2-ml-component-description-d-) and [Section 3 (ML Development Log)](#3-ml-development-log-u-). 
- Standardization bodies and legislators: An overview of the safety argumentation is presented in [Section 5 (ML Component Specification)](#5-ml-model-learning-argument-pattern-w).
- Curious readers: For an overview of the use of ML components in SMIRK, read [Section 1 (Introduction)](#1-introduction).

## 1.6 References ##
The references are organized into 1) internal SMIRK documentation, 2) SMIRK data sets, 3) peer-reviewed publications, and 4) gray literature and white papers. When a reference listed under category 2) or 3) is used to motivate a design decision or a specific requirement, there is an explicit reference in the running text. Note that this DMS is self-contained, the references are provided for traceability to the underlying design rationales. Interested readers are referred to the discussions in the original sources.

**Internal SMIRK documentation**
- [System Requirements Specification](</docs/System Requirements Specification.md>)
- [System Architecture Description](</docs/System Architecture Description.md>)
- [Data Management Specification](</docs/Data Management Specification.md>)

**SMIRK data sets**
- Development Data [N]
- Internal Test Data [O]
- Verification Data [P]

**Peer-reviewed publications**
- An and Cho, 2015. [Variational Autoencoder Based Anomaly Detection Using Reconstruction Probability](http://dm.snu.ac.kr/static/docs/TR/SNUDM-TR-2015-03.pdf). Special Lecture on IE 2(1), SNU Data Mining Center, pp. 1-18.
- Klaise, Van Looveren, Cox, Vacanti, and Coca, 2020. [Monitoring and Explainability of Models in Production](https://arxiv.org/abs/2007.06299). In *Proc. of the ICML Workshop on Challenges in Deploying and Monitoring Machine Learning Systems*.
- Liu, Qi, Qin, Shi, and Jia, 2018. [Path Aggregation Network for Instance Segmentation](https://arxiv.org/abs/1803.01534). In *Proc. of the IEEE Conference on Computer Vision and Pattern Recognition*, pp. 8759-8768.
- Redmon, Diwala, Girshik, and Farhadi, 2016. [You Only Look Once: Unified, Real-Time Object Detection](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Redmon_You_Only_Look_CVPR_2016_paper.pdf). In *Proc. of the IEEE Conference on Computer Vision and Pattern Recognition*, pp. 779-788.

**Gray literature and white papers**
- The Assurance Case Working Group (ACWG), 2018. [Goal Structuring Notation Community Standard](https://scsc.uk/r141B:1?t=1), Version 2, SCSC-141B.
- Jocher *et al.*, 2021. YOLOv5n 'Nano' models, Roboflow Integration, TensorFlow Export, OpenCV DNN Support, [10.5281/zenodo.5563715](https://zenodo.org/record/5563715).
- Rajput, 2020. [YOLO V5 — Explained and Demystified](https://towardsai.net/p/computer-vision/yolo-v5%E2%80%8A-%E2%80%8Aexplained-and-demystified), Towards AI, (Retrieved 2021-12-01)
- Van Looveren, Vacanti, Klaise, Coca, and Cobb, 2019. [Alibi Detect: Algorithms for Outlier, Adversarial and Drift Detection](https://github.com/SeldonIO/alibi-detect), GitHub.

# 2 ML Component Description [D]
The SMIRK pedestrian recognition component consists of, among other things, two ML-based constituents: a pedestrian detector and an anomaly detector. Further details are available in the [Logical View](</docs/System Architecture Description.md#31-logical-view>) of the system architecture. In this section, we describe the pedestrian detector. The anomaly detection is described in Section 4.

The SMIRK pedestrian detector uses the third-party OSS framework YOLOv5 by Ultralytics implemented using [PyTorch](https://pytorch.org/). YOLO is an established real-time object detection algorithm that was originally released by Redmon *et al.* (2016). The first version of YOLO introduced a novel object detection process that uses a single deep neural network (DNN) to perform both prediction of bounding boxes around objects and classification at once. Compared to the alternatives, YOLO was heavily optimized for fast inference to support real-time applications. A fundamental concept of YOLO is that the algorithm considers each image only once, hence its name "You Only Look Once." YOLO is referred to as a single-stage object detector. While there have been several versions of YOLO (and the original authors maintained them until v3), the fundamental ideas of YOLO remains the same across versions - including YOLOv5 used in SMIRK.

YOLO segments input images into smaller images. Each input image is split into a square grid of individual cells. Each cell predicts bounding boxes capturing potential objects and provides confidence scores for each box. Furthermore, YOLO does a class prediction for objects in the bounding boxes. Note that for the SMIRK MVP, the only class we predict is pedestrian. Relying on the [Intersection over Union](https://www.pyimagesearch.com/2016/11/07/intersection-over-union-iou-for-object-detection/) method for evaluating bounding boxes, YOLO eliminates redundant bounding boxes. The final output from YOLO consists of unique bounding boxes with class predictions. Further details are available in the original paper by Redmon *et al.* (2016).

The pedestrian recognition component in SMIRK uses the YOLOv5 architecture without any modifications. This paragraph presents a high-level description of the model architecture and the key techincal details. We refer the interested reader to further details provided by Rajput (2020) and the OSS repository on GitHub. YOLOv5 provides several alternative DNN architectures. To enable real-time performance for SMIRK, we select **YOLOv5s** with 191 layers and about 7.5 million parameters. 

Figure 1 shows the speed/accuracy tradeoffs for different YOLOv5 architectures with YOLOv5s depicted in orange. The results are provided by [Ultralytics](https://github.com/ultralytics/yolov5#why-yolov5) including instructions for reproduction. On the y-axis, *COCO AP val* denotes the mAP@0.5:0.95 metric measured on the 5,000-image COCO val2017 dataset over various inference sizes from 256 to 1,536. On the x-axis, *GPU Speed* measures average inference time per image on the COCO val2017 dataset using an AWS p3.2xlarge V100 instance at batch-size 32. The curve EfficientDet illustrates results from Google AutoML at batch size 8.

![YOLOv5-tradeoffs](/docs/figures/YOLOv5-comparison.png) <a name="yolov5_comparison"></a>

*Figure 1: Speed/accuracy tradeoffs for different YOLOv5 architectures. (Image source: [Ultralytics](https://github.com/ultralytics/yolov5))*

As an single-stage object detector, YOLOv5s consists of three core parts: 1) the model backbone, 2) the model neck, and 3) the model head. The model backbone extracts important features from input images. The model neck generates so called "feature pyramids" using PANet (Liu *et al.*, 2018) that support generalization to different sizes and scales. The model head performs the detection task, i.e., it generates the final output vectors with bounding boxes and class probabilities.

In SMIRK, we use the default configurations proposed in YOLOv5s regarding activation, optimization, and cost functions. As activation functions, YOLOv5s uses **Leaky ReLU** in the hidden layers and the **sigmoid function** in the final layer. We use the default optimization function in YOLOv5s, i.e., **stochastic gradient descent**. The default cost function in YOLOv5s is **binary cross-entropy with logits loss** as provided in [PyTorch](https://pytorch.org/docs/master/generated/torch.nn.BCEWithLogitsLoss.html), which we also use.

# 3 Model Development Log [U] 
This section describes how the YOLOv5s model has been trained for the SMIRK MVP. We followed the general process presented by Ultralytics for [training on custom data](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data).

First, we manually prepared two SMIRK datasets to match the input format of YOLOv5. In this step, we prepared the development data [N] and the internal test data [O] according to Ultralytic's instructions. We created a dataset.yaml with the paths to the two data sets and specified that we train YOLOv5 for a single class, i.e., pedestrians. The data sets were already annotated using ESI Pro-SiVIC, thus we only needed to export the labels to the YOLO format with one txt-file per image. Finally, we organize the individual files (images and labels) according to the YOLOv5 instructions. More specifically, each label file contains the following information:
- One row per object
- Each row contains class, x_center, y_center, width, and height.
- Box coordinates are stored in normalized xywh format (from 0 - 1).
- Class numbers are zero-indexed, i.e., they start from 0.

Second, we trained the YOLOv5s model using the development data (as specified in dataset.yaml) from the pretrained weights in yolov5s.pt. The model was trained for 3 epochs with a batch-size of 16. The [Internal Test Results [X]](https://github.com/RI-SE/smirk/blob/main/docs/protocols/Internal%20Test%20Results%20[X]%202022-06-16.pdf) provides evidence that the ML model satisfies the requirements on the internal test data. 

The [final pedestrian detection model](https://github.com/RI-SE/smirk/releases/download/v0.99/pedestrian-detection-model.pt), i.e., the ML model [V], has a size of about 14 MB.

# 4 Outlier Detection for the Safety Cage Architecture <a name="outlier_detection_safety_cage_architecture"></a>
SMIRK relies on the open-source third-party library [Alibi Detect](https://github.com/SeldonIO/alibi-detect) from Seldon for outlier detection. The outlier detection is part of the safety cage architecture. Alibi Detect is a Python library that provides several algorithms for outlier, adversarial, and drift detection for various types of data (Klaise, 2020). For SMIRK, we trained Alibi Detect's autoencoder for outlier detection, with three convolutional and deconvolutional layers for the encoder and decoder respectively. The [final OOD detection model](https://github.com/RI-SE/smirk/releases/download/v0.99/outlier-detection-model.zip) is roughly 150 MB. 

Figure 2 shows an overview of the DNN architecture of an autoencoder. An encoder and a decoder are trained jointly in two steps to minimize a reconstruction error. First, the autoencoder receives input data *X* and encodes it into a latent space of fewer dimensions. Second, the decoder tries to reconstruct the original data and produces output *X'*. An and Cho (2015) proposed using the reconstruction error from a autoencoder to identify input that differs from the training data. Intuitively, if inlier data is processed by the autoencoder, the difference between *X* and *X'* will be smaller than for outlier data. By carefully selecting a threshold, this approach can be used for OOD detection.

![Autoencoder](/docs/figures/autoencoder.png) <a name="autoencoder"></a>

*Figure 2: Overview architecture of an autoencoder. Adapted from WikiUser:EugenioTL (CC BY-SA 4.0)

For SMIRK, we trained Alibi Detect's autoencoder for OOD detection on the training data subset of the development data. The encoder part is designed with three convolutional layers followed by a dense layer resulting in a bottleneck that compresses the input by 96.66%. The latent dimension is limited to 1,024 variables to limit requirements on processing VRAM of the GPU. The reconstruction error from the autoencoder is measured as the mean squared error between the input and the reconstructed instance. The mean squared error is used for OOD detection by computing the reconstruction error and considering an input image as an outlier if the error surpasses a threshold *theta*. The threshold used for OOD detection in SMIRK is 0.004, roughly corresponding to the threshold that rejects a number of samples that equals the amount of outliers in the validation set. As explained in the [Erroneous Behaviour Log](https://github.com/RI-SE/smirk/blob/main/docs/Deployment%20Specification.md#4-erroneous-behaviour-log-dd), the OOD detection is only active for objects at least 10 m away from ego car as the results for close-up images are highly unreliable. Furthermore, as the constrained SMIRK ODD ensures that only one single object appears in each scenario, the safety cage architecture applies the policy ``once an anomaly, always an anomaly'' - objects that get rejected once will remain anomalous no matter what subsequent frames might contain.

# 5 ML Model Learning Argument Pattern [W]
The figure below shows the ML model learning argument pattern using GSN. The pattern closely resembles the example provided in AMLAS, but adapts it to the specific SMIRK case.

![GSN-ML-Model_Learning_Argument_Pattern](/docs/figures/gsn-model_learning_argument_pattern.png) <a name="gsn-ml_model_learning_argument"></a>

*Figure 3: SMIRK ML Model Learning Argument Pattern.*

The top claim (G4.1) in this argument pattern is that the development of the learned model [V] is sufficient. The strategy is to argue over the internal testing of the model and that the ML development was appropriate (S4.1) in context of creating a valid model that meets practical constraints such as real-time performance and cost (C4.2). Sub-claim (G4.2) is that the ML model satisfies the ML safety requirements when using the internal test data [O]. We justify that the internal test results indicate that the ML model satisfies the ML safety requirements (J3.1) by presenting evidence from the internal test results [X].

Sub-claim G4.3 addresses the approach that was used when developing the model. The claim is supported by three claims regarding the type of model selected, the transfer learning process used, and the model parameters selected, respectively. First, G4.5 claims that the type of model is appropriate for the specified ML safety requirements and the other model constraints. Second, G4.6 claims that the process followed to allow transfer learning is appropriate. ML development processes, including transfer learning, are highly iterative thus rationales for development decisions must be recorded. Third, G4.7 claims that the parameters of the ML model are appropriately selected to tune performance toward the object detection task in the specified ODD. Rationales for any decisions in G4.4 and G4.5 are recorded in the model development log [U].

# 6 ML Learning Argument [Y]
SMIRK instantiates the ML Learning Argument through a subset of the artifacts listed in the [Safety Assurance Table](https://github.com/RI-SE/smirk/tree/main/docs#safety-assurance). This instantiation activity uses as input the [ML Learning Argument Pattern [W]](</docs/ML%20Component%20Specification.md#5-ml-model-learning-argument-pattern-w>), as well as the following artifacts from preceding AMLAS activities:
- [ML Safety Requirements](</docs/System Requirements Specification.md#33-machine-learning-safety-requirements-h->) [H]
- [Development Data](https://www.ai.se/en/data-factory/datasets/smirk-synthetic-pedestrians-dataset) [N]
- [Internal Test Data](https://www.ai.se/en/data-factory/datasets/smirk-synthetic-pedestrians-dataset) [O]
  
