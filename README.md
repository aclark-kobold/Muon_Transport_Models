# Muon Transport Models

Tools for comparing models of the cosmic-ray muon flux at the surface and underground.

- **Surface flux:** five analytic parametrizations (Gaisser, Guan, Tang, Bugaev/Reyna, Smith-Duller/Chatzidakis) are compared with each other and with measured spectra (BESS-TeV, L3+C, LVD).
- **Reference models:** [daemonflux](https://github.com/mceq-project/daemonflux) (muon-calibrated flux model) and PARMA simulation output serve as references.
- **Underground:** an analytic propagation (flat overburden, continuous energy loss) turns a surface model into underground spectra, intensities and detector rates.

## Repository layout

```
Analytical_Models/
  Analytical_Models/                  Surface flux models (importable modules)
    gaisser_model.py                  Gaisser formula
    guan_model.py                     Modified Gaisser (Guan et al.)
    tang_model.py                     Modified Gaisser (Tang et al., PRD 74, 053007)
    bugaev_reyna_model.py             Bugaev (vertical only) and Reyna formulas
    smith_duller_model.py             Smith-Duller / Chatzidakis
    muon_kinematics.py                Shared helpers (momentum, dp/dE, unit conversion)
  Model_Analysis/
    model_analysis.py                 Plots of all models (differential, integrated, angular)
    Plots/
  Model_Comparison/
    make_energy_tables.py             Converts published momentum tables to energy tables; tabulates models at zenith 0
    compare_to_data.py                Overlays measured fluxes on every model
    model_comparison_analysis.py      Chi-squared comparison of models to data, model ranking
    guan_vs_daemonflux.py             Guan vs daemonflux vs data (and PARMA)
    Data/                             Energy tables, chi2 CSVs, PARMA output (mysite.out)
    Plots/
  Analytical_Propagation_Underground/
    muon_diff_energy_spectrum_underground.py   Underground spectra, intensity, mean energy, angular distributions
    cylinder_muon_rate_vs_depth.py             Muon rate through a cylindrical detector vs depth (output in .txt)
    muons_underground.py                       Earlier standalone version of the underground calculation
    Plots/
DAEMONFlux/
  test.py                             Surface muon spectra from daemonflux -> CSV + plots
  Data/  Plots/
  README.md                           User guide for daemonflux
```

## Conventions

- `E` is total muon energy in GeV; zenith angle `theta` is in radians.
- Model flux is differential, `dPhi/dE`, in m^-2 s^-1 sr^-1 GeV^-1 (mu+ + mu-).
- The `DAEMONFlux/` scripts and the underground code work internally in cm^-2, and the underground plots convert to m^-2.
- daemonflux works in total momentum and returns `p^3 * dPhi/dp`. The scripts convert this to `dPhi/dE`.

## Setup

Python 3.10 or newer (needed by daemonflux).

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1      macOS/Linux: source .venv/bin/activate
pip install numpy scipy matplotlib daemonflux
```

## Running

Each script adds `../Analytical_Models` to `sys.path` itself and writes to its own `Plots/` (or `Data/`) folder. Run each from its own directory:

```bash
cd Analytical_Models/Model_Comparison
python make_energy_tables.py          # rebuild energy tables in Data/
python compare_to_data.py
python model_comparison_analysis.py
python guan_vs_daemonflux.py          # needs daemonflux

cd ../Model_Analysis
python model_analysis.py

cd ../Analytical_Propagation_Underground
python muon_diff_energy_spectrum_underground.py
python cylinder_muon_rate_vs_depth.py

cd ../../DAEMONFlux
python test.py
```

## Caveats

- **daemonflux** is calibrated for roughly 5 GeV to 10 TeV. It was fitted to BESS-TeV and L3+C, so those are not independent tests of it. Here it is used with `location='generic'` (no site-specific altitude or atmosphere).
- **LVD** is not a direct sea-level measurement. It is derived from underground data using a Gaisser-shaped spectrum, so its shape is partly built in.
- **Tang model:** Eq. (7) of the paper is ambiguous. `EXPONENT_USES_TILDE` in `tang_model.py` selects the interpretation (default `True`). See the docstring.
- **PARMA** muons are only tabulated up to about 0.9 TeV, and the table is for its own site and date, not the experiments' sites.
- **Underground loss parameters** `A_LOSS = 0.25 GeV/m.w.e.` and `B_LOSS = 0.36e-3 /m.w.e.` are effective values for standard-rock-like material, reliable from roughly 0.5 to 6 km.w.e. Change them for other rock.

## References

- Tang, Horton-Smith, Kudryavtsev, Tonazzo, Phys. Rev. D 74, 053007 (2006), [arXiv:hep-ph/0604078](https://arxiv.org/abs/hep-ph/0604078)
- Yañez and Fedynitch, daemonflux, [arXiv:2303.00022](https://arxiv.org/abs/2303.00022)
- See also [DAEMONFlux/README.md](DAEMONFlux/README.md)
