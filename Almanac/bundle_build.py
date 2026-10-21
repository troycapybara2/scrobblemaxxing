# Packs every out/*.csv into out/bundle.json: one file the almanac reads all its data from.
# Each row is {id, rows}; rows is that dataset's CSV as a JSON string (every cell kept as text, like a CSV upload).
import csv, json, glob, os
out = []
for p in sorted(glob.glob('out/*.csv')):
    with open(p, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    out.append({'id': os.path.basename(p)[:-4], 'rows': json.dumps(rows, ensure_ascii=False, separators=(',', ':'))})
json.dump(out, open('out/bundle.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('bundle.json', len(out), 'datasets', round(os.path.getsize('out/bundle.json') / 1e6, 2), 'MB')
