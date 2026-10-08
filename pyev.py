#!/usr/bin/env python3
"""PyEV command-line interface: calculate, export or start the local interface."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'dist'))
import pyev_engine
import pyev_reports


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    initial=commands.add_parser('init',help='Write an editable example design JSON file')
    initial.add_argument('path',nargs='?',default='PyEV_Design.json')
    run=commands.add_parser('run',help='Analyse a JSON design and export all tables and graphs')
    run.add_argument('path',nargs='?',help='PyEV JSON file; omit to run the default Kunray example')
    run.add_argument('--out',default='outputs/pyev',help='Output folder')
    serve=commands.add_parser('serve',help='Start the local Python application')
    serve.add_argument('--port',type=int,default=8765)
    serve.add_argument('--no-browser',action='store_true')
    args=parser.parse_args()
    if args.command=='init':
        target=Path(args.path)
        if target.exists():
            raise SystemExit(f'{target} already exists. Choose another filename to preserve it.')
        bootstrap=pyev_engine.bootstrap()
        target.write_text(json.dumps({'schema_version':1,'application':'PyEV','spec':bootstrap['default_spec'],'sweep':bootstrap['default_sweep']},indent=2),encoding='utf-8')
        print(f'Example saved to {target.resolve()}')
        return
    if args.command=='serve':
        import serve as local_server
        sys.argv=['serve.py','--port',str(args.port)]+(['--no-browser'] if args.no_browser else [])
        local_server.main()
        return
    payload=json.loads(Path(args.path).read_text(encoding='utf-8')) if args.path else {}
    if not isinstance(payload,dict):raise SystemExit('Design JSON must be an object.')
    allowed={'schema_version','application','spec','sweep'}
    if set(payload)-allowed:raise SystemExit('Expected a PyEV JSON object with spec and sweep fields.')
    result=pyev_engine.analyze(payload.get('spec'),payload.get('sweep'))
    out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
    (out/'PyEV_Results.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    (out/'PyEV_Design.json').write_text(json.dumps({'schema_version':1,'application':'PyEV','spec':result['spec'],'sweep':result['sweep']},indent=2),encoding='utf-8')
    (out/'PyEV_Engineering_Report.html').write_text(pyev_reports.report_html(result),encoding='utf-8')
    for table in result.get('tables',[]):
        name=''.join(c for c in table['id'] if c.isalnum() or c in '_-')
        (out/(name+'.csv')).write_text(pyev_reports.table_csv(table),encoding='utf-8-sig')
    for chart in result.get('charts',[]):
        name=''.join(c for c in chart['id'] if c.isalnum() or c in '_-')
        (out/(name+'.svg')).write_text(pyev_reports.chart_svg(chart),encoding='utf-8')
    print(f'PyEV calculation completed: {len(result.get("tables",[]))} tables and {len(result.get("charts",[]))} graphs.')
    print(f'Open {(out/"PyEV_Engineering_Report.html").resolve()}')

if __name__=='__main__':
    main()
