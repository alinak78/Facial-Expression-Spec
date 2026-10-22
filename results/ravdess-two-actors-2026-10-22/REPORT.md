# RAVDESS expression baseline — October 22, 2026

The existing EmotiEffLib ONNX expression model completed 120 audiovisual speech clips from actors 01 and 02. Clip accuracy on the seven supported reference categories was **63.5% (66/104)**. The 16 calm clips were processed but excluded from accuracy because this model has no calm class.

## Run and scoring

- Existing model: `enet_b0_8_best_vgaf`, CPU/ONNX; weights and the original per-video runner were unchanged.
- No training, adaptation, parameter search, or expression threshold tuning was performed.
- One audiovisual version of each trial was included. Video-only duplicates and song recordings were excluded.
- At most 12 roughly uniform frames per clip, including neutral lead-in/out. The largest detected face was selected per frame; eight-class softmax scores were averaged across frames.
- RAVDESS fearful maps to model Fear, happy to Happiness, angry to Anger, sad to Sadness, and surprised to Surprise. Neutral and disgust map directly. Contempt predictions remain errors. Calm is not silently remapped to neutral.
- A missing prediction would count as incorrect on a supported-label clip. There were no such failures.

## Results

- Face detection coverage: 1,412/1,412 sampled frames (100.0%).
- Clip accuracy: 63.5%; macro recall: 65.2%; macro F1: 0.599.
- An always-most-frequent-class baseline scores 16/104 (15.4%) on these supported-label clips.

| Actor | Comparable clips | Correct | Accuracy |
|---|---:|---:|---:|
| 1 | 52 | 34 | 65.4% |
| 2 | 52 | 32 | 61.5% |

Per-class recall is the proportion of clips in that reference condition predicted correctly.

| Reference condition | Clips | Correct | Recall | F1 |
|---|---:|---:|---:|---:|
| neutral | 8 | 7 | 87.5% | 0.519 |
| happy | 16 | 16 | 100.0% | 1.000 |
| sad | 16 | 5 | 31.2% | 0.417 |
| angry | 16 | 8 | 50.0% | 0.571 |
| fearful | 16 | 2 | 12.5% | 0.222 |
| disgust | 16 | 16 | 100.0% | 0.667 |
| surprised | 16 | 12 | 75.0% | 0.800 |

## Confusion matrix

| Reference / predicted | neutral | happy | sad | angry | fearful | disgust | surprised | contempt | no_prediction |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| neutral | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| happy | 0 | 16 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| sad | 2 | 0 | 5 | 4 | 0 | 5 | 0 | 0 | 0 |
| angry | 3 | 0 | 0 | 8 | 0 | 4 | 1 | 0 | 0 |
| fearful | 3 | 0 | 3 | 0 | 2 | 7 | 1 | 0 | 0 |
| disgust | 0 | 0 | 0 | 0 | 0 | 16 | 0 | 0 | 0 |
| surprised | 4 | 0 | 0 | 0 | 0 | 0 | 12 | 0 | 0 |

## Interpretation and limits

Happy and disgust had perfect recall in this small subset, but disgust was also over-predicted on other reference conditions. Fearful had 2/16 correct and sad had 5/16 correct. Actor 02 had no correctly classified sad clips. These errors deserve inspection before expanding the evaluation.

RAVDESS contains acted reference conditions and is not documented as a speech-disability cohort. This run verifies decoding, face detection, scoring and clip-level evaluation. It does not establish performance on dysarthric speech, motor disability, or internal emotional state. Two actors cannot establish generalization across the full dataset. Softmax scores are uncalibrated, and face detection coverage alone does not establish accurate localization or tracking.

The public TORGO release contains no facial video or reference emotion labels, so it is incompatible with this facial-expression evaluation. A direct disability/video/emotion experiment still requires an authorized suitable dataset such as DEED or THE-POSSD.

## Files and reproduction

- `predictions.csv`: one prediction per clip and its reference condition.
- `clips.jsonl`: source archive/member, input checksum, prediction and averaged scores.
- `frame_predictions/`: all bounding boxes, timestamps and eight-class frame scores.
- `summary.json`: aggregate and actor-level metrics, confusion matrices, source archives, model commit and weight checksum.

Run from the repository root with a new, empty output directory:

```sh
.venv/bin/python scripts/run_ravdess_evaluation.py --actors 1 2 --frames 12 --output results/ravdess-two-actors-new-run
```

Validation passed: 120 unique clips, 120 frame-output JSON files, consistent model commit/weight hash, and finite normalized frame and clip scores. No raw recordings were added to Git.
