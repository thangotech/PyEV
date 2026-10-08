# PyEV

<img src="dist/assets/thangotech-engineering-logo.jpeg" alt="Thangotech Engineering" width="360">

**Electric Vehicle Engineering**  
Prof Bonginkosi Thango · Thangotech Engineering

PyEV is open-source Python software for estimating electric-vehicle operating performance from editable motor, controller, battery, drivetrain, vehicle and road specifications. The initial example is the Kunray 72 V, 3000 W kart considered in the accompanying engineering study. Users can replace those values and compare their own designs.

[Open PyEV](https://pyev-thangotech.bonginkosithango.chatgpt.site)

[Download the complete Python source ZIP](https://pyev-thangotech.bonginkosithango.chatgpt.site/pyev-source.zip)

## Where to find the code

Select **Python code** in the application header or **Download Python code** in the sidebar. These source-download links are available from every page, including on mobile. The ZIP contains the computational engine, web interface, local Python launcher, examples, tests, documentation and GitHub Pages deployment workflow.

The main calculation code is `dist/pyev_engine.py`. Run the extracted project locally with `python serve.py`, or use `pyev.py` for command-line calculations. The supplied Thangotech Engineering logo is included unchanged in `dist/assets/thangotech-engineering-logo.jpeg`.

## Run it

### Public web application

Open the link, wait for the Python engine to load, edit **Specifications**, and select **Run analysis**. The public application runs the actual Python computational module in a browser worker using Pyodide. The first visit downloads that runtime. No Python installation, account or calculation server is needed. The application has no analytics or application-level upload of entered specifications. The host and runtime CDN receive ordinary asset requests.

Save a design as JSON to retain it. Imported JSON files and motor CSV curves are processed locally. The application accepts structured PyEV JSON and `rpm,torque_nm` CSV, not automatic extraction from photographs or PDF datasheets. Enter values from such datasheets in the specification editor.

### Local Python application

Install Python 3.10 or later, extract the complete source folder, and run:

```bash
python serve.py
```

On systems where Python is called `python3`, use `python3 serve.py`. On Windows, `START_PYEV_WINDOWS.bat` opens the application; macOS users can run `START_PYEV_MAC.command` or `python3 serve.py`. The launcher opens a browser at `http://127.0.0.1:8765/`. Keep its terminal open while using PyEV.

The local launcher uses installed Python directly. It does not require Pyodide downloads or third-party Python packages, and works offline. The local interface, engine and exports are the same as the web edition.

If the source ZIP is absent from an extracted copy, the launcher recreates it at startup so **Python code** also works locally. If the project folder is read-only, calculations still run and the terminal explains how to enable the download. All source files remain available in the extracted folder.

### Python / command-line calculations

```bash
python pyev.py init My_Design.json
python pyev.py run My_Design.json --out outputs/my_design
python pyev.py run --out outputs/kunray_default
```

Each run saves the analysed input file, full results JSON, every table as CSV, every graph as SVG and a self-contained HTML report. Open that HTML in a browser to read or print it to PDF.

For scripts and notebooks:

```python
import sys
sys.path.insert(0, "dist")
from pyev_engine import analyze

result = analyze({"mass_kg": 225, "gear_ratio": 7,
                  "grade_pct": 7, "speed_kmh": 25})
# Omitted values inherit the documented example assumptions.
for metric in result["metrics"]:
    print(metric["label"], metric["value"], metric["unit"])
```

## What is included

- Editable specifications with units, ranges and input guidance.
- A constant-torque reference model and an imported motor torque-versus-rpm curve option.
- Road-load, wheel-force, required-torque, gearing, acceleration, power and propulsion-mass calculations.
- Battery energy, operating demand, runtime and range estimates; current and voltage compatibility checks.
- Brake, tyre-traction, chain/sprocket and simplified optional frame calculations.
- A default 360-condition sweep and editable sweep ranges up to 10000 combinations.
- Filterable/paginated scenario results, separate model-limit flags and vector performance graphs.
- JSON design save/import; CSV table downloads; SVG graphs; complete HTML and Word reports.
- One shared Python engine, independent numerical tests, source license and GitHub Pages deployment workflow.

The Word report generated in the web interface includes all result tables and chart images. Its tables are editable. The HTML report retains vector charts and supports Print / Save as PDF. Governing-equation sections are omitted from the generated Word and HTML reports. The interactive **Method & sources** page retains the equations and calculation guidance for users who want to inspect the model. Exports use the last completed analysis; editing inputs marks the displayed results as out of date until the next run.

## Default engineering case

| Input | Value |
|---|---:|
| Total running mass | 225 kg |
| Reduction ratio | 7:1 |
| Uphill grade | 7% |
| Road speed | 25 km/h |
| Tyre diameter | 280 mm |
| Assumed motor torque | 5.4 N·m |
| Total transmission efficiency | 0.90 |
| Rolling coefficient | 0.02 |
| Aerodynamic drag area | 0.60 m² |
| Air density | 1.20 kg/m³ |

The report reference values are 243.0 N drive force, 215.52869 N road resistance, 4.7895265 N·m required motor torque, 3315.72798 rpm motor speed and 0.122095 m/s² nominal acceleration. The reference 4900 rpm is an adopted analysis boundary; it is not a verified hard speed limit.

The 360-case grid is the Cartesian product of:

- Mass: 100, 150, 180, 200, 225, 250 kg.
- Reduction ratio: 6, 7, 8, 10.
- Grade: 0, 5, 7, 10, 15%.
- Speed: 15, 25, 35 km/h.

These nominal torque/reference-speed classifications are P=225, T=75, R=50 and TR=10. Other checks remain independent. The selected example is case 263. Case 239 remains T even though its torque demand rounds to 5.40 N·m at only two decimal places.

The file `examples/motor_curve.csv` is illustrative test data, not a measured Kunray curve. Replace it with a verified curve for a real design.

## Understanding the results

| Code | Interpretation |
|---|---|
| P | The assumed motor torque and reference-speed checks are met. |
| T | Required torque exceeds the model value inside the speed range. |
| R | Operating rpm is outside the adopted reference range. |
| TR | Both nominal torque and reference-speed checks are exceeded. |
| U | The requested condition is outside supplied torque-curve coverage or cannot be evaluated. |

A P result is not a completed vehicle design approval. Battery current, traction, braking, transmission packaging and structural checks can still identify a problem. An unknown input must not be treated as a verified limit.

The default battery is an illustrative design assumption, not a battery included in the quoted kit. The controller's quoted 45 A is not automatically interpreted as a battery-side limit. Select its current basis or enter independently verified battery/phase limits. Quoted input power, shaft output power and peak versus continuous capability are different quantities.

Torque interpolation is used only within the supplied curve range. The software does not extrapolate an unknown motor curve. Slow hill climbing and standing starts still require motor/controller thermal and launch verification. Negative downhill wheel-power demand is braking demand; it does not imply regenerative charging.

The optional frame model is a simplified beam calculation. Vehicle load approval requires the actual frame, welds, axle, bearings, tyres, brakes and motor duty to be verified. See [the model guide](docs/MODEL_GUIDE.md) and [validation record](docs/VALIDATION.md).

## Host on GitHub Pages

The repository stores the code. GitHub Pages supplies the public application URL. Ordinary server-side Python does not run on Pages; this package works because the Python engine runs in each visitor's browser.

For the account `thangotech`, a repository named `pyev` produces a project URL of:

`https://thangotech.github.io/pyev/`

That is the expected address after enabling Pages and completing deployment, not a claim that the repository has already been created.

1. Create a **public** GitHub repository named `pyev`.
2. Put the contents of the extracted **PyEV** folder in the repository root. Include the `.github/workflows/pages.yml` file. Do not upload only the ZIP.
3. In **Settings → Pages → Build and deployment**, choose **GitHub Actions**.
4. Open **Actions → Deploy PyEV to GitHub Pages → Run workflow**, or push a change to `main`.
5. Wait for the workflow to succeed. Open the URL shown in the deployment result. Visitors can use that URL directly.

The workflow runs the Python tests, rebuilds the source ZIP and publishes the `dist` folder. All web asset URLs are relative, so a repository path such as `/pyev/` is supported. Future pushes to `main` repeat the tests and deployment.

For an upload-only Pages setup, publish the contents of `dist` at the root of a separate public repository and select **Deploy from a branch → main → /(root)**. The downloadable ZIP inside that folder contains the complete Python source. Use the full-project workflow above when developing PyEV itself.

Primary hosting documentation: [GitHub Pages creation](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site), [custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages), [Pyodide web workers](https://pyodide.org/en/stable/usage/webworker.html).

## Development

```bash
python -m unittest discover -s tests -v
python build_source.py
python serve.py
```

The authoritative calculation module is `dist/pyev_engine.py`; `dist/pyev_reports.py` only formats computed results. Browser presentation is in `dist/app.mjs`, `dist/charts.mjs` and `dist/exports.mjs`. `dist/worker.mjs` dispatches calculations to local Python or the pinned browser runtime. No physics is duplicated in JavaScript.

To change the runtime pin, edit `runtimeURL` in `dist/worker.mjs`, read the corresponding Pyodide release instructions and repeat numerical/export/runtime validation. Changes to an engineering equation require a corresponding independent reference or invariant test. See `docs/VALIDATION.md` for the verification actually performed for this release.

## License

MIT. Copyright 2026 Prof Bonginkosi Thango, Thangotech Engineering. The separate Pyodide runtime and browser components retain their own licenses. This repository does not bundle the Python runtime download.
