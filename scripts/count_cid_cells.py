"""
CIDコードが含まれているセルの数を確認
"""

import sys
import io
import csv
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*80)
print("CIDコード含有セルのカウント")
print("="*80)

# CSVファイル読み込み
csv_path = Path('output') / '全言語統合_テンプレート_インポート用.csv'

print(f"\nファイル: {csv_path.name}")

# CIDコードのパターン
cid_pattern = re.compile(r'\(cid:\d+\)')

# カウンター
total_cells = 0
cid_cells = 0
cid_rows = 0
cells_by_column = {}

# 行ごとの詳細
rows_with_cid = []

with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    headers = next(reader)  # ヘッダー行

    print(f"列数: {len(headers)}")
    print(f"列名: {', '.join(headers)}")

    # 列ごとのカウンター初期化
    for header in headers:
        cells_by_column[header] = 0

    for row_idx, row in enumerate(reader, start=2):  # ヘッダーの次の行から
        row_has_cid = False
        cid_in_row = []

        for col_idx, cell in enumerate(row):
            total_cells += 1

            if cid_pattern.search(cell):
                cid_cells += 1
                row_has_cid = True

                # 列名を取得
                col_name = headers[col_idx] if col_idx < len(headers) else f"列{col_idx+1}"
                cells_by_column[col_name] += 1

                # この行のCID情報を記録
                cid_matches = cid_pattern.findall(cell)
                cid_in_row.append({
                    'column': col_name,
                    'cids': cid_matches,
                    'text': cell[:50] + '...' if len(cell) > 50 else cell
                })

        if row_has_cid:
            cid_rows += 1
            rows_with_cid.append({
                'row': row_idx,
                'ja': row[0] if len(row) > 0 else '',
                'cells': cid_in_row
            })

print("\n" + "="*80)
print("統計")
print("="*80)

print(f"\n総セル数: {total_cells:,}")
print(f"CID含有セル数: {cid_cells} ({cid_cells/total_cells*100:.2f}%)")
print(f"CID含有行数: {cid_rows}")

print("\n" + "="*80)
print("列ごとのCID含有セル数")
print("="*80)

for col_name, count in cells_by_column.items():
    if count > 0:
        print(f"{col_name}: {count}セル")

print("\n" + "="*80)
print("CID含有行の詳細")
print("="*80)

for row_info in rows_with_cid[:10]:  # 最初の10行のみ表示
    print(f"\n行{row_info['row']}: {row_info['ja']}")
    for cell_info in row_info['cells']:
        print(f"  [{cell_info['column']}] CID: {', '.join(cell_info['cids'])}")
        print(f"    テキスト: {cell_info['text']}")

if len(rows_with_cid) > 10:
    print(f"\n... 他 {len(rows_with_cid) - 10} 行")

print("\n" + "="*80)
print("CIDコードの種類と出現回数")
print("="*80)

# 全CIDコードを収集
all_cids = []

with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダースキップ

    for row in reader:
        for cell in row:
            cids = cid_pattern.findall(cell)
            all_cids.extend(cids)

# CIDの頻度をカウント
from collections import Counter
cid_counter = Counter(all_cids)

print(f"\nユニークなCIDコード: {len(cid_counter)}種類")
print(f"CID出現総数: {len(all_cids)}回")

print("\n出現頻度トップ10:")
for cid, count in cid_counter.most_common(10):
    cid_num = cid.replace('(cid:', '').replace(')', '')
    print(f"  {cid} (番号:{cid_num}): {count}回")

print("\n" + "="*80)
print("完了")
print("="*80)
