"""Reassemble downloaded Drive archive parts and verify original SHA-256 hashes."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("parts_dir", type=Path, help="Folder containing downloaded .partNNN files (searched recursively)")
    parser.add_argument("--manifest", type=Path, default=Path(__file__).resolve().parents[1] / "data/manifests/drive-uploads.json")
    parser.add_argument("--output", type=Path, default=Path("reassembled"))
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text())
    for archive in manifest["archives"]:
        sources = []
        for name in archive["parts"]:
            matches = list(args.parts_dir.rglob(name))
            if len(matches) != 1:
                raise SystemExit(f"Expected exactly one {name}; found {len(matches)}. Download every part with its original filename.")
            sources.append(matches[0])
        destination = args.output / archive["dataset"] / archive["name"]
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            raise SystemExit(f"Output already exists: {destination}. Choose another output directory.")
        temporary = destination.with_name(destination.name + ".reassembling")
        digest = hashlib.sha256()
        size = 0
        with temporary.open("xb") as output:
            for source in sources:
                with source.open("rb") as stream:
                    while chunk := stream.read(1024 * 1024):
                        output.write(chunk)
                        digest.update(chunk)
                        size += len(chunk)
        if size != archive["bytes"] or digest.hexdigest() != archive["sha256"]:
            temporary.unlink()
            raise SystemExit(f"Checksum or size mismatch: {archive['name']}")
        temporary.rename(destination)
        print(f"Verified: {destination}")


if __name__ == "__main__":
    main()
