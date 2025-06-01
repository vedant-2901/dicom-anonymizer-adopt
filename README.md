

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
