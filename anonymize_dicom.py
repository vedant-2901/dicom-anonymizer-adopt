#!/usr/bin/env python3

"""
ADOPT Project - DICOM Anonymization Script
Author: [Your Name]
Date: [YYYY-MM-DD]

This script anonymizes CT scan DICOM datasets by removing PHI and regenerating UIDs.
It preserves essential metadata for AI-based segmentation tasks.

Dependencies:
    - pydicom
    - gdcm
    - tqdm
"""

import os
import argparse
import logging
import pydicom
from pydicom.uid import generate_uid
from pydicom.dataelem import DataElement
from tqdm import tqdm

# DICOM tags to anonymize
ANONYMIZE_TAGS = {
    "PatientName", "PatientID", "PatientBirthDate", "PatientSex",
    "OtherPatientIDs", "OtherPatientNames", "EthnicGroup",
    "PatientComments", "ReferringPhysicianName", "InstitutionName",
    "InstitutionAddress", "AccessionNumber", "StudyID",
    "SeriesDescription", "StudyDescription", "OperatorsName",
    "PerformingPhysicianName", "RequestingPhysician", "StationName",
    "DeviceSerialNumber"
}

def anonymize_dataset(ds: pydicom.Dataset) -> pydicom.Dataset:
    """
    Remove sensitive tags and regenerate UIDs in the DICOM dataset.
    """
    for tag in ANONYMIZE_TAGS:
        if tag in ds:
            ds.data_element(tag).value = ''

    # Regenerate essential UIDs
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()

    # Mark as anonymized
    ds.add(DataElement(0x00120062, 'LO', 'Anonymized by ADOPT'))

    return ds

def anonymize_dicom_file(in_path: str, out_path: str):
    """
    Anonymize a single DICOM file.
    """
    try:
        ds = pydicom.dcmread(in_path, force=True)

        # Optional: Trigger pixel decompression if GDCM is available
        if 'PixelData' in ds:
            _ = ds.pixel_array

        ds = anonymize_dataset(ds)

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        ds.save_as(out_path)

    except Exception as e:
        logging.error(f"Error processing {in_path}: {e}")

def anonymize_directory(input_dir: str, output_dir: str):
    """
    Recursively anonymize all DICOM files in a directory.
    """
    logging.info(f"Starting anonymization: {input_dir} → {output_dir}")

    for root, _, files in os.walk(input_dir):
        for file in tqdm(files, desc=f"Processing {root}"):
            if file.lower().endswith(".dcm"):
                in_file = os.path.join(root, file)
                rel_path = os.path.relpath(in_file, input_dir)
                out_file = os.path.join(output_dir, rel_path)
                anonymize_dicom_file(in_file, out_file)

    logging.info("✅ Anonymization complete.")

def main():
    parser = argparse.ArgumentParser(description="DICOM Anonymizer for ADOPT Project")
    parser.add_argument("--input", "-i", required=True, help="Path to input DICOM directory")
    parser.add_argument("--output", "-o", required=True, help="Path to save anonymized DICOMs")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable debug logging")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    anonymize_directory(args.input, args.output)

if __name__ == "__main__":
    main()
