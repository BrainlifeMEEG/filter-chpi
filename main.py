"""
Remove continuous head-position-indicator (cHPI) and line-noise artifacts
from raw MEG data.

This app loads raw MEG data with cHPI coils active during acquisition and
removes the cHPI (and, optionally, power-line) artifacts from the sensor
signals using MNE's iterative-fitting method (mne.chpi.filter_chpi), which
is recommended over notch filtering since cHPI signals are not stationary
(head movements act like amplitude modulators on them). It generates a
before/after PSD comparison and produces a report.

Inputs
------
mne : str
    Path to the input MNE-format MEG data file (.fif). Must have real cHPI
    information (cHPI was on during the recording), unless allow_line_only
    is set.
include_line : bool
    If true, also filter line (powerline) noise. Default: true.
t_step : float
    Time step to use for cHPI amplitude estimation, in seconds. Default: 0.01.
t_window : str
    Time window to use to estimate the amplitudes, in seconds, or "auto"
    for MNE's automatic window selection. Default: "auto".
ext_order : int
    External order for SSS-like interference suppression, used as
    projection vectors during fitting. Default: 1.
allow_line_only : bool
    If true, allow filtering line noise only, even when no real cHPI
    information is present. Default: false (fails cleanly if cHPI info is
    missing and this is false).

Outputs
-------
raw.fif : str
    MEG data with cHPI/line-noise artifacts removed, in MNE format.
psd_before.png / psd_after.png : str
    PSD plots before and after filtering.
report.html : str
    HTML report comparing original and filtered data.
"""

# Copyright (c) 2026 brainlife.io
#
# Remove continuous head-position-indicator (cHPI) and line-noise
# artifacts from raw MEG data.
#
# Authors:
# - Maximilien Chaumon (https://github.com/dnacombo)

import sys
import os
import mne
import mne.chpi
import matplotlib
import matplotlib.pyplot as plt

# Add brainlife_utils to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'brainlife_utils'))

from brainlife_utils import (
    load_config,
    setup_matplotlib_backend,
    create_product_json,
    add_info_to_product,
    add_image_to_product,
    add_raw_info_to_product,
    ensure_output_dirs,
    require_config_keys,
    save_figure_with_base64,
)

# Setup environment
setup_matplotlib_backend()
config = load_config()
require_config_keys(config, ['mne'])

ensure_output_dirs('out_dir', 'out_report', 'out_figs')

# == PARSE PARAMETERS ==
include_line = config.get('include_line', True)
t_step = float(config.get('t_step', 0.01))
t_window = config.get('t_window', 'auto')
if t_window != 'auto':
    t_window = float(t_window)
ext_order = int(config.get('ext_order', 1))
allow_line_only = config.get('allow_line_only', False)

# == LOAD DATA ==
fname = config['mne']
raw = mne.io.read_raw_fif(fname, preload=True)
raw_orig = raw.copy()

# == CHECK FOR REAL cHPI INFO ==
# filter_chpi() itself raises if no cHPI info is present, unless
# allow_line_only=True -- check up front instead of letting that surface
# as an uncaught stack trace, so a genuinely missing-cHPI dataset fails
# cleanly with a product.json message rather than a crash.
hpi_freqs, _, _ = mne.chpi.get_chpi_info(raw.info, on_missing='warn')
if len(hpi_freqs) == 0 and not allow_line_only:
    product_items = []
    add_info_to_product(
        product_items,
        f"No cHPI information found in {os.path.basename(fname)} (cHPI "
        f"must have been on during acquisition). Set allow_line_only=true "
        f"to filter line noise only, without cHPI info.",
        'error'
    )
    create_product_json(product_items)
    sys.exit(1)

# == PSD BEFORE ==
fig_before = raw_orig.compute_psd().plot(exclude='bads', show=False)
before_path = os.path.join('out_figs', 'psd_before.png')
before_base64 = save_figure_with_base64(fig_before, before_path, dpi_file=150, dpi_base64=80)

# == FILTER cHPI / LINE NOISE ==
print(f"Filtering cHPI{'/line noise' if include_line else ''} "
      f"({len(hpi_freqs)} coil(s) detected)...", flush=True)
mne.chpi.filter_chpi(
    raw,
    include_line=include_line,
    t_step=t_step,
    t_window=t_window,
    ext_order=ext_order,
    allow_line_only=allow_line_only,
)

# == PSD AFTER ==
fig_after = raw.compute_psd().plot(exclude='bads', show=False)
after_path = os.path.join('out_figs', 'psd_after.png')
after_base64 = save_figure_with_base64(fig_after, after_path, dpi_file=150, dpi_base64=80)

# == GENERATE REPORT ==
print("Generating report...", flush=True)
report = mne.Report(title='cHPI Filtering Report')
report.add_raw(raw_orig, 'Original Data', psd=True)
report.add_raw(raw, 'cHPI-Filtered Data', psd=True)
report.save('out_report/report.html', overwrite=True, verbose=False)

# == SAVE FILTERED DATA ==
raw.save('out_dir/raw.fif', overwrite=True)

# Validate round-trip before declaring success
_ = mne.io.read_raw_fif('out_dir/raw.fif', preload=False, verbose=False)
print("Verified out_dir/raw.fif reloads successfully", flush=True)

# == CREATE PRODUCT.JSON ==
product_items = []
add_info_to_product(
    product_items,
    f"Filtered {len(hpi_freqs)} cHPI coil(s) at "
    f"{', '.join(f'{f:.1f}' for f in hpi_freqs)} Hz"
    f"{' + line noise' if include_line else ''}",
    'success'
)
add_raw_info_to_product(product_items, raw)
add_image_to_product(product_items, 'PSD before filtering', base64_data=before_base64)
add_image_to_product(product_items, 'PSD after filtering', base64_data=after_base64)
create_product_json(product_items)
