# Speech disability datasets for emotion detection

Verified October 15, 2026. Prioritize DEED for an initial audio/video experiment and THE-POSSD for a larger post-stroke comparison. Both document dysarthria and emotion categories. Neither offers anonymous access to the clinical recordings. No recordings were downloaded or access requests sent in this review.

## Two direct matches

| Dataset | Participants and modalities | Emotion categories | Acquisition | Decision |
|---|---|---|---|---|
| DEED | British English; four dysarthric speakers, one with cerebral palsy and three with Parkinson's disease; 21 typical speakers. Audio and video, with one typical speaker audio-only. | Happiness, sadness, anger, surprise, fear, disgust, neutral; elicited expressions. | Request research access through dysarthricdeed@gmail.com. | First choice for speech and facial-expression analysis; very small clinical cohort. |
| THE-POSSD | Chinese post-stroke motor dysarthria; acoustic, glottal and facial video. The 2026 video study uses 35 patients and 25 controls. | Happy, sad, angry, neutral. | Corresponding-author request to duanshufei@tyut.edu.cn; privacy restrictions. | Strong second choice, especially for motor impairment and facial movement. |

### DEED evidence and limitations

The [official project page](https://sites.google.com/sheffield.ac.uk/deed/home) states the population, categories and request route. The [original paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0287971) describes 320 dysarthric and 1,680 typical utterances and filename-encoded labels. Research access is subject to eligibility and licence conditions; free access does not mean unrestricted redistribution. The paper's reported emotion validation uses audio, so those results should not be presented as a validated facial-video benchmark.

For an audiovisual comparison, verify the missing typical participant and use the same eligible clips in both modalities. Four dysarthric speakers support an exploratory evaluation, not a broad disability-generalization claim.

### THE-POSSD evidence and limitations

The [2026 primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12944553/) confirms the video subset, categories, access restrictions and contact. The [original database paper](https://arxiv.org/abs/2312.08998) reports 39 patients and 29 controls; these counts describe different study scopes and must not be merged. Confirm the release's participant inventory and which emotion annotations are supplied. The later study's AU annotations use a pretrained model; they are not independent human emotion ground truth.

## Adjacent leads to keep separate

**emoHD:** [Primary study](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2025.1633492/full). Emotional speech from 102 Huntington's gene carriers and 35 controls, annotated for primary emotions, affective phenomena and activation. Data require a research partnership and transfer arrangements. The cohort includes different disease stages; documented dysarthria must be checked per participant before calling it a speech-disability benchmark. Useful future audio-only lead, not a confirmed replacement for DEED.

**Intelligent-Throat:** [Primary study](https://www.nature.com/articles/s41467-025-68228-9) includes five stroke patients with dysarthria and neutral, relieved and frustrated categories. Emotion classification uses carotid pulse signals, while silent speech uses throat vibrations. This is a sensor-based emotion resource, not a facial-video or ordinary acoustic-speech dataset. Although the paper links a [public Zenodo release](https://zenodo.org/records/17956161), its [archive preview](https://zenodo.org/records/17956161/preview/tcy21414/Intelligent-Throat-v1.0.0.zip?include_deleted=0) shows code and demonstration files. A complete patient emotion-data release was not verified; do not advertise it as ready to run.

## Exclusions from the emotion benchmark

- [TORGO](https://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html): genuine CP/ALS-related dysarthric speech, but no documented reference emotion labels and all video excluded from the public release.
- [UASpeech](https://speechtechnology.web.illinois.edu/uaspeech/): dysarthric speech corpus; owner documentation does not establish emotion labels.
- [YFP](https://github.com/AvLab-CV/YouTube-Facial-Palsy-Database): palsy-region/intensity annotations; neither emotion labels nor confirmed speech-disability status.
- MuDERI: relevant to intellectual disability and affect, but intellectual disability alone does not establish a speech disability.

## Acquisition checklist for the two direct matches

Ask for audio, video, emotion labels, participant IDs, relevant speech/motor severity metadata, exact current release and licence. Establish whether labels denote elicitation conditions, observer ratings or self-report. Confirm video synchronisation and missing modalities before running the frozen model. Evaluate by participant and clip, keep detection failures visible, and keep participants separate when adapting or tuning models.

Recommendation: pursue DEED access first, THE-POSSD second. No directly downloadable, fully verified audio/video emotion benchmark for dysarthric speakers was confirmed in this search.


## Downloadable datasets and existing code

Two downloadable resources can support different parts of the project: RAVDESS for labelled audio/video emotion evaluation, and TORGO for dysarthric audio processing. They do not replace DEED or THE-POSSD as datasets combining speech disability, video and emotion annotations. The complete public RAVDESS speech and TORGO archives have now been downloaded locally and verified; see `data/manifests/public-downloads.json` and `results/public-dataset-inspection.md`. Raw recordings are excluded from Git.

### RAVDESS for immediate audio and video emotion testing

RAVDESS contains 24 professional actors and 7,356 recordings across speech and song, with audio-only, video-only and audiovisual versions. Speech categories are neutral, calm, happy, sad, angry, fearful, disgust and surprised. It is suitable for validating face detection, clip aggregation, label parsing and audio/video evaluation before clinical data access is granted. Participants are not documented as a speech-disability cohort, so results cannot establish disability-specific performance. [Dataset description and licence](https://affectivedatascience.com/datasets) [Original study](https://pmc.ncbi.nlm.nih.gov/articles/PMC5955500/)

Download: The original Zenodo record offers separate speech-video archives per actor and a speech-audio archive. Start with Video_Speech_Actor_01.zip (approximately 553 MB) to test the video pipeline, then extend to more actors for evaluation. Speech-video archives contain audiovisual and video-only versions of the same trials; select a single modality to avoid counting duplicates as independent samples. RAVDESS is released under CC BY-NC-SA 4.0 for noncommercial use with attribution and share-alike conditions. [Official RAVDESS downloads](https://zenodo.org/records/1188976)

Model compatibility: The current eight-class EmotiEffLib baseline includes contempt but no calm class. Define a mapping before scoring: evaluate the seven shared categories with the treatment of contempt predictions stated explicitly, and report calm as an unsupported target rather than silently relabelling it as neutral. Keep actors separate when tuning or adapting the model.

### TORGO for downloadable speech disability audio

TORGO provides speech and 3D articulatory recordings from eight dysarthric speakers with cerebral palsy or ALS and seven controls. The official Toronto page links four archives: F.tar.bz2, M.tar.bz2, FC.tar.bz2 and MC.tar.bz2. The full release is approximately 18 GB uncompressed and is free for academic nonprofit use with required citation. Audio is 16 kHz mono WAV. Begin with one clinical archive for an audio-only inventory or robustness experiment. [Official TORGO download page and terms](https://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html)

Project limitation: TORGO’s public release excludes all video and does not document reference emotion labels. It cannot be input to the facial-expression model or used to calculate emotion accuracy. An audio emotion model may produce exploratory outputs, but those predictions are not ground truth.

### Existing code repositories

EmotiEffLib: Existing pretrained expression models with ONNX and PyTorch implementations for face crops and video workflows. Code is Apache-2.0. Already cloned at repos/EmotiEffLib; the ONNX baseline has passed the project’s demo-video test. Use this for RAVDESS facial-video predictions and, once access is granted, DEED video. The project wrapper is scripts/run_expression_baseline.py. [EmotiEffLib repository](https://github.com/sb-ai-lab/EmotiEffLib)

OpenFace: Facial landmarks, head pose, eye gaze and action-unit extraction. Already cloned at repos/OpenFace; its native executable has not been compiled or run in this project. The cloned licence specifies academic/nonprofit noncommercial research use. Useful for measuring facial movement and detection failures alongside expression predictions, rather than treating action units as reference emotion labels. [OpenFace repository](https://github.com/TadasBaltrusaitis/OpenFace)

SpeechBrain: Existing speech-processing toolkit with a released wav2vec2 emotion-recognition checkpoint trained on IEMOCAP. The model expects 16 kHz single-channel speech and exposes file-level inference. This is a candidate audio comparison baseline for authorized DEED recordings or exploratory TORGO processing. It is not installed or cloned locally, and its performance on dysarthric speech is unverified. The linked checkpoint is labelled Apache-2.0; its output classes must be checked against the chosen dataset before evaluation. [SpeechBrain code](https://github.com/speechbrain/speechbrain) [Pretrained emotion model and inference example](https://huggingface.co/speechbrain/emotion-recognition-wav2vec2-IEMOCAP)

Recommended next experiment: Use one RAVDESS speech-video actor archive to verify decoding and prediction output. For evaluation, expand across actors, use a documented class mapping and report failures. Pursue DEED or THE-POSSD access for the primary speech-disability emotion question; use TORGO only for the separately defined audio robustness task.
