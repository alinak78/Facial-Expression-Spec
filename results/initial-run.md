# Initial baseline run

Date: October 15, 2026

The pretrained EmotiEffLib `enet_b0_8_best_vgaf` ONNX model ran successfully on CPU using OpenFace's included `samples/default.wmv` demo. Twelve frames were sampled at a stride of 25 frames. Faces were detected in all twelve sampled frames, and all returned score vectors were finite and summed to one within tolerance. Per-frame outputs, bounding boxes, hashes, and model commit are saved in `demo-video-baseline.json`.

This demo has no supplied emotion ground truth or disability cohort designation. No accuracy, F1, or disability generalization conclusion is reported. It verifies model loading, video decoding, face cropping, inference, and output serialization.

The first run exposed an OpenCV 5 API incompatibility. Pinning OpenCV to 4.12.0.88 restored the Haar cascade API; the rerun passed. ONNX Runtime emitted a telemetry-ID persistence warning, but inference completed.

OpenFace was cloned but its native feature extractor was not compiled. Emotrics was cloned but its desktop application was not installed or run. The supplied Facial-Expression-Spec repository was cloned and inspected; its sole remote branch contains only a README.

The model is an existing general expression baseline. The full disability datasets remain unavailable locally pending access or further acquisition checks. See `research/DATASETS.md` and `research/access-request-drafts.md`.
