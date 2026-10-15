# Dataset shortlist

For the focused speech-disability/emotion decision and additional checks, see [Speech disability datasets for emotion detection](SPEECH_EMOTION_DATASETS.md). DEED and THE-POSSD are the two verified direct matches; the other entries below serve different populations or analysis goals.

Checked October 15, 2026. A public description or download link does not necessarily provide unrestricted access to participant recordings. No full disability dataset is locally available yet.

| Priority | Dataset | Population and modalities | Labels and fit | Access and local status |
|---|---|---|---|---|
| 1 | DEED | Dysarthria associated with CP/PD; audio and facial video; typical-speech comparison group | Seven elicited categories including neutral. Best direct match for emotion and speech disability. Four dysarthric speakers constrain evaluation. | Research access by email request; not downloaded. |
| 2 | THE-POSSD | Post-stroke motor dysarthria; acoustic, glottal, facial video | Happy, angry, sad, neutral elicitation; clinical severity. Relevant multimodal extension. | Corresponding-author request; not downloaded. |
| 3 | YouTube Facial Palsy (YFP) | Facial-palsy videos/frame sequences; speech-disability status not established | Clinician palsy regions, eye/mouth classes and intensity; no documented emotion ground truth. Useful for movement and failure analysis. | Documentation and sample collage cloned; full archive requires an institutional request/password. |
| 4 | MEEI Facial Palsy Standard Set | Facial palsy and controls; standardized photos/video | Clinical facial-function scales, not reference felt-emotion labels; speech-disability status not established. | Publication located; current authorized acquisition endpoint/terms still to verify. |
| 5 | MuDERI | Intellectual disability; audiovisual, RGB-D and physiological recordings | Affective annotations; speech/motor-disability inclusion not established. Secondary population. | Dataset landing page found; direct page retrieval failed. Access route needs verification. |
| 6 | TORGO | CP/ALS-related dysarthria and controls; audio and 3D articulatory recordings | Speech prompts/articulation; no documented emotion labels. Audio robustness/extraction only. | Academic nonprofit download offered; full release about 18 GB uncompressed. Not downloaded because it does not supply the requested video/emotion benchmark. |
| 7 | UASpeech | Dysarthria associated with CP; acoustic corpus | Isolated-word speech/ASR resource; emotion labels not established. Confirm supplied modalities with owner. | Academic/government researchers only; request required; no redistribution/commercial use. Not downloaded. |

## Source details and decisions

**DEED.** The [official project page](https://sites.google.com/sheffield.ac.uk/deed) confirms audio/video, seven elicited categories, four dysarthric speakers and 21 typical speakers. The [original paper](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0287971) specifies 320 dysarthric and 1,680 typical utterances, filename label encoding, and request-based access to confidential data. Request via `dysarthricdeed@gmail.com`; ask which modalities and annotations are in the current release and obtain the exact licence. Elicited expression labels are not direct evidence of internal emotional state.

**THE-POSSD.** The [primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12944553/) reports a video analysis subset of 35 patients and 25 controls, with four emotion conditions and clinical severity. It also mentions a larger collection elsewhere; verify release-specific counts. Recordings are available on request because of privacy/ethical restrictions. The study's characterization of DEED conflicts with DEED's own original description; use the original DEED sources to establish DEED's emotional content.

**YFP.** The [owner repository](https://github.com/AvLab-CV/YouTube-Facial-Palsy-Database) describes 32 videos but inconsistently says 21 and 22 people; verify IDs before any split. It provides an institutional request form and password process, and prohibits redistribution and profit-making use. The clone contains `README.md`, `RequestForms.txt`, and a sample collage; it does not contain the full video/frame dataset. Request administrator `avlabdba@gmail.com` and cc `jison@mail.ntust.edu.tw` using a university account. Public YouTube origin is not a speech-disability or emotion annotation.

**MEEI.** The [original paper](https://pubmed.ncbi.nlm.nih.gov/31021433/) describes 60 participants and facial-function grading. A [later primary study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12584918/) describes 50 participants with palsy and ten controls in that standard set and identifies the Sir Charles Bell Society as its host. Confirm current download access and use conditions before acquisition.

**MuDERI.** The [dataset owner's landing page](https://institutorobotica.org/muderi-dataset/) was indexed with a description of 12 participants and multimodal affective recordings. Direct page access failed, so download availability and licence remain unverified. Do not describe this cohort as dysarthric without participant documentation.

**TORGO.** The [official Toronto page](https://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html) offers acoustic/articulatory archives for academic nonprofit use. Crucially, all video data are excluded from the public release. `VIDEO` markers indicate a recording setup, not downloadable facial videos. The release does not establish reference emotion annotations.

**UASpeech.** The [current owner page](https://speechtechnology.web.illinois.edu/uaspeech/) describes 16 dysarthric speakers remaining in distribution, specifies access restrictions, and lists request requirements. Request through `uaspeech-requests@lists.illinois.edu`; provide affiliation, institutional email, intended use, delivery account and access period. Do not substitute a third-party mirror for the owner's current distribution.

## Local acquisition plan

Create `data/raw/deed/` first once access is granted. Keep the current dataset release's licence and participant metadata alongside the files, and record hashes, counts, available modalities, speaker IDs, and label provenance. Add other datasets according to the selected experiment. The existing repository demo media can verify installation, but provides no disability performance evidence.


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
