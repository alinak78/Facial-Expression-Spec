"""Download the official speech archives listed in the saved source manifest."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import shutil
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / 'data/manifests/download-sources.json'
MANIFEST = ROOT / 'data/manifests/public-downloads.json'


def download(item):
    folder = ROOT / 'data/raw' / item['dataset'] / 'archives'
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / item['name']
    if not path.exists():
        partial = path.with_name(path.name + '.part')
        print('Downloading ' + item['dataset'] + '/' + item['name'], flush=True)
        subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
                        '--retry', '5', '--retry-delay', '3', '--retry-all-errors',
                        '--connect-timeout', '30', '--speed-limit', '1024', '--speed-time', '120',
                        '--continue-at', '-', '--output', str(partial), item['url']], check=True)
        partial.rename(path)
    sha = hashlib.sha256()
    md5 = hashlib.md5()
    with path.open('rb') as f:
        while block := f.read(8 * 1024 * 1024):
            sha.update(block)
            md5.update(block)
    if item.get('size') and path.stat().st_size != item['size']:
        raise ValueError('Size mismatch: ' + str(path))
    if item.get('checksum') and item['checksum'] != 'md5:' + md5.hexdigest():
        raise ValueError('Publisher checksum mismatch: ' + str(path))
    media = 0
    members = 0
    expanded_bytes = 0
    if path.suffix == '.zip':
        with zipfile.ZipFile(path) as z:
            bad = z.testzip()
            if bad:
                raise ValueError('ZIP CRC failure: ' + bad)
            for entry in z.infolist():
                members += 1
                expanded_bytes += entry.file_size
                media += entry.filename.lower().endswith(('.mp4', '.wav'))
    else:
        with tarfile.open(path, 'r|bz2') as tar:
            for entry in tar:
                members += 1
                expanded_bytes += entry.size
                media += entry.isfile() and entry.name.lower().endswith('.wav')
    record = {**item, 'path': str(path.relative_to(ROOT)),
              'bytes': path.stat().st_size, 'sha256': sha.hexdigest(),
              'md5': md5.hexdigest(), 'archive_integrity': 'passed',
              'members': members, 'media_files': media,
              'uncompressed_bytes': expanded_bytes,
              'verified_at': datetime.now(timezone.utc).isoformat()}
    print(f"Verified {item['name']}: {path.stat().st_size / 1e6:.1f} MB, {media} media files", flush=True)
    return record


def main():
    if shutil.disk_usage(ROOT).free < 26 * 1024 ** 3:
        raise RuntimeError('Need at least 26 GiB free for all compressed archives')
    src = json.loads(SOURCES.read_text())
    items = [{'dataset': 'torgo', 'name': u.rsplit('/', 1)[-1], 'url': u} for u in src['torgo']]
    items += [{'dataset': 'ravdess', **f} for f in sorted(src['ravdess'], key=lambda f: f['name'])]
    manifest = {'scope': 'RAVDESS speech audio/video (song excluded); complete TORGO release',
                'status': 'in_progress', 'files': [], 'errors': []}
    def save():
        temporary = MANIFEST.with_suffix('.tmp')
        temporary.write_text(json.dumps(manifest, indent=2) + '\n')
        temporary.replace(MANIFEST)
    save()
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {pool.submit(download, item): item for item in items}
        for future in as_completed(futures):
            item = futures[future]
            try:
                manifest['files'].append(future.result())
            except Exception as e:
                manifest['errors'].append({'name': item['name'], 'error': str(e)})
                print('FAILED ' + item['name'] + ': ' + str(e), flush=True)
            save()
    manifest['status'] = 'complete' if not manifest['errors'] else 'incomplete'
    save()
    print(f"{manifest['status']}: {len(manifest['files'])}/{len(items)} archives verified", flush=True)
    if manifest['errors']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
