"""Index RAVDESS labels directly from verified archives, without full extraction."""
from collections import Counter
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
EMOTIONS = {1: 'neutral', 2: 'calm', 3: 'happy', 4: 'sad', 5: 'angry',
            6: 'fearful', 7: 'disgust', 8: 'surprised'}


def main():
    manifest = json.loads((ROOT / 'data/manifests/public-downloads.json').read_text())
    if manifest['status'] != 'complete':
        raise RuntimeError('Wait for the public archive download to complete')
    clips = []
    for record in manifest['files']:
        if record['dataset'] != 'ravdess':
            continue
        with zipfile.ZipFile(ROOT / record['path']) as archive:
            for member in archive.namelist():
                path = Path(member)
                if path.suffix.lower() not in {'.mp4', '.wav'}:
                    continue
                modality, channel, emotion, intensity, statement, repetition, actor = map(int, path.stem.split('-'))
                clips.append({'archive': record['path'], 'member': member, 'actor': actor,
                              'modality': {1: 'audiovisual', 2: 'video_only', 3: 'audio_only'}[modality],
                              'emotion': EMOTIONS[emotion], 'intensity_code': intensity,
                              'statement': statement, 'repetition': repetition})
    counts = Counter(c['modality'] for c in clips)
    assert dict(counts) == {'audio_only': 1440, 'audiovisual': 1440, 'video_only': 1440}, dict(counts)
    out = {'status': 'complete', 'counts': dict(counts), 'actors': sorted({c['actor'] for c in clips}),
           'warning': 'Modalities contain repeated versions of the same trial; do not pool as independent samples.',
           'clips': sorted(clips, key=lambda c: (c['actor'], c['member']))}
    (ROOT / 'data/manifests/ravdess-clips.json').write_text(json.dumps(out, indent=2) + '\n')
    print('Indexed', len(clips), 'media files from', len(out['actors']), 'actors:', dict(counts))


if __name__ == '__main__':
    main()
