# TruckDrive: reproducible box–surface discrepancies

## 1. Main observations

Existing fixed visible-surface selections expose geometric discrepancies in three objects and four frames. These are signed surface-to-GT-face medians in box-local metric coordinates: positive means beyond the named face. They are not estimates of object-center error.

| Case | Scene / native object / sync | Native subtype | Range XY (m) | Selected / outside face | Face | Median (m) | Atlas pages |
|---|---|---|---:|---:|---|---:|---|
| H01 | scene_35_31 / Vehicle:97 / 0188 | Trailer | 96.99 | 589 / 565 | +Y side | +0.443503 | 2–3 |
| F01 | scene_36_27 / Vehicle:3 / 0118 | Vehicle-Passenger; visually van | 74.88 | 1461 / 1351 | -X rear | +0.461251 | 5–6 |
| F03 far | scene_36_39 / Vehicle:10 / 0032 | Trailer | 186.12 | 282 / 282 | -X rear | +0.685512 | 7–8 |
| F03 near | scene_36_39 / Vehicle:10 / 0070 | Trailer | 76.30 | 1600 / 1592 | -X rear | +0.472415 | 9–10 |

Selection is post hoc manual surface judgment, not a blinded sample. The existing F01/F03 source code selects positive-camera-depth points inside fixed image polygons, without filtering by GT-box membership; every selected row is retained. F01 includes background/tail returns and is not certified as a pure body set. The H01 formal 589-point pixel selection is separate from the older GT-dependent 794-point corridor; the union table must be filtered by pixel_panel_589==1 for the formal result. No new selection or measurement was made for this report.

The formal geometric contract is centered Velodyne-frame x/y/z/l/w/h/yaw, complete oriented boxes and native Aeva-to-Velodyne/camera transforms. RPY variants are sensitivity checks, not replacement official geometry. Native object identities, 7D values and fixed raw-row indices are preserved. No fitted alignment or GT correction is applied.

F03 near and far are evaluated separately. Stationary status has not been independently verified; no timing rebuttal relies on assuming a parked or stationary trailer. The near right-front candidate camera remains N/A as independent confirmation of the same rear surface (atlas p. 11).

## 2. Technical clarification requested

Per-point coordinates and timing. Specify whether the released joint Aeva xyz are deskewed per point, the pose interpolation/transformation procedure, and the exact coordinate reference time. Define time_offset_ns units, zero and sign, including whether a positive offset denotes acquisition before or after the reference.

Multi-LiDAR merge and compensation. For the described seven-LiDAR setup, distinguish rigid extrinsic merging, ego-motion compensation and independent object-motion compensation, their order, and the timeline of the final coordinates. Clarify whether synchronization-accuracy statements cover sensor/frame timing only or also the coordinates after merge and compensation. Frame synchronization alone does not establish the per-point reference-time contract.

GT time and enclosure. Specify the precise GT box reference time, geometric-center and length/width/height definitions, whether boxes enclose visible/exterior surfaces, acceptable tolerance, and quality-control checks. Review the named +Y/-X surfaces in the four main frames.

Trajectory and imaging pipeline. Document smoothing, interpolation and refinement of trajectories/poses/annotations; whether motion is accounted for during scans; calibration versions; and JPEG formation/rectification versus the released projection matrices. Published interpolation flags alone do not close these contracts.

Publisher/reference-pipeline check. Confirm original basenames and SHA256 against the intended release/version, then replay the fixed point rows using the reference pipeline and the stated time/calibration contracts. Local multi-copy SHA agreement proves copy consistency, not publisher-release identity.

## 3. Scope and limitations

The stored geometric discrepancy can be independently checked, but the publisher-release identity has not been authenticated and attribution to annotation parameters, timing, compensation or calibration is not established. Three objects/four main frames are not a dataset error rate. Possible evaluation effects under strict 0.5–2 m matching thresholds are unquantified; neither magnitude nor direction has been measured.

All 14 objects / 21 object-frames remain in the 31-page atlas and correspondence table. N04 far is moderate supplementary evidence: a GT-dependent 57-point corridor has 25 points beyond the end face, maximum +0.840725 m, but overall median -1.258017 m. It is not a whole-object translation claim. N04 near and H01 far remain sparse/inconclusive. F04 is partially consistent: 51/94 selected points lie inside the complete OBB; its median is -0.093545 m. F02's selected grille has no returns; zero selected returns do not imply no neighborhood observations.

H02 and N01–N03 retain sparse/mixed/unassigned or projection-limited judgments. C01's same fixed 11 rows support a cross-camera correspondence question, not certified complete barrel point ownership. C02/C06 do not supply an independently authenticated entity-surface set. C05 neighborhood IDs are local display indices; raw point-row indices were not retained. Historical model candidates are auxiliary, not truth; query indices are not cross-model physical identities.

Public source locators are dataset-relative. SOURCE_NOT_INCLUDED identifies omitted historical inputs; EXTERNAL_SOURCE identifies released source files that are not in this repository. Provenance SHA fields identify the original saved bytes; SHA256SUMS.txt separately identifies this public package. Native source bytes were not edited. The figures contain untouched photographic scene content within existing scientific renderings.

## 4. Supporting materials and offline verification

This repository edition provides reports/Evidence_Report.md and its PDF, the 31-page reports/Evidence_Atlas.pdf, four unchanged principal figures, and compact data tables. data/correspondence.csv connects 21 case rows, 113 source-asset references, 199 existing metric extracts, 20 saved point groups and 30 atlas source figures. No full source annotation, calibration, JPEG, Aeva BIN, model weight or source-asset ZIP is published here.

Run the standard-library-only public integrity check:

    python3 scripts/verify_evidence.py

For the 20 locally held matching released source files, use an external directory whose root contains scene_35_31/, scene_36_27/ and scene_36_39/:

    python3 scripts/verify_evidence.py --source-root /path/to/TruckDrive

The first command checks public-file SHA, 21 case identities, 199 metric extracts and the fixed-point group structure. The second also checks source-file sizes and SHA, original native identities/7D for the four main frames, and exact XYZ bytes for their four saved point-row sets. It does not recompute scientific medians, select points, project boxes, fit alignment, evaluate detections or run models. METHODS.md records the geometric formulas and selection limits. Historical formula snapshots are not included as runnable pipelines; the original source hashes remain provenance references.

No dataset download or server is required by the scripts. Obtain any external source files through the publisher's authorized access route or a separately authorized nonpublic transfer; no such transfer or private link is supplied by this repository. Matching local SHA proves copy identity with the held evidence files, not authentication against an official release. Publisher reference-pipeline replay and the timing/calibration contracts are still requested. All weaker cases and N/A judgments remain visible; no new scientific measurement was added for publication.
