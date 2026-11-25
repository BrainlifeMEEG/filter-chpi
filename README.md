<h1 align="center">Filter cHPI</h1>

<p align="center">
  Removes continuous head-position-indicator (cHPI) and optionally power-line noise from raw MEG data with MNE-Python mne.chpi.filter_chpi, with before/after PSD plots and an HTML report.
</p>

<p align="center">
  <a href="https://github.com/brainlife/abcd-spec"><img src="https://img.shields.io/badge/ABCD_Spec-v1.1-green.svg" alt="ABCD Spec v1.1"></a>
  <a href="https://doi.org/10.25663/brainlife.app.962"><img src="https://img.shields.io/badge/Brainlife-brainlife.app.962-blue.svg" alt="Run on brainlife.io"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-see_LICENSE-lightgrey.svg" alt="License"></a>
</p>

## At a glance

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Removes continuous head-position-indicator (cHPI) and optionally power-line noise from raw MEG data with MNE-Python mne.chpi.filter_chpi, with before/after PSD plots and an HTML report.**

Uses MNE's iterative-fitting cHPI filter, recommended over notch filtering because cHPI signals are modulated by head movement, to remove the coil frequencies (and line noise when include_line is true) from the MEG sensors. Use it on recordings acquired with cHPI coils active, before further preprocessing. Without cHPI information the App stops unless allow_line_only is set, in which case only line noise is removed.

| | |
|---|---|
| **Inputs** | `neuro/meeg/mne/raw` |
| **Outputs** | `neuro/meeg/mne/raw` · `generic/image/png` · `report/html` |
| **Container** | `brainlifemeeg/mne:1.12.1` |
| **Resources** | 4 CPUs · 20 GB memory |
| **Run it** | [doi.org/10.25663/brainlife.app.962](https://doi.org/10.25663/brainlife.app.962) |

#### Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meeg/mne/raw` | yes | Raw MEG data in MNE FIF format recorded with cHPI coils active. Must contain cHPI information unless allow_line_only is true. |

#### Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | Raw MEG data with cHPI (and line) noise removed (raw.fif). |
| `out_figs` | `generic/image/png` | Power spectral density plots before and after filtering. |
| `out_report` | `report/html` | HTML report comparing original and filtered data. |

<details>
<summary><b>Parameters</b> (5)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `include_line` | boolean | `true` | If true, also filter line (powerline) noise, in addition to cHPI. |
| `t_step` | number | `0.01` | Time step to use for cHPI amplitude estimation, in seconds. |
| `t_window` | string | `auto` | Time window to use to estimate the amplitudes, in seconds, or "auto" for MNE's automatic window selection. |
| `ext_order` | number | `1` | The external order for SSS-like interference suppression; the SSS bases are used as projection vectors during fitting. |
| `allow_line_only` | boolean | `false` | If true, allow filtering line noise only, even when no real cHPI information is present. |

</details>

<!-- brainlife-app:end -->

## Running the App

### On brainlife.io

Open the App at [doi.org/10.25663/brainlife.app.962](https://doi.org/10.25663/brainlife.app.962), choose `neuro/meeg/mne/raw` from your project, set the parameters and press **Execute**. The results are saved to your project as `neuro/meeg/mne/raw`, `generic/image/png`, `report/html`.

### Locally

You need [Singularity/Apptainer](https://apptainer.org/) (the App runs in `brainlifemeeg/mne:1.12.1`), [`jq`](https://jqlang.github.io/jq/).

1. Clone this repository.
2. Create `config.json` with the paths to your inputs and the parameters:

   ```json
   {
       "mne": "/path/to/fif/mne",
       "include_line": true,
       "t_step": 0.01,
       "t_window": "auto",
       "ext_order": 1,
       "allow_line_only": false
   }
   ```

3. Run `./main`.

## Input Files

- **meg.fif**: MNE-format raw MEG data file, with cHPI coils active during acquisition (required,
  unless `allow_line_only` is set)

## Output Files

- **raw.fif**: MEG data with cHPI/line-noise artifacts removed, in MNE format
- **psd_before.png** / **psd_after.png**: Power spectral density plots before and after filtering
- **report.html**: Interactive HTML report with before/after data summaries and PSDs

## Configuration Parameters

- **include_line** (bool): If true, also filter line (powerline) noise, in addition to cHPI.
  Default: `true`.
- **t_step** (float): Time step to use for cHPI amplitude estimation, in seconds. Default: `0.01`
  (10 ms).
- **t_window** (string): Time window to use to estimate the amplitudes, in seconds, or `"auto"` for
  MNE's automatic window selection. Default: `"auto"`.
- **ext_order** (int): The external order for SSS-like interference suppression; the SSS bases are
  used as projection vectors during fitting. Default: `1`.
- **allow_line_only** (bool): If true, allow filtering line noise only, even when the input has no
  real cHPI information present. Default: `false` — the app fails cleanly (with a product.json
  error, not a crash) if no cHPI information is found and this is false.

## Local Testing

```bash
# Update config.json with your data path
# Then run:
python main.py
```

## cHPI Filtering

`mne.chpi.filter_chpi` fits and subtracts the cHPI coil signals (and, optionally, line noise)
directly from the continuous data using an iterative method, rather than a fixed notch filter —
this handles the fact that cHPI amplitudes vary over time as the head moves relative to the coils.
Requires the raw data to be preloaded and to carry real cHPI channel/frequency information (present
whenever cHPI coils were switched on during acquisition); operates in place on the loaded data.

## Power Spectral Density (PSD)

The report includes PSD plots for both the original and filtered data — the cHPI coil frequencies
(and line-noise frequency and its harmonics, if `include_line` is set) should be visibly reduced in
the "after" plot.

## Citing

If you use this App, please cite it, the software it builds on and brainlife.io:

- Filter cHPI. brainlife.io App. [doi:10.25663/brainlife.app.962](https://doi.org/10.25663/brainlife.app.962)
- Gramfort A. et al. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)
- Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Avesani P, McPherson B, Hayashi S, et al. The open diffusion data derivatives, brain data upcycling via integrated publishing of derivatives and reproducible open cloud services. *Scientific Data* 6:69 (2019). [doi:10.1038/s41597-019-0073-y](https://doi.org/10.1038/s41597-019-0073-y)

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)

## Funding

[![Wellcome-226486/Z/22/Z](https://img.shields.io/badge/Wellcome-226486%2FZ%2F22%2FZ-purple.svg)](https://wellcome.org/)
[![NIH-NINDS-U24NS140384](https://img.shields.io/badge/NIH_NINDS-U24NS140384-green.svg)](https://reporter.nih.gov/project-details/11261037)
[![NIH-NINDS-UM1NS132207](https://img.shields.io/badge/NIH_NINDS-UM1NS132207-green.svg)](https://reporter.nih.gov/project-details/11411328)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://reporter.nih.gov/project-details/10262925)
[![NIH-NIBIB-R01EB030896](https://img.shields.io/badge/NIH_NIBIB-R01EB030896-green.svg)](https://reporter.nih.gov/project-details/10428625)
[![NIH-NIMH-R01MH126699](https://img.shields.io/badge/NIH_NIMH-R01MH126699-green.svg)](https://reporter.nih.gov/project-details/10460628)
[![NIH-NIDCD-R01DC020088](https://img.shields.io/badge/NIH_NIDCD-R01DC020088-green.svg)](https://reporter.nih.gov/project-details/11140284)
[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-2203524](https://img.shields.io/badge/NSF_BCS-2203524-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2203524)
[![NSF-IIS-1636893](https://img.shields.io/badge/NSF_IIS-1636893-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-OAC-2148729](https://img.shields.io/badge/NSF_OAC-2148729-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148729)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NSF-IIS-2148700](https://img.shields.io/badge/NSF_IIS-2148700-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=2148700)
[![NSF-OAC-1916518](https://img.shields.io/badge/NSF_OAC-1916518-blue.svg)](https://www.nsf.gov/awardsearch/showAward?AWD_ID=1916518)

<sub>brainlife.io, which runs this App, is publicly funded by Wellcome, the U.S. National Institutes of Health and the U.S. National Science Foundation; acknowledging that support helps keep it running.</sub>

## License

See [LICENSE](LICENSE).
