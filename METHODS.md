# Fixed evidence: method and verification boundaries

## Coordinate and face convention

The formal contract is a geometric-center yaw-only oriented box in the Velodyne frame, `(x, y, z, l, w, h, yaw)`. Complete OBB membership uses all three dimensions. Original Aeva points are transformed with the native `lidar2velo` contract before box-local comparison; no new time/pose correction or fitted transform is applied. Native camera projection and augmentation conventions were checked in the existing audit. RPY box variants are sensitivity checks only.

For a Velodyne point `p`, center `c`, and yaw `theta`, define `q = Rz(-theta) (p-c)`:

```
qx = cos(theta)*(px-cx) + sin(theta)*(py-cy)
qy = -sin(theta)*(px-cx) + cos(theta)*(py-cy)
qz = pz-cz
inside = abs(qx)<=l/2 and abs(qy)<=w/2 and abs(qz)<=h/2
H01 +Y clearance = qy - w/2
F01/F03 -X clearance = -qx - l/2
```

A positive signed face clearance is beyond that selected face, not a center error. The median/P05/P95 are the existing per-point clearance statistics on the saved selections. Points beyond other faces and mixed/background points remain in a fixed selection; outside-face count and full-OBB count need not sum to selection size. A surface discrepancy is not by itself an authenticated annotation-parameter error.

## Selections and scientific provenance

Selection was post hoc manual, not blind or representative. F01/F03 source code uses a fixed image polygon and positive camera depth, without filtering by GT OBB membership. F01 retains background/tail returns. H01's formal 589-point pixel-panel flag is separate from its older GT-dependent 794-point corridor; the union has 840 distinct saved rows. Use `pixel_panel_589==1` for H01's main result. Do not infer an error rate or universal physical ownership.

`fixed_point_indices.csv` preserves all 15,696 saved index rows in existing table order, including unassigned historical search regions. `point_groups.csv` also records zero-row groups. C05's local display IDs do not locate original BIN rows. No XYZ, UV, velocity, time or sensor channels are published in the index table. The full atlas preserves all 14 identities and 21 object-frames, including moderate, sparse, partially consistent, occluded and N/A cases.

Historical formula snapshots are not bundled as runnable programs: some depend on omitted intermediate files/imports. `metrics.csv` preserves their existing SHA identifiers and the original result JSON pointers, while `measurements.json` contains only the referenced metric values. These locators are provenance, not a claim that omitted files exist in this repository. The public verifier checks the compact extracted values consistently; the earlier local package check resolved all 199 numeric pointers against the held existing result records before this extraction.

## What the executable verifier checks

With no external inputs it verifies every public deliverable hash/size implied by SHA256SUMS.txt, 21 unique case keys / 14 scene+object identities, 199 metric IDs/values/locators, 383 correspondence rows, 20 point-group sizes, and formal selection counts 589/1461/282/1600. This is package integrity, not scientific remeasurement.

With `--source-root` it additionally verifies sizes/SHA of the 20 held released source members, native annotation IDs/Tracking_ID and exact 7D for four main frames, original BIN row bounds, and exact concatenated little-endian XYZ byte digests for their fixed selections. BIN format is 11 float64 fields, 88 bytes per row; XYZ are the first three fields; offsets are zero-based. The expected digests were obtained from existing saved row coordinates and independently checked against the held original BIN bytes. No data are downloaded, written, translated or corrected by the verifier.

The verifier intentionally does not replay projection, compensation or scientific statistics. A reference-pipeline reproduction of face clearances needs matching original source files plus the publisher's time, calibration and enclosure contracts described in the report. These upstream contracts and release authentication remain unresolved. The published formulas and fixed indices permit focused independent geometric review; they do not replace those contracts or a complete raw-data pipeline.
