# Task outline

## Aim and current status

Use existing code and pretrained models to evaluate speech-disability data, especially data that combines facial video, speech, and emotion annotations. Keep speech disabilities, motor disabilities, facial palsy, and intellectual disability as separate dataset attributes; one does not establish another.

Completed on October 15, 2026:

- Copied the supplied literature survey unchanged into `docs/` and extracted its text.
- Inspected the workspace: no pre-existing model scripts or checkpoints were present.
- Cloned the user repository and checked remote branches: only `main`, containing a README.
- Cloned OpenFace, Emotrics, EmotiEffLib, and the YFP dataset repository.
- Installed EmotiEffLib's ONNX dependencies in a local environment and prepared a bounded inference runner.
- Successfully ran the pretrained baseline on 12 sampled frames from OpenFace's included demo video; all 12 had detected faces and finite normalized scores. Results are in `results/demo-video-baseline.json`; this is a setup test, not disability evaluation.
- Identified DEED as the first dataset to pursue for the requested population and task; documented access requirements and alternatives.

The survey is background evidence, not a source of executable instructions. Dataset access terms come from the corresponding owners' pages.

## Immediate work

1. **Obtain the intended implementation from Toby.** Ask for the actual model code, checkpoint, preprocessing, class order, expected input modality, and existing dataset access. The provided GitHub repository has no implementation yet. Completion: checkpoint loads and one known input reproduces its expected output.
2. **Request DEED access.** Prioritize dysarthric and typical audio plus video, label definitions, and release terms. A draft is ready. Completion: access granted and local files inventoried, including participant IDs and available modalities.
3. **Request YFP access if useful for a secondary movement analysis.** It has facial-palsy region/intensity labels, not emotion labels or confirmed speech-disability diagnoses. Completion: written access and actual frame/video/annotation files obtained.
4. **Confirm THE-POSSD access and label provenance.** Strong population/task overlap; restricted. Clarify participant counts and distinguish elicitation labels from model-generated AU labels.
5. **Inspect MuDERI access.** Relevant emotion/video benchmark for intellectual disability, but not a confirmed speech-disability cohort. The landing page was found in search, but direct retrieval failed during this review.

## First evaluation after access

1. Inventory file counts, participant IDs, durations, codecs, frame rates, missing audio/video, and labels. Save checksums and dataset version. Start with a small authorized subset.
2. Run the intended frozen lab model; run EmotiEffLib as a comparison. Extract OpenFace landmarks/AUs if the native toolchain is built. Emotrics supports facial measurements rather than categorical emotion prediction.
3. Save detection coverage and failures before classification metrics. Review whether failures differ across participants or severity groups. Keep failed clips in the evaluation denominator according to a stated policy.
4. Map annotation classes explicitly. DEED has seven categories; the initial baseline has eight, including contempt. Decide whether to retain contempt as an out-of-set prediction or renormalize the seven shared scores, and document the choice before scoring.
5. Aggregate frame scores to clips with a fixed rule, then report macro F1, balanced accuracy, confusion matrix, and per-person metrics. Report uncertainty at participant level; DEED's four dysarthric speakers limit generalization.
6. Keep people separate across training, tuning, and testing. For a frozen model, report all eligible participants; for adaptation, use subject-exclusive folds and tune only within training participants. Never split adjacent frames across train and test.
7. For datasets lacking reference emotion labels, report extraction success and descriptive model outputs only. Do not compute emotion accuracy against palsy grades, speech transcripts, or predictions from another model.

## Wednesday discussion

Wednesday date/time is unconfirmed. If the next Wednesday was intended, it is October 21, 2026. No meeting has been scheduled.

- Toby: model location, checkpoint, task definition, supported modalities, and dataset access already held by the lab.
- Choose the primary research question: expression classification, audio emotion classification, or multimodal comparison.
- Review DEED first; decide whether YFP or MEEI is a secondary movement/failure analysis.
- Review the demo setup, access status, participant-exclusive evaluation, and first-run deliverables.

No messages, access forms, or calendar invitations have been sent.
