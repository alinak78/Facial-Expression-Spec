"""Run the cloned EmotiEffLib model locally on images or sampled video frames."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--stride", type=int, default=25)
    p.add_argument("--max-frames", type=int, default=20)
    args = p.parse_args()
    if args.stride < 1 or args.max_frames < 1:
        p.error("stride and max-frames must be positive")
    if not args.input.is_file():
        p.error("input file does not exist")
    if args.output.exists():
        p.error("output exists; choose a new output filename")

    import cv2
    import numpy as np
    import emotiefflib.facial_analysis as fa

    repo = ROOT / "repos/EmotiEffLib"
    model_name = "enet_b0_8_best_vgaf"
    model_path = repo / "models/affectnet_emotions/onnx" / (model_name + ".onnx")
    # Use already-cloned weights, avoiding upstream's home-directory cache/download.
    fa.get_model_path_onnx = lambda name: str(model_path)
    model = fa.EmotiEffLibRecognizer(engine="onnx", model_name=model_name)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if detector.empty():
        raise RuntimeError("Face detector failed to load")
    frames = []
    is_image = args.input.suffix.lower() in {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}
    cap = None
    if is_image:
        frame = cv2.imread(str(args.input))
        if frame is None:
            raise ValueError("Image could not be decoded")
        frames = [(0, None, frame)]
    else:
        cap = cv2.VideoCapture(str(args.input))
        if not cap.isOpened():
            raise ValueError("Video could not be opened")
        fps = cap.get(cv2.CAP_PROP_FPS)
        index = 0
        try:
            while len(frames) < args.max_frames:
                ok, frame = cap.read()
                if not ok:
                    break
                if index % args.stride == 0:
                    frames.append((index, index / fps if fps > 0 else None, frame))
                index += 1
        finally:
            cap.release()
    if not frames:
        raise ValueError("No decodable frames")
    records = []
    for index, timestamp, frame in frames:
        boxes = detector.detectMultiScale(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                                          scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
        faces = []
        for x, y, w, h in boxes:
            crop = cv2.cvtColor(frame[y:y+h, x:x+w], cv2.COLOR_BGR2RGB)
            labels, scores = model.predict_emotions(crop, logits=False)
            values = scores[0]
            if not np.all(np.isfinite(values)) or not np.isclose(values.sum(), 1, atol=1e-5):
                raise ValueError("Invalid normalized model scores")
            faces.append({"bbox_xywh": [int(x), int(y), int(w), int(h)],
                          "predicted_expression": labels[0],
                          "softmax_scores": {model.idx_to_emotion_class[i]: float(v)
                                             for i, v in enumerate(values)}})
        records.append({"frame_index": index, "timestamp_seconds": timestamp, "faces": faces})
    result = {"input": str(args.input.resolve()),
              "input_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
              "model": model_name,
              "model_sha256": hashlib.sha256(model_path.read_bytes()).hexdigest(),
              "model_repository_commit": subprocess.check_output(
                  ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip(),
              "python": sys.version, "detector": "OpenCV frontal-face Haar cascade",
              "sampled_frames": len(records),
              "frames_with_faces": sum(bool(r["faces"]) for r in records),
              "interpretation": "Expression predictions only. Softmax scores are uncalibrated. "
                                "No emotion ground truth or disability diagnosis is inferred.",
              "records": records}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Saved {len(records)} frames; {result['frames_with_faces']} with detected faces to {args.output}")


if __name__ == "__main__":
    main()
