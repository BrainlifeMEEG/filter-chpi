# Filter cHPI Artifacts from Raw MEG Data

<!-- brainlife-app:begin (generated from the App manifest; edit the manifest, not this block) -->

> **Removes continuous head-position-indicator (cHPI) and optionally power-line noise from raw MEG data with MNE-Python mne.chpi.filter_chpi, with before/after PSD plots and an HTML report.**

Uses MNE's iterative-fitting cHPI filter, recommended over notch filtering because cHPI signals are modulated by head movement, to remove the coil frequencies (and line noise when include_line is true) from the MEG sensors. Use it on recordings acquired with cHPI coils active, before further preprocessing. Without cHPI information the App stops unless allow_line_only is set, in which case only line noise is removed.

| | |
|---|---|
| 📥 **Inputs** | `neuro/meeg/mne/raw` |
| 📤 **Outputs** | `neuro/meeg/mne/raw` · `generic/image/png` · `report/html` |
| 🐳 **Container** | `brainlifemeeg/mne:1.12.1` |
| ⚙️ **Resources** | 4 CPUs · 20 GB memory |
| 🔗 **Run it** | [doi.org/10.25663/brainlife.app.962](https://doi.org/10.25663/brainlife.app.962) |

#### 📥 Inputs

| Input | Datatype | Required | Description |
|---|---|---|---|
| `fif` | `neuro/meeg/mne/raw` | yes | Raw MEG data in MNE FIF format recorded with cHPI coils active. Must contain cHPI information unless allow_line_only is true. |

#### 📤 Outputs

| Output | Datatype | Description |
|---|---|---|
| `out_dir` | `neuro/meeg/mne/raw` | Raw MEG data with cHPI (and line) noise removed (raw.fif). |
| `out_figs` | `generic/image/png` | Power spectral density plots before and after filtering. |
| `out_report` | `report/html` | HTML report comparing original and filtered data. |

<details>
<summary><b>⚙️ Parameters</b> (5)</summary>

| Parameter | Type | Default | Description |
|---|---|---|---|
| `include_line` | boolean | `true` | If true, also filter line (powerline) noise, in addition to cHPI. |
| `t_step` | number | `0.01` | Time step to use for cHPI amplitude estimation, in seconds. |
| `t_window` | string | `auto` | Time window to use to estimate the amplitudes, in seconds, or "auto" for MNE's automatic window selection. |
| `ext_order` | number | `1` | The external order for SSS-like interference suppression; the SSS bases are used as projection vectors during fitting. |
| `allow_line_only` | boolean | `false` | If true, allow filtering line noise only, even when no real cHPI information is present. |

</details>

📚 **References used by this App:**
- Hayashi S., Caron B. A., Heinsfeld A. S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nature Methods 21, 809-813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)
- Gramfort A. et al. MEG and EEG data analysis with MNE-Python. Frontiers in Neuroscience 7:267 (2013). [doi:10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)

<!-- brainlife-app:end -->

## Description

This Brainlife.io application removes continuous head-position-indicator (cHPI) and, optionally,
power-line noise artifacts from raw MEG data using MNE-Python's `mne.chpi.filter_chpi` — an
iterative-fitting method recommended over plain notch filtering, since cHPI signals are not
stationary (head movements act like amplitude modulators on them).

The app generates:
- MEG data with cHPI/line-noise artifacts removed, in MNE-Python format
- Power spectral density (PSD) plots before and after filtering
- An HTML report comparing original and filtered data

## Inputs

### Input Files

- **meg.fif**: MNE-format raw MEG data file, with cHPI coils active during acquisition (required,
  unless `allow_line_only` is set)

## Outputs

### Output Files

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

## Usage

### Running on Brainlife.io

1. Select an MEG raw data file that had cHPI coils active during acquisition.
2. Select the filter-chpi app.
3. Configure parameters (the defaults match MNE's own recommended defaults for `filter_chpi`).
4. Submit the task.
5. Review the before/after PSD plots in the report to confirm the cHPI coil frequencies (and line
   noise, if enabled) are gone from the filtered spectrum.

### Local Testing

```bash
# Update config.json with your data path
# Then run:
python main.py
```

## Technical Details

### cHPI Filtering

`mne.chpi.filter_chpi` fits and subtracts the cHPI coil signals (and, optionally, line noise)
directly from the continuous data using an iterative method, rather than a fixed notch filter —
this handles the fact that cHPI amplitudes vary over time as the head moves relative to the coils.
Requires the raw data to be preloaded and to carry real cHPI channel/frequency information (present
whenever cHPI coils were switched on during acquisition); operates in place on the loaded data.

### Power Spectral Density (PSD)

The report includes PSD plots for both the original and filtered data — the cHPI coil frequencies
(and line-noise frequency and its harmonics, if `include_line` is set) should be visibly reduced in
the "after" plot.

## Authors

- Maximilien Chaumon (https://github.com/dnacombo)

## Citations

Hayashi, S., Caron, B.A., Heinsfeld, A.S. et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. Nat Methods 21, 809–813 (2024). https://doi.org/10.1038/s41592-024-02237-2

## Funding Acknowledgement

brainlife.io is publicly funded. We kindly ask that you acknowledge the funding below in your code and publications.

[![NSF-BCS-1734853](https://img.shields.io/badge/NSF_BCS-1734853-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1734853)
[![NSF-BCS-1636893](https://img.shields.io/badge/NSF_BCS-1636893-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1636893)
[![NSF-ACI-1916518](https://img.shields.io/badge/NSF_ACI-1916518-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1916518)
[![NSF-IIS-1912270](https://img.shields.io/badge/NSF_IIS-1912270-blue.svg)](https://nsf.gov/awardsearch/showAward?AWD_ID=1912270)
[![NIH-NIBIB-R01EB029272](https://img.shields.io/badge/NIH_NIBIB-R01EB029272-green.svg)](https://grantome.com/grant/NIH/R01-EB029272-01)
