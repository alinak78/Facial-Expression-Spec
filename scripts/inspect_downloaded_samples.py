"""Extract one video and one dysarthric WAV from verified public archives."""
from pathlib import Path
import hashlib
import json
import tarfile
import wave
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'data/manifests/public-downloads.json').read_text())
    result = []
    for dataset in ['ravdess', 'torgo']:
        records = [f for f in manifest['files'] if f['dataset'] == dataset]
        if dataset == 'ravdess':
            records = sorted((f for f in records if f['name'].startswith('Video_Speech')), key=lambda f: f['name'])
        else:
            records = sorted((f for f in records if f['name'] in ['F.tar.bz2', 'M.tar.bz2']), key=lambda f: f['name'])
        if not records:
            print('No verified sample archive yet for ' + dataset)
            continue
        record = records[0]
        folder = ROOT / 'data/raw' / dataset / 'samples'
        folder.mkdir(parents=True, exist_ok=True)
        if dataset == 'ravdess':
            with zipfile.ZipFile(ROOT / record['path']) as z:
                name = sorted(n for n in z.namelist() if Path(n).name.startswith('01-01-') and n.lower().endswith('.mp4'))[0]
                content = z.read(name)
        else:
            with tarfile.open(ROOT / record['path'], 'r|bz2') as tar:
                member = next(m for m in tar if m.isfile() and '/wav_headMic/' in m.name and m.name.lower().endswith('.wav'))
                name = member.name
                content = tar.extractfile(member).read()
        path = folder / Path(name).name
        path.write_bytes(content)
        entry = {'dataset': dataset, 'archive': record['path'], 'archive_member': name,
                 'sample': str(path.relative_to(ROOT)), 'sha256': hashlib.sha256(content).hexdigest()}
        if dataset == 'torgo':
            with wave.open(str(path)) as wav:
                entry.update({'sample_rate': wav.getframerate(), 'channels': wav.getnchannels(),
                              'duration_seconds': wav.getnframes() / wav.getframerate()})
        result.append(entry)
        print('Extracted ' + str(path.relative_to(ROOT)))
    (ROOT / 'data/manifests/inspection-samples.json').write_text(json.dumps(result, indent=2) + '\n')


if __name__ == '__main__':
    main()
