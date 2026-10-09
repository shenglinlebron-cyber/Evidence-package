# Rights and provenance

TruckDrive, provided by Torc Robotics, Inc., available at torc-ai.github.io/TruckDrive, used under the Torc Robotics Non-Commercial License v1.0.

Copyright (c) 2026 TORC ROBOTICS, INC. All rights reserved.

## Dataset terms

The [official project page](https://torc-ai.github.io/TruckDrive/), [Non-Commercial License v1.0](https://torc-ai.github.io/TruckDrive/LICENSE-NONCOMMERCIAL.txt) (effective May 1, 2026), and [dataset notice](https://torc-ai.github.io/TruckDrive/NOTICE.txt) are the governing publisher references. The official Hugging Face distribution also supplies license material under its [TruckDrive tree](https://huggingface.co/datasets/Torc-Robotics/TruckDrive/tree/main/TruckDrive).

Section 3 permits non-commercial sharing of licensed and adapted material, subject to Section 4. Dataset-derived figures and evidence extracts retain the license, attribution and publisher warranty disclaimer: the publisher supplies the material AS-IS and AS-AVAILABLE, with the full disclaimers/limitations in Section 6. Commercial use requires the publisher's separate written license. No additional legal or technological restrictions are imposed on recipients' licensed rights (Sections 4(g)–4(h)). Keeping complete source files outside this repository is the contributor's publication decision, not a new downstream license condition.

No blanket repository license re-licenses the dataset, figures or metadata. The devkit's software license does not replace the dataset license. This repository claims no publisher endorsement, sponsorship, affiliation or official status. It does not use vehicle plates to query motor-vehicle records or identify people. Consult any applicable publisher-supplied third-party notices with the source release; this evidence package is not a certification that no third-party interests exist.

## Changes and provenance

The already existing scientific renderings include native camera crops/ROIs, box projections, selected-point plots and annotations. These are derived evidence, not native-resolution complete source photographs. Publication adds an English report, captions/layout, compact tables, public relative locators and a standard-library integrity verifier. Existing source PNG pixels, fixed row selections and scientific values are unchanged. No AI-generated imagery or fitted alignment is used. No complete source JPEG/BIN, annotation/calibration file, source-asset ZIP or model weight is committed.

Source-file SHA fields identify locally held bytes or earlier recorded inputs. Historical-result and selection-table SHA fields identify pre-translation/pre-redaction source bytes; omitted files are marked SOURCE_NOT_INCLUDED. They are not hashes of the compact public extracts. SHA256SUMS.txt hashes the actual public package files. The XYZ digest in formal_point_sets.csv hashes only concatenated existing original-row XYZ bytes in published row order and can be checked against matching external BIN files; it is not a new geometric measurement.

The 20 locally held released source files were preserved byte for byte. The remaining asset references remain external and may not be locally held. Original basenames and dataset-relative paths are retained, but source publisher version/archive identity has not been authenticated. Neither local SHA equality nor the public verifier resolves upstream deskew, pose/object compensation, GT time or camera-generation contracts. Section 5 of the dataset license distinguishes released data from unprocessed raw sensor streams; this repository therefore calls the external inputs released source files.

## Citation

CITATION.bib reproduces the [official project page's BibTeX](https://torc-ai.github.io/TruckDrive/#bibtex) for the 2026 CVPR dataset paper. The license requests the publisher's CITATION.cff format for academic publications; that file was not among the held evidence inputs and could not be verified in the public devkit. Consult the publisher's current release citation before a formal academic submission. This operational citation-format uncertainty does not authenticate or change the held source release.
