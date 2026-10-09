#!/usr/bin/env python3
"""Read-only public-package and optional external-source integrity checks.

Python 3.9+ standard library. No network, data writes or scientific remeasurement.
"""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_csv(name):
    with (ROOT / 'data' / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def require(condition, description):
    if not condition:
        raise ValueError(description)


def local_member(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root.resolve()), 'Unsafe relative member: ' + relative)
    require(path.is_file(), 'Missing file: ' + relative)
    return path


def select_rows(indices, formal):
    rows = [r for r in indices if r['case_key'] == formal['case_key']
            and r['group'] == formal['group']]
    if formal['filter'] == 'pixel_panel_589==1':
        rows = [r for r in rows if r['pixel_panel_589'] == '1']
    else:
        require(formal['filter'] == 'all rows in group', 'Unsupported formal filter')
    require(len(rows) == int(formal['N']), 'Formal count: ' + formal['case_key'])
    require(all(r['raw_row_index'] for r in rows), 'Missing formal raw row index')
    require(len({r['raw_row_index'] for r in rows}) == len(rows), 'Duplicated formal index')
    return rows


def verify(source_root=None):
    checked_files = 0
    for line in (ROOT / 'SHA256SUMS.txt').read_text(encoding='utf-8').splitlines():
        expected, relative = line.split('  ', 1)
        path = local_member(ROOT, relative)
        require(digest(path) == expected, 'Public SHA mismatch: ' + relative)
        checked_files += 1

    cases = read_csv('cases.csv')
    keys = {c['case_key'] for c in cases}
    require(len(cases) == len(keys) == 21, 'Expected 21 unique case keys')
    require(len({(c['scene'], c['object_id']) for c in cases}) == 14, 'Expected 14 objects')
    for c in cases:
        require(c['case_key'] == '{}|{}|{:04d}'.format(c['scene'], c['object_id'], int(c['sync_id'])), 'Case identity: ' + c['case_key'])
        require(len(json.loads(c['native_x_y_z_l_w_h_yaw'])) == 7, '7D shape: ' + c['case_key'])

    values = json.loads((ROOT / 'data/measurements.json').read_text(encoding='utf-8'))['metrics']
    metrics = read_csv('metrics.csv')
    require(len(values) == len(metrics) == 199, 'Expected 199 existing metric extracts')
    for i, (m, v) in enumerate(zip(metrics, values)):
        require(m['metric_id'] == v['metric_id'] == 'M{:03d}'.format(i + 1), 'Metric ID')
        require(m['case_key'] == v['case_key'] and m['case_key'] in keys, 'Metric case')
        require(m['metric'] == v['metric'] and json.loads(m['value']) == v['value'], 'Metric value: ' + m['metric_id'])
        require(m['measurement_locator'] == 'data/measurements.json#/metrics/{}/value'.format(i), 'Metric locator')
        require(m['existing_result_source_sha256'] == v['original_source_sha256']
                and m['existing_result_JSON_pointer'] == v['original_JSON_pointer'], 'Metric source provenance')

    correspondence = read_csv('correspondence.csv')
    require(len(correspondence) == 383, 'Expected 383 correspondence rows')
    expected_types = {'case': 21, 'source_asset': 113, 'metric': 199, 'point_group': 20, 'figure': 30}
    require(dict(collections.Counter(r['row_type'] for r in correspondence)) == expected_types, 'Correspondence types')
    require(all(r['case_key'] in keys for r in correspondence), 'Correspondence case key')

    indices = read_csv('fixed_point_indices.csv')
    groups = read_csv('point_groups.csv')
    require(len(indices) == 15696 and len(groups) == 20, 'Expected fixed-row/group counts')
    counts = collections.Counter((r['case_key'], r['group']) for r in indices)
    declared = {(g['case_key'], g['group']) for g in groups}
    require(len(declared) == len(groups) and set(counts).issubset(declared), 'Group identity')
    for g in groups:
        require(counts[(g['case_key'], g['group'])] == int(g['rows']), 'Group row count: ' + g['case_key'])
    for r in indices:
        require(r['case_key'] in keys, 'Index case key')
        if r['raw_row_index']:
            require(int(r['raw_row_index']) >= 0, 'Negative raw row index')
        if r['group'] == 'C05_UNASSIGNED_DISPLAY_COORDINATES_NO_RAW_INDEX':
            require(not r['raw_row_index'] and r['local_display_index'], 'C05 display/raw distinction')

    formal = read_csv('formal_point_sets.csv')
    require(len(formal) == 4, 'Expected four formal fixed subsets')
    primary = {c['case_key']: c for c in cases if c['tier'] == 'primary'}
    require(set(primary) == {f['case_key'] for f in formal}, 'Formal/primary identity')
    for f in formal:
        require(int(f['N']) == int(primary[f['case_key']]['fixed_subset_N']), 'Formal case count')
        select_rows(indices, f)

    assets = read_csv('source_assets.csv')
    require(len(assets) == 113, 'Expected 113 source asset references')
    figures = read_csv('atlas_figures.csv')
    require(len(figures) == 30 and {int(f['atlas_page']) for f in figures} == set(range(2, 32)), 'Atlas page mapping')
    for f in figures:
        if not f['standalone_figure'].startswith('SOURCE_NOT_INCLUDED/'):
            path = local_member(ROOT, f['standalone_figure'])
            require(digest(path) == f['source_png_sha256'], 'Existing source figure SHA')

    result = {'status': 'PASS', 'public_files_SHA_verified': checked_files,
              'object_identities': 14, 'object_frames': 21, 'existing_metric_extracts': 199,
              'fixed_index_rows': 15696, 'fixed_groups': 20, 'formal_subsets': 4,
              'source_check': 'NOT_REQUESTED', 'scientific_remeasurement': False,
              'publisher_release_authenticated': False}
    if source_root is not None:
        require(source_root.is_dir(), 'External source root is not a directory')
        held = {}
        for a in assets:
            if a['source_held_for_local_verification'] == 'True':
                relative = a['dataset_relative_path']
                if relative in held:
                    require((a['sha256'], a['bytes']) == (held[relative]['sha256'], held[relative]['bytes']), 'Conflicting source identity')
                held[relative] = a
        require(len(held) == 20, 'Expected 20 held source-file identities')
        for relative, a in held.items():
            path = local_member(source_root, relative)
            require(path.stat().st_size == int(a['bytes']), 'Source size mismatch: ' + relative)
            require(digest(path) == a['sha256'], 'Source SHA mismatch: ' + relative)
        for f in formal:
            c = primary[f['case_key']]
            ann_relative = c['scene'] + '/annotations/bounding_boxes/' + c['annotation_filename']
            ann_path = local_member(source_root, ann_relative)
            annotation = json.loads(ann_path.read_text(encoding='utf-8'))[int(c['annotation_record_index_0based'])]
            require(annotation['id'] == c['object_id'] and str(annotation['Tracking_ID']) == c['Tracking_ID'], 'Native object ID: ' + c['case_key'])
            require([annotation[k] for k in ['x', 'y', 'z', 'l', 'w', 'h', 'yaw']] == json.loads(c['native_x_y_z_l_w_h_yaw']), 'Native 7D: ' + c['case_key'])
            path = local_member(source_root, f['dataset_BIN_path'])
            require(path.stat().st_size % 88 == 0, 'BIN stride: ' + f['dataset_BIN_path'])
            point_count = path.stat().st_size // 88
            h = hashlib.sha256()
            with path.open('rb') as stream:
                for row in select_rows(indices, f):
                    idx = int(row['raw_row_index'])
                    require(0 <= idx < point_count, 'Raw row beyond BIN: ' + c['case_key'])
                    stream.seek(88 * idx)
                    xyz_bytes = stream.read(24)
                    require(len(xyz_bytes) == 24, 'Truncated XYZ row')
                    h.update(xyz_bytes)
            require(h.hexdigest() == f['xyz_bytes_sha256'], 'Fixed original XYZ bytes: ' + c['case_key'])
        result.update(source_check='PASS', external_source_files_SHA_verified=20,
                      primary_native_annotation_checks=4, primary_original_XYZ_row_set_checks=4)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path,
                        help='External TruckDrive root containing the 20 held matching released source files; read-only')
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.source_root), indent=2))
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}, indent=2), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
