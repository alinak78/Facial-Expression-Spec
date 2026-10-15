# Public dataset downloads

Recordings are stored locally under `data/raw/`, which is excluded from Git. This keeps large media files out of GitHub history. Only download instructions and manifests belong in the repository.

## Scope

- **RAVDESS:** all 24 speech-video actor archives and the speech-audio archive. Song recordings are excluded because this project concerns speech. Original source: https://zenodo.org/records/1188976. Dataset terms: CC BY-NC-SA 4.0; see https://affectivedatascience.com/datasets.
- **TORGO:** all four official archives, including dysarthric speakers and controls. Original source and academic nonprofit terms: https://www.cs.toronto.edu/~complingweb/data/TORGO/torgo.html. Cite the TORGO publications listed on that page when publishing work using the data.

`data/manifests/public-downloads.json` records the current download status. A file is listed as verified only after download and integrity checks. RAVDESS is checked against the publisher's MD5 checksum and ZIP CRCs. TORGO's compressed tar stream is read to completion; locally computed SHA-256 checksums establish a reproducibility fingerprint, not independent publisher authentication. Both datasets receive file sizes and media counts.

## Download or resume

From the project root, run:

```sh
python3 scripts/download_public_datasets.py
```

The script uses saved official download URLs from `data/manifests/download-sources.json`, resumes `.part` files with curl, and rechecks completed archives. Downloading all compressed archives requires about 23 GB. Full extraction needs additional space; archives remain compressed by default. Small inspection samples, when present, are stored separately under each dataset's `samples/` directory.

## Research fit

RAVDESS provides labelled emotion audio/video from actors, without a documented speech-disability cohort. TORGO provides dysarthric audio and articulatory data but excludes video and has no documented reference emotion labels. Neither replaces DEED or THE-POSSD for the combined disability/video/emotion research question.

DEED and THE-POSSD require owner approval and are not included in these public downloads.
