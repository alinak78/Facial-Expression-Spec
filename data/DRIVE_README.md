# Dataset archives on Google Drive

Folder: https://drive.google.com/drive/folders/1th61GgZEXmLy2_1SOmKuMcv9VzsptR4r

## Scope and storage

The upload contains the complete TORGO release (F, FC, M, and MC archives), the complete RAVDESS speech-audio archive, and RAVDESS speech-video actors 01 and 02. This is approximately 10.9 GB of archive data. RAVDESS video actors 03–24 remain local because the Drive account initially had about 12.3 GB available. This is not the full RAVDESS speech-video collection.

TORGO includes dysarthric speakers and controls, but no released video or reference emotion labels. RAVDESS has emotion labels and audiovisual speech from actors, without a documented speech-disability cohort. See Dataset_sources_and_terms.md for source links and usage terms.

The connector accepts files smaller than 100 MB. Whole-archive browser uploads failed, so each original archive is stored in 80 MiB parts under its dataset's `Archive parts` folder. Parts are binary slices, not individually extractable archives. Preserve every original filename, including `.part001`, `.part002`, and so on. Two small inspection samples are also provided separately.

## Download and reconstruct

1. Download the archive parts from both dataset folders and extract any ZIP wrappers created by Google Drive. Keep the `.partNNN` filenames unchanged.
2. Download `drive-uploads.json` and `reassemble_drive_archives.py` from the main Drive folder.
3. With Python 3, run:

```sh
python3 reassemble_drive_archives.py /path/to/downloaded-parts --manifest /path/to/drive-uploads.json --output /path/to/reassembled
```

The script searches subfolders, joins each archive's parts in manifest order, and verifies the reconstructed archive against the original byte count and SHA-256 checksum. It refuses to overwrite existing archive outputs. Allow approximately 11 GB of extra local space for reconstruction, plus any space needed for extraction.

`Local_archive_checksums.json` describes all 29 locally downloaded archives, including those not uploaded to Drive. `drive-uploads.json` records the narrower Drive scope and upload status.
