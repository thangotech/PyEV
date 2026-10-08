#!/usr/bin/env python3
"""Package portable open source, excluding hosting identity, caches and output."""
from pathlib import Path
import zipfile
ROOT=Path(__file__).resolve().parent
TARGET=ROOT/'dist'/'pyev-source.zip'
EXCLUDED_DIRS={'.git','.openai','__pycache__','.pytest_cache','.venv','node_modules','outputs'}
EXCLUDED_NAMES={'pyev-source.zip','CONTRACT.md','.DS_Store'}

def main():
    with zipfile.ZipFile(TARGET,'w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(ROOT.rglob('*')):
            relative=path.relative_to(ROOT)
            if path.is_file() and not any(part in EXCLUDED_DIRS for part in relative.parts) and path.name not in EXCLUDED_NAMES and path.suffix not in {'.pyc','.pyo'}:
                archive.write(path,Path('PyEV')/relative)
    print(f'{TARGET} ({TARGET.stat().st_size} bytes)')
if __name__=='__main__':main()
