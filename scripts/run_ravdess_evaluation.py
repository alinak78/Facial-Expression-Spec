"""Evaluate the existing expression runner on one audiovisual modality per RAVDESS trial."""
import argparse
from collections import Counter
import csv
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

from index_ravdess_archives import EMOTIONS

ROOT = Path(__file__).resolve().parents[1]
CLASS_MAP = {"Anger": "angry", "Contempt": "contempt", "Disgust": "disgust",
             "Fear": "fearful", "Happiness": "happy", "Neutral": "neutral",
             "Sadness": "sad", "Surprise": "surprised"}
SHARED = [label for label in EMOTIONS.values() if label != "calm"]


def summarize(rows):
    eligible = [r for r in rows if r["reference"] in SHARED]
    confusion = {label: dict(Counter(r["prediction"] for r in eligible if r["reference"] == label))
                 for label in SHARED}
    per_class = {}
    for label in SHARED:
        tp = sum(r["reference"] == label and r["prediction"] == label for r in eligible)
        support = sum(r["reference"] == label for r in eligible)
        predicted = sum(r["prediction"] == label for r in eligible)
        per_class[label] = {"support": support, "correct": tp,
                            "recall": tp / support if support else None,
                            "f1": 2 * tp / (support + predicted) if support + predicted else None}
    return {"clips": len(rows), "scored_clips": len(eligible),
            "unsupported_calm_clips": sum(r["reference"] == "calm" for r in rows),
            "failures": sum(r["prediction"] == "no_prediction" for r in rows),
            "correct": sum(r["prediction"] == r["reference"] for r in eligible),
            "accuracy": sum(r["prediction"] == r["reference"] for r in eligible) / len(eligible) if eligible else None,
            "macro_recall": sum(v["recall"] for v in per_class.values() if v["recall"] is not None) / sum(v["recall"] is not None for v in per_class.values()) if eligible else None,
            "macro_f1": sum(v["f1"] for v in per_class.values() if v["f1"] is not None) / sum(v["f1"] is not None for v in per_class.values()) if eligible else None,
            "per_class": per_class, "confusion_matrix": confusion,
            "sampled_frames": sum(r["sampled_frames"] for r in rows),
            "frames_with_faces": sum(r["frames_with_faces"] for r in rows)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actors", type=int, nargs="+", default=[1, 2])
    parser.add_argument("--frames", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.frames < 1 or len(set(args.actors)) != len(args.actors):
        parser.error("frames must be positive and actors must be unique")
    if args.output.exists():
        parser.error("output already exists; choose a new directory")
    import cv2
    args.output.mkdir(parents=True)
    predictions_dir = args.output / "frame_predictions"
    predictions_dir.mkdir()
    rows = []
    archive_manifest = json.loads((ROOT / "data/manifests/public-downloads.json").read_text())
    sources = []
    for actor in args.actors:
        archive_path = ROOT / f"data/raw/ravdess/archives/Video_Speech_Actor_{actor:02d}.zip"
        sources.extend(f for f in archive_manifest["files"] if f["path"] == str(archive_path.relative_to(ROOT)))
        with zipfile.ZipFile(archive_path) as archive:
            members = sorted(n for n in archive.namelist()
                             if Path(n).name.startswith("01-01-") and n.endswith(".mp4"))
            if len(members) != 60:
                raise ValueError(f"Expected 60 audiovisual speech clips for actor {actor}, got {len(members)}")
            for member in members:
                filename = Path(member).name
                reference = EMOTIONS[int(Path(member).stem.split("-")[2])]
                output = predictions_dir / (Path(filename).stem + ".json")
                row = {"actor": actor, "archive": str(archive_path.relative_to(ROOT)),
                       "member": member, "reference": reference, "prediction": "no_prediction",
                       "sampled_frames": 0, "frames_with_faces": 0}
                with tempfile.TemporaryDirectory(prefix="ravdess-", dir=ROOT / "data/raw/ravdess") as tmp:
                    video = Path(tmp) / filename
                    video.write_bytes(archive.read(member))
                    cap = cv2.VideoCapture(str(video))
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    cap.release()
                    stride = max(1, math.ceil(total_frames / args.frames))
                    process = subprocess.run([sys.executable, str(ROOT / "scripts/run_expression_baseline.py"),
                                              str(video), "--output", str(output), "--stride", str(stride),
                                              "--max-frames", str(args.frames)], capture_output=True, text=True, timeout=120)
                    if process.returncode:
                        row["error"] = process.stderr[-2000:]
                    else:
                        result = json.loads(output.read_text())
                        result["dataset_source"] = {"archive": row["archive"], "member": member,
                                                    "reference_condition": reference}
                        result["input"] = f"{row['archive']}::{member}"
                        output.write_text(json.dumps(result, indent=2) + "\n")
                        row.update(sampled_frames=result["sampled_frames"], frames_with_faces=result["frames_with_faces"],
                                   input_sha256=result["input_sha256"])
                        faces = [max(frame["faces"], key=lambda f: f["bbox_xywh"][2] * f["bbox_xywh"][3])
                                 for frame in result["records"] if frame["faces"]]
                        if faces:
                            means = {label: sum(f["softmax_scores"][label] for f in faces) / len(faces)
                                     for label in CLASS_MAP}
                            row["prediction"] = CLASS_MAP[max(means, key=means.get)]
                            row["mean_softmax_scores"] = means
                rows.append(row)
                with (args.output / "clips.jsonl").open("a") as stream:
                    stream.write(json.dumps(row) + "\n")
                print(f"{len(rows):03d}: {filename} reference={reference} prediction={row['prediction']}", flush=True)
    summary = {"dataset": "RAVDESS audiovisual speech", "actors": args.actors,
               "method": "Unmodified run_expression_baseline.py; at most 12 roughly uniform frames per clip; largest detected face per frame; mean of eight-class softmax scores; no training or tuning.",
               "label_policy": "Seven shared categories scored. Calm excluded as unsupported. Contempt predictions remain errors. No-prediction failures count as incorrect on shared-category clips.",
               "limitations": "Two actors only; acted expression labels, not measured internal emotion. No documented speech-disability cohort. No speaker adaptation or model calibration. Neutral lead-in/out frames included. Haar detection may fail on atypical facial movement.",
               "sources": sources, "overall": summarize(rows),
               "by_actor": {str(actor): summarize([r for r in rows if r["actor"] == actor]) for actor in args.actors}}
    (args.output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    fields = ["actor", "member", "reference", "prediction", "sampled_frames", "frames_with_faces"]
    with (args.output / "predictions.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps(summary["overall"], indent=2), flush=True)


if __name__ == "__main__":
    main()
