# DICOM Anonymizer - ADOPT Project

This repository contains a Python script to anonymize DICOM (CT scan) data for the ADOPT medical imaging pipeline.

## Features

- Removes PHI (e.g., patient name, ID, institution)
- Regenerates UIDs for ethical dataset reuse
- GDCM-based decompression support for compressed DICOMs
- Preserves essential metadata for segmentation
- Recursive directory processing

## Installation

Install required libraries:

```bash
pip install -r requirements.txt
```

Install GDCM (for compressed DICOM support):

```bash
conda install -c conda-forge gdcm
```

## Usage

```bash
python anonymize_dicom.py -i /path/to/input_dicom -o /path/to/output_dicom
```

Enable debug logging:

```bash
python anonymize_dicom.py -i input_dir -o output_dir -v
```

## Requirements

```
pydicom>=2.4.0
tqdm
gdcm
```
