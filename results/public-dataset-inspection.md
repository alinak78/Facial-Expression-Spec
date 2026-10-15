# Public dataset inspection

The public download manifest tracks the full archive download separately from these small inspection samples.

- RAVDESS: extracted one audiovisual speech clip from Actor 05. The existing EmotiEffLib ONNX model processed 11 sampled frames, with faces detected in all 11 and valid normalized scores. This is a decoding and inference check, not a multi-actor evaluation.
- TORGO: extracted F01/Session1/wav_headMic/0064.wav from the clinical F archive. Python wave inspection confirms mono 16 kHz audio with duration 1.53425 seconds. TORGO supplies no reference emotion label for this clip.

Sample source members and SHA-256 hashes are in `data/manifests/inspection-samples.json`; video-model outputs are in `results/ravdess-public-sample-baseline.json`.
