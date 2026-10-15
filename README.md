# Facial expression and speech disability research

Work started October 15, 2026. The objective is to run existing models on speech-disability data, including participants with motor disabilities, and evaluate expression or emotion predictions against appropriate labels.

## Project files

- `docs/`: supplied literature survey with a dataset appendix, plus the expanded downloadable dataset shortlist and its Google Doc link. Previous surveys and presentation files remain in their original locations.
- `research/TASKS.md`: task outline, priorities, and Wednesday discussion agenda.
- `research/DATASETS.md`: dataset shortlist with sources, modalities, labels, and access status.
- `research/SPEECH_EMOTION_DATASETS.md`: focused review of datasets with speech-disability and emotion evidence, including access contacts and exclusions.
- `research/access-request-drafts.md`: editable access requests and Toby discussion points; nothing has been sent.
- `research/repositories.json`: cloned repository URLs and exact commits.
- `research/literature-survey-extracted.txt`: paragraph/table text extracted from the supplied survey for searching; not a layout-preserving conversion.
- `repos/`: four companion clones. This project folder is the user-provided Facial-Expression-Spec clone; its original README is preserved as `README.repository.md`.
- `scripts/run_expression_baseline.py`: local image/video inference using existing EmotiEffLib weights.
- `results/`: demo outputs and environment records. Demo samples are not disability benchmarks.

## Run the initial baseline

The project-local `.venv` uses Python 3.12. Dependencies were installed from the cloned EmotiEffLib project. The model loads already-cloned ONNX weights and runs on CPU.

```sh
.venv/bin/python scripts/run_expression_baseline.py repos/OpenFace/samples/default.wmv --output results/new-demo.json --max-frames 12 --stride 25
.venv/bin/python scripts/run_expression_baseline.py /absolute/path/to/authorized/video.mov --output results/new-video.json --max-frames 100 --stride 25
```

The runner samples frames by index, detects faces with OpenCV's Haar cascade, and writes bounding boxes, expression predictions, all eight softmax scores, input/model hashes, and the model repository commit. It records frames with no detected faces. The cascade is a setup baseline and may fail on atypical facial movement, pose, or lighting. Face indices are not tracked identities. Video decoding is bounded by the sample count; this is not yet a dataset-wide evaluation pipeline.

At the start of this work, the provided `alinak78/Facial-Expression-Spec` repository contained only a README on `main`. Its model/checkpoint needs to be supplied before that specific implementation can be run. The baseline is an additional existing model, not a reproduction of an unavailable lab model.

Public RAVDESS speech archives and the full TORGO release are managed under `data/raw/`; current completion and integrity status is recorded in `data/manifests/public-downloads.json`. See `data/README.md` for download scope and source terms. DEED and YFP require access requests; other options and their limitations are documented in the shortlist. Raw data should go in `data/raw/<dataset>/` after access is established. Raw data, environments, and nested clones are excluded by the project `.gitignore`.

To rebuild the baseline environment, first clone the model and demo repository:

```sh
git clone https://github.com/sb-ai-lab/EmotiEffLib.git repos/EmotiEffLib
git -C repos/EmotiEffLib checkout 520a051c64cd191521e5934655314e769a319684
git clone https://github.com/TadasBaltrusaitis/OpenFace.git repos/OpenFace
git -C repos/OpenFace checkout 3d4b5cf8d96138be42bed229447f36cbb09a5a29
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-baseline.txt
```

OpenCV is pinned to 4.12 because version 5 removed the cascade API used by this runner. Exact installed package versions are saved in `results/environment-freeze.txt`; its local installation paths reflect the original environment. All companion clone URLs and commits are in `research/repositories.json`.
