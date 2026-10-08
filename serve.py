#!/usr/bin/env python3
"""Open PyEV using native Python and the same web interface, without packages."""
from __future__ import annotations
import argparse
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys
import threading
import webbrowser

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'dist'))
import pyev_engine
import pyev_reports

MAX_REQUEST_BYTES = 32 * 1024 * 1024


def ensure_source_download():
    """Restore the source download excluded from its own portable archive."""
    target = ROOT / 'dist' / 'pyev-source.zip'
    if target.is_file():
        return
    try:
        import build_source
        build_source.main()
    except OSError as exc:
        try:
            if target.is_file():
                target.unlink()
        except OSError:
            pass
        print(
            f'PyEV could not create the Python source ZIP: {exc}. '
            f'Calculations will still run. The complete source remains in {ROOT}. '
            'Copy the project to a writable folder and restart to enable the download.',
            file=sys.stderr,
        )


class PyEVHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Cache-Control', 'no-cache')
        super().end_headers()

    def send_json(self, status, data):
        encoded = json.dumps(data, allow_nan=False).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == '/api/health':
            return self.send_json(200, {'service': 'pyev-native', 'version': pyev_engine.bootstrap()['version']})
        return super().do_GET()

    def do_POST(self):
        if self.path not in ('/api/bootstrap', '/api/analyze', '/api/docx'):
            return self.send_json(404, {'error': 'Unknown PyEV operation.'})
        origin = self.headers.get('Origin')
        host = self.headers.get('Host', '')
        if origin and origin != f'http://{host}':
            return self.send_json(403, {'error': 'Requests must come from the local PyEV interface.'})
        try:
            length = int(self.headers.get('Content-Length', '0'))
            if not 0 <= length <= MAX_REQUEST_BYTES:
                raise ValueError('Request exceeds the 32 MiB limit.')
            payload = json.loads(self.rfile.read(length) or b'{}')
            if not isinstance(payload, dict):
                raise ValueError('The operation requires a JSON object.')
            action = self.path.rsplit('/', 1)[1]
            if action == 'bootstrap':
                result = pyev_engine.bootstrap()
            elif action == 'analyze':
                result = pyev_engine.analyze(**payload)
            else:
                result = pyev_reports.docx_download(**payload)
            self.send_json(200, {'result': result})
        except (ValueError, TypeError, KeyError) as exc:
            self.send_json(400, {'error': str(exc)})
        except Exception as exc:
            self.send_json(500, {'error': 'Calculation failed: ' + str(exc)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    ensure_source_download()
    handler = partial(PyEVHandler, directory=str(ROOT / 'dist'))
    try:
        server = ThreadingHTTPServer(('127.0.0.1', args.port), handler)
    except OSError as exc:
        raise SystemExit(f'Could not start PyEV: {exc}. Try --port 8766.') from exc
    url = f'http://127.0.0.1:{server.server_port}/'
    print(f'PyEV is running at {url}\nKeep this window open. Press Ctrl+C to stop.')
    if not args.no_browser:
        threading.Timer(0.3, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
